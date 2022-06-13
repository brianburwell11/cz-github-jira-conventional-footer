## v1.0.0 (2022-06-13)

### Bug Fixes

- [![53997](https://img.shields.io/badge/-53997-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/53997cee306c596191f52ce44976f338f0013e1c)[![XX-99](https://img.shields.io/badge/-XX--99-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-99) add `re.MULTILINE` flag to find Jira footers
- [![33855](https://img.shields.io/badge/-33855-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/338556f2d9bb1b19c1f347eef5428b641eb98782) correct invalid regex pattern in commit_parser

## v0.3.0 (2022-06-09)

### Refactor

- [![6c157](https://img.shields.io/badge/-6c157-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/6c1576bdb23ae984f0c943ee1c39a60da37e806a)[![XX-42](https://img.shields.io/badge/-XX--42-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-42)[![XX-123](https://img.shields.io/badge/-XX--123-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-123) _(config)_ use `dict.get()` to handle defaults for optional keys
- [![82b37](https://img.shields.io/badge/-82b37-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/82b375b41aba9f8c52a2843ebfef5b6c49f4b979)[![XX-19](https://img.shields.io/badge/-XX--19-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-19) _(config)_ raise custom exceptions for invalid config settings
- [![205e5](https://img.shields.io/badge/-205e5-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/205e5ef59239fba8274188e2a4795021e75f2021)[![XX-06](https://img.shields.io/badge/-XX--06-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-06) convert config checks to EAFP

### Features

- [![94fe6](https://img.shields.io/badge/-94fe6-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/94fe63d6d84897f2d36dfa4c0054c676db6cbfb9)[![XX-99](https://img.shields.io/badge/-XX--99-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-99) _(config)_ add optional config for standard commitizen settings

## v0.2.0 (2022-06-09)

### Features

- [![b56ea](https://img.shields.io/badge/-b56ea-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/b56ea677af8a969614b159316d9d28a3267f7169)[![XX-03](https://img.shields.io/badge/-XX--03-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-03)[![XX-04](https://img.shields.io/badge/-XX--04-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-04) _(changelog)_ add GitHub and Jira badges to CHANGELOG
- [![22ebe](https://img.shields.io/badge/-22ebe-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/22ebe396d6e6a336513ecd508631747900b91092)[![XX-02](https://img.shields.io/badge/-XX--02-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-02) _(config)_ add a configurable `jira_token`
- [![e0c29](https://img.shields.io/badge/-e0c29-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/e0c29e515fd50acf4e4339556940dd8c0d6b75ac) remove required validator on Jira issues
- [![eacc3](https://img.shields.io/badge/-eacc3-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/eacc3543ee30be575455633471720a7a33502553) _(message)_ separate breaking changes from other footers
- [![c78eb](https://img.shields.io/badge/-c78eb-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/c78eb3499eb997bf9124c01a1b9b7990e0a7c682) add question for jira issues
- [![aa657](https://img.shields.io/badge/-aa657-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/aa6575373cc235c976539b6f36f966e3b683e955) remove jira requirement in message scope

### Bug Fixes

- [![48ee9](https://img.shields.io/badge/-48ee9-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/48ee9e8a032dde2dcebfdd8f2ed6c94465e9cca7)[![XX-00](https://img.shields.io/badge/-XX--00-dfe1e5.svg?style=flat-square&logo=jira&logoColor=0052cc)](https://myproject.atlassian.net/browse/XX-00) _(message)_ add `!` after the type (or scope) of breaking change commits
- [![beefc](https://img.shields.io/badge/-beefc-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/beefc33b3546d9ec06ced1caac9ceef35c05644b) _(changelog)_ remove extra parentheses

## v0.1.0 (2022-06-07)

### Bug Fixes

- [![a99a7](https://img.shields.io/badge/-a99a7-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/a99a796cec4b4cca435cc5fd628d699606da39fb) change commitizen config file to use this plugin

### Features

- [![70723](https://img.shields.io/badge/-70723-%23121011.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/brianburwell11/cz-github-jira-conventional-footer/commit/7072339bd57c26d92f3ed91aefe419e7d917c9ca) _(changelog)_ format links to Jira and GitHub as badges
