# Contributing

:tada: Thanks for taking the time to contribute! :tada:

The following is a set of guidelines for contributing to [ormar-postgres-extenions](https://github.com/tophat/ormar-postgres-extensions).

These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document.

## Table Of Contents

[Code of Conduct](#code-of-conduct)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)

- [Python 3](#python-3)
- [Releases](#releases)

[How Can I Contribute?](#how-can-i-contribute)

- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Pull Requests](#pull-requests)

[Styleguides](#styleguides)

- [Code Styleguide](#code-styleguide)
- [`pathlib` over `os.path`](#usage-of-pathlib)

[Additional Notes](#additional-notes)

- [Issue and Pull Request Labels](#issue-and-pull-request-labels)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## What should I know before I get started

### Python 3

- Python typing and hints: [typing](https://docs.python.org/3/library/typing.html)

### Releases

- Semantic versioning: [semver](https://semver.org/spec/v2.0.0.html)

## How Can I Contribute

Before diving into writing code, please take a look at the following.

### Reporting Bugs

When attempting to fix a bug, create an issue using the "Bug report" template.

Give as much information in this issue as it allows for discussions and documentation about the decisions reached for any bugs that have been encounted.

### Suggesting Enhancements

Have an idea? Create an issue using the "Feature request" template.

Detailing in there as much as possible, the idea and any potential solutions to it, before suggesting a pull request.

### Your First Code Contribution

Have an issue to submit code changes for? See below.

#### Local development

- Clone the repository
- Run `. script/bootstrap` to ensure you're working from the correct environment
- Run `inv test` to verify enviroment is correctly setup
- Checkout a new branch and add code changes
- Add tests to verify code changes and rerun `inv test`
- See submitting [pull requests](#pull-requests)

### Pull Requests

Creating a pull request uses our template using the GitHub web interface.

Fill in the relevant sections, clearly linking the issue the change is attemping to resolve.

## Styleguides

### Code Styleguide

A linter is available to catch most of our styling concerns.
This is provided in a pre-commit hook when setting up [local development](#local-development).

You can also run `inv lint --fix` to see and solve what issues it can.

## Additional Notes

### Issue and Pull Request Labels

Please tag issues and pull requests according to the relevant [github labels](https://github.com/tophat/ormar-postgres-extensions/issues/labels).
