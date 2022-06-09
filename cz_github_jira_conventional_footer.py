import os
import re
from typing import Any, Dict, List, Optional

from commitizen import defaults, git, config
from commitizen.exceptions import CommitizenException, ExitCode
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.cz.exceptions import CzException
from yaml.scanner import Scanner, ScannerError

__all__ = ["GithubJiraConventionalFooterCz"]

CONVENTIONAL_COMMIT_REGEX = (
    r"^(?P<change_type>feat|fix|refactor|perf)(?:\((?P<scope>\w+)\))?(?P<breaking>\!)?: (?P<subject>.*)"
    r"(?s:\n\n(?P<body>^(?:(?!^\n^{BREAKING(?: |-)CHANGE|[\w-]+}{ #|: }).)*)?"
    r"(?:\n^\n(?P<footers>.*))+)"
)
"""regular expression pattern with named groups for conventional commits v1.0.0-beta.4"""


class MissingConfigKey(CommitizenException):
    """Exception raised when a required config key is not defined."""

    exit_code = ExitCode.INVALID_CONFIGURATION

    def __init__(self, config_key: str):
        super().__init__(config_key)
        self.message = f"Missing required config key: {config_key}"


class InvalidConfigValue(CommitizenException):
    """Exception raised when a config value doesn't match a criteria."""

    exit_code = ExitCode.INVALID_CONFIGURATION

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidAnswerError(CzException):
    ...


