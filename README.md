# cz-github-jira-conventional-footer

**cz-github-jira-conventional-footer** is a plugin for the [**commitizen tools**][commitizen], a toolset that helps you to create [**conventional commit messages**][conventional-commit]. Since the structure of conventional commits messages is standardized they are machine readable and allow commitizen to automaticially calculate and tag [**semantic version numbers**][semver] as well as create **CHANGELOG.md** files for your releases.

This plugin extends the commitizen tools by:
- **adding Jira issue identifiers** in a customisable footer of the commit message
- **creating links to GitHub** commits in the CHANGELOG.md
- **creating links to Jira** issues in the CHANGELOG.md

## Installation

Install with pip
```console
python -m pip install cz-github-jira-conventional-footer
```

## Configuration

The behavior of the plugin can be modified by adding the following values to your .yaml/.toml/.json config file.
Note that `github_repo` and `jira_base_url` are *required* while the others are _optional_.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `github_repo` | `str` | YES |  | Name of the repository on GitHub in format "`{username}`/`{repo name}`" |
| `jira_base_url` | `str` | YES |  | Base URL of the Jira application that tracks issues for this repository |
| `jira_prefix` | `str` | NO | None | Key for the Jira project that tracks issues for this repository. If issues for this repository are tracked on multiple Jira projects, this config value should be left blank which will prompt commitizen for full issue identifiers  |
| `jira_token` | `str` | NO | `Jira` | Token to use for the footer containing Jira issues. Cannot contain spaces or the phrase "Breaking Change". Can optionally specify the separator as either `:<space>`[^yaml-note] or `<space>#` by including it in the value. If the separator is not specified, a `:<space>` separator will automatically be added |
| `bump_pattern` | `str` | NO | [`commitizen.defaults.bump_pattern`][cz-defaults-bump-pattern] | Regex to extract information from commit (subject and body) |
| `bump_map` | `dict` | NO | [`commitizen.defaults.bump_map`][cz-defaults-bump-map] | Dictionary mapping the extracted information to a SemVer increment type (MAJOR, MINOR, PATCH) |
| `changelog_pattern` | `str` | NO | `bump_pattern` | Regex to validate the commits, this is useful to skip commits that don't meet your ruling standards like a Merge. Usually the same as bump_pattern |
| `change_type_map` | `dict` | NO | `{"feat":"Features", "fix":"Bug Fixes", "refactor":"Refactor", "perf":"Performance Improvements"}` | Convert the title of the change type that will appear in the changelog, if a value is not found, the original will be used |

[^yaml-note]: The colon (`:`) character has a special meaning in YAML syntax and must be escaped by enclosing the entire value in single quotes (ex: `jira_token: 'resolves-issue: '`)

### pre-commit

Add this plugin to the dependencies of your commit message linting with [pre-commit][pre-commit]. 

Example `.pre-commit-config.yaml` file:
```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v2.17.13
    hooks:
      - id: commitizen
        additional_dependencies: [cz-github-jira-conventional-footer]
```
Install the hook with 
```bash
pre-commit install --hook-type commit-msg
```

## Example Usage

### Configuration

Example `.cz.yaml` file:
```yaml
commitizen:
  name: cz_github_jira_conventional_footer
  tag_format: v$version
  version: 0.3.1
  github_repo: brianburwell11/cz-github-jira-conventional-footer
  jira_base_url: https://myproject.atlassian.net
  jira_prefix: XX-
```

### Making a Commit

When you call commitizen `commit` you will be prompted to enter the scope of your commit as a Jira issue id (or multiple issue ids, prefixed or without prefix, see [config](#configuration) above).

```console
$ cz commit
? Select the type of change you are committing feat: A new feature. Correlates with MINOR in SemVer
? What is the scope of this change? (class or file name): (press [enter] to skip)
 changelog
? Write a short and imperative summary of the code changes: (lower case and no period)
 add GitHub and Jira badges to CHANGELOG
? Provide additional contextual information about the code changes: (press [enter] to skip)
 Modify `changelog_message_builder_hook()` to show the commit hash and Jira issues as badges in each entry of the changelog. This is enabled by named groups in the `commit_parser` regex pattern.
? Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer No
? JIRA issue number (multiple "42, 123"). XX- 03, 04
? Add any additional footers. (press [enter] to skip)
 added-by: Brian Burwell <brianburwell11@gmail.com>
```

Creates the following commit message:
```
feat(changelog): add GitHub and Jira badges to CHANGELOG

Modify `changelog_message_builder_hook()` to show the commit hash and Jira issues as badges in each entry of the changelog. This is enabled by named groups in the `commit_parser` regex pattern.

Jira: XX-03,XX-04
added-by: Brian Burwell <brianburwell11@gmail.com>
```

### Reading the Changelog

The changelog created by commitizen (`cz changelog` or `cz bump --changelog`) contains links to the commits in Github and the Jira issues.
```markdown
### Features

- [![b56ea](https://img.shields.io/badge/-b56ea-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/b56ea677af8a969614b159316d9d28a3267f7169)[![XX-03](https://img.shields.io/badge/-XX--03-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-03)[![XX-04](https://img.shields.io/badge/-XX--04-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-04) _(changelog)_ add GitHub and Jira badges to CHANGELOG
``` 
_which renders as_
> ### Features
>
> - [![b56ea](https://img.shields.io/badge/-b56ea-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/b56ea677af8a969614b159316d9d28a3267f7169)[![XX-03](https://img.shields.io/badge/-XX--03-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-03)[![XX-04](https://img.shields.io/badge/-XX--04-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-04) _(changelog)_ add GitHub and Jira badges to CHANGELOG

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements
This plugin would not have been possible without the fantastic work from:
* [commitizen tools](https://github.com/commitizen-tools/commitizen)
* [conventional_JIRA](https://github.com/Crystalix007/conventional_jira)
* [cz_github_jira_conventional](https://github.com/apheris/cz-github-jira-conventional)


<!-- links -->
[commitizen]: https://github.com/commitizen-tools/commitizen
[conventional-commit]: https://www.conventionalcommits.org/en/v1.0.0-beta.4/
[semver]: https://semver.org/
[pre-commit]: https://pre-commit.com/
[cz-defaults-bump-pattern]: https://github.com/commitizen-tools/commitizen/blob/0497d62ef9460e5961d90d7ba35fbb4e90b8e345/commitizen/defaults.py#L67
[cz-defaults-bump-map]: https://github.com/commitizen-tools/commitizen/blob/0497d62ef9460e5961d90d7ba35fbb4e90b8e345/commitizen/defaults.py#L68