class GithubJiraConventionalFooterCz(BaseCommitizen):
    # set defaults for optional config values
    commit_parser = CONVENTIONAL_COMMIT_REGEX
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    changelog_pattern = defaults.bump_pattern
    change_type_map = {
        "feat": "Feat",
        "fix": "Fix",
        "refactor": "Refactor",
        "perf": "Perf",
    }
    jira_prefix = ""
    issue_multiple_hint = "XZ-42, XY-123"
    jira_token = "Jira: "

    # read the config file and replace default if setting is defined
    try:
        conf = config.read_cfg()
    except ScannerError as e:
        if e.problem == "mapping values are not allowed here":
            error_message = (
                "Raw mapping values not allowed.\n\n"
                + 'Are you trying to define a footer token containing ":"? If so, be sure to enclose your defined value in quotation marks. For example,\n'
                + '\tjira_token: "resolves-issue: "'
            )
            raise InvalidConfigValue(error_message)
        raise

    if "jira_prefix" in conf.settings:
        jira_prefix = conf.settings["jira_prefix"]
        issue_multiple_hint = "42, 123"
    jira_token = str(conf.settings.get("jira_token", jira_token))
    if not (jira_token.endswith(": ") or jira_token.endswith(" #")):
        jira_token = f"{jira_token}: "
    bump_pattern = conf.settings.get("bump_pattern", bump_pattern)
    bump_map = conf.settings.get("bump_map", bump_map)
    changelog_pattern = conf.settings.get("changelog_pattern", changelog_pattern)
    change_type_map = conf.settings.get("change_type_map", change_type_map)
    try:
        jira_base_url = conf.settings["jira_base_url"]
        github_repo = conf.settings["github_repo"]
    except KeyError as e:
        raise MissingConfigKey(e)

    # validate format for config settings
    if re.fullmatch(r"^(?i)BREAKING( |-)CHANGE( #|: )?", jira_token):
        raise InvalidConfigValue(
            "jira_token cannot match regex ^(?i)BREAKING( |-)CHANGE( #|: )"
        )
    if not (re.fullmatch(r"^(?i)[\w-]+(?: #|: )$", jira_token)):
        raise InvalidConfigValue("jira_token must match regex ^(?i)[\w-]+( #|: )?$")

    def questions(self) -> List[Dict[str, Any]]:
        questions: List[Dict[str, Any]] = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "fix",
                        "name": "fix: A bug fix. Correlates with PATCH in SemVer",
                    },
                    {
                        "value": "feat",
                        "name": "feat: A new feature. Correlates with MINOR in SemVer",
                    },
                    {"value": "docs", "name": "docs: Documentation only changes"},
                    {
                        "value": "style",
                        "name": (
                            "style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                    },
                    {
                        "value": "perf",
                        "name": "perf: A code change that improves performance",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Adding missing or correcting " "existing tests"
                        ),
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "What is the scope of this change? (class or file name): (press [enter] to skip)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: (lower case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "breaking_change",
                "message": "Describe the breaking change:\n",
                "when": lambda x: x["is_breaking_change"],
            },
            {
                "type": "input",
                "name": "jira_issues",
                "message": (
                    f'JIRA issue number (multiple "{self.issue_multiple_hint}"). {self.jira_prefix}'
                ),
                "filter": self.parse_jira_issues,
            },
            {
                "type": "input",
                "name": "footer",
                "message": "Add any additional footers. (press [enter] to skip)\n",
            },
        ]
        return questions

    def parse_jira_issues(self, text):
        """
        Parse the issues given and add Jira prefixes if they were specified in the config.
        """

        if self.jira_prefix:
            issueRE = re.compile(r"\d+")
        else:
            issueRE = re.compile(r"\w+-\d+")

        if not text:
            return ""

        issues = [i.strip() for i in text.strip().split(",")]
        for issue in issues:
            if not issueRE.fullmatch(issue):
                raise InvalidAnswerError(f"Jira issue of '{issue}' is invalid")

        if len(issues) == 1:
            return self.jira_prefix + issues[0]

        return ",".join([self.jira_prefix + i for i in issues])

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]
        jira_issues = answers["jira_issues"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if jira_issues:
            footer = f"{self.jira_token}{jira_issues}\n{footer}"
        if is_breaking_change:
            breaking_change = answers["breaking_change"]
            footer = f"BREAKING CHANGE: {breaking_change}\n{footer}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}{'!' if is_breaking_change else ''}: {subject}{body}{footer}"

        return message

    def example(self) -> str:
        return (
            "fix(lang)!: add polish language\n"
            "\n"
            "see the issue for details on the implementation\n"
            "\n"
            "BREAKING CHANGE: clients must add Polish as a language option\n"
            "Jira: XX-01"
        )

    def schema(self) -> str:
        return (
            "<type>(<scope>)(!): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: <breaking change>)\n"
            "(<jira_token><jira issues>)\n"
            "<footer>"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(\S+\))?!?:(\s.*)"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:
        """add github and jira links to the readme as badges"""

        rev = commit.rev[:5]
        github_commit_badge_img = get_badge_image(
            "", rev, "%23121011", "github", "white"
        )
        github_commit_badge = f"[{github_commit_badge_img}](https://github.com/{self.github_repo}/commit/{commit.rev})"

        jira_issue_badges = []
        if parsed_message["footers"]:
            jira_issues = []
            for footer_value in re.findall(
                rf"^Jira: (?P<issues>.+)$",
                parsed_message["footers"],
                re.IGNORECASE | re.MULTILINE,
            ):
                [
                    jira_issues.append(issue_id.strip())
                    for issue_id in footer_value.split(",")
                ]

            for issue_id in jira_issues:
                issue_badge_img = get_badge_image(
                    "",
                    issue_id.replace("-", "--"),
                    "dfe1e5",
                    "jira",
                    "0052cc",
                    alt_text=issue_id,
                )
                issue_badge = (
                    f"[{issue_badge_img}]({self.jira_base_url}/browse/{issue_id})"
                )
                jira_issue_badges.append(issue_badge)
        parsed_message[
            "message"
        ] = f"{github_commit_badge}{''.join([badge for badge in jira_issue_badges])} {parsed_message['subject']}"
        return parsed_message


def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return "-".join(scope)


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


def get_badge_image(
    label: str,
    value: str,
    background_color: str,
    logo: Optional[str] = None,
    logo_color: Optional[str] = None,
    style: Optional[str] = None,
    alt_text: Optional[str] = None,
) -> str:
    """get a badge from https://shields.io/ as markdown"""

    if not style:
        style = "flat-square"
    if not alt_text:
        alt_text = value
    badge_img = (
        f"https://img.shields.io/badge/-{value}-{background_color}.svg?style={style}"
    )
    if logo:
        badge_img = f"{badge_img}&logo={logo}"
        if logo_color:
            badge_img = f"{badge_img}&logoColor={logo_color}"
    badge_img = f"{badge_img}"
    return f"![{alt_text}]({badge_img})"


discover_this = GithubJiraConventionalFooterCz
