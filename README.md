# ormar-postgres-extensions
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Maturity badge - level 1](https://img.shields.io/badge/Maturity-Level%201%20--%20New%20Project-yellow.svg)](https://github.com/tophat/getting-started/blob/master/scorecard.md) [![Stage](https://img.shields.io/pypi/status/ormar-postgres-extensions)](https://pypi.org/project/ormar-postgres-extensions/) [![Discord](https://img.shields.io/discord/809577721751142410?label=community%20chat)](https://discord.gg/YhK3GFcZrk)

[![Pypi](https://img.shields.io/pypi/v/ormar-postgres-extensions)](https://pypi.org/project/ormar-postgres-extensions/) [![Wheel](https://img.shields.io/pypi/wheel/ormar-postgres-extensions)](https://pypi.org/project/ormar-postgres-extensions/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ormar-postgres-extensions) [![PyPI - Downloads](https://img.shields.io/pypi/dm/ormar-postgres-extensions)](https://pypi.org/project/ormar-postgres-extensions/) [![PyPI - License](https://img.shields.io/pypi/l/ormar-postgres-extensions)](./LICENSE)

![Build Status](https://github.com/tophat/ormar-postgres-extensions/workflows/Ormar%20Postgres%20Extensions%20CICD/badge.svg) [![codecov](https://codecov.io/gh/tophat/ormar-postgres-extensions/branch/main/graph/badge.svg)](https://codecov.io/gh/tophat/ormar-postgres-extensions)

## Overview

ormar-postgres-extensions is a an extension to the[Ormar](https://github.com/collerek/ormar) ORM. It enables developers to write models that map to native PostgreSQL types.

## Motivation

[Ormar](https://github.com/collerek/ormar) is an amazing async ORM that works with [FastAPI](https://github.com/tiangolo/fastapi). However, it is agnostic to the underlying database used meaning that we cannot use native PostgreSQL types such as UUID or JSONB columns. The aim of this library is to provide Ormar fields that can be used to generate database columns with native PG types.

## Installation

```shell
python -m pip install ormar-postgres-extensions
```

## Usage

### Fields

Three native PG fields are provided. The `JSONB` and `UUID` types map to native `JSONB` and `UUID` data types respectively. The `Array` type can be used to create an array column. Using these in an Ormar model is as simple as importing the fields and using them in the model.

#### UUID

```python
from uuid import UUID

import ormar
import ormar_postgres_extensions as ormar_pg_ext


class MyModel(ormar.Model):
    uuid: UUID = ormar_pg_ext.UUID(unique=True, nullable=False)
```
#### JSONB
```python
import ormar
import ormar_postgres_extensions as ormar_pg_ext

class JSONBTestModel(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    data: dict = ormar_pg_ext.JSONB()
```
#### Array

Array field requires a bit more setup to pass the type of the array into the field

```python
import ormar
import sqlalchemy
import ormar_postgres_extensions as ormar_pg_ext

class ModelWithArray(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = ormar_pg_ext.ARRAY(item_type=sqlalchemy.String())
```

Arrays have access to three special methods that map to specific PostgreSQL array functions

##### array_contained_by

The maps to the [`contained_by`](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contained_by) operator in Postgres.

```python
await ModelWithArray.objects.filter(data__array_contained_by=["a"]).all()
```

##### array_contains

The maps to the [`contains`](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contains) operator in Postgres.

```python
await ModelWithArray.objects.filter(data__array_contains=["a"]).all()
```

##### array_overlap

The maps to the [`overlap`](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator.overlap) operator in Postgres.

```python
await ModelWithArray.objects.filter(data__array_overlap=["a"]).all()
```

## Uninstalling

```python
pip uninstall ormar-postgres-extensions
```

## Contributing

Feel free to open a PR or GitHub issue. Contributions welcome!

To develop locally, clone this repository and run `. script/bootstrap` to install test dependencies. You can then use `invoke --list` to see available commands.
To run the tests locally, PostgreSQL needs to be running. This can be easily started via `inv database`.

### See contributing [guide](https://github.com/tophat/ormar-postgres-extensions/tree/main/CONTRIBUTING.md)
## Contributors

_You don't really have to add this section yourself! Simply use [all-contributors](https://allcontributors.org/) by adding comments in your PRs like so:_
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://everttimberg.io"><img src="https://avatars.githubusercontent.com/u/6757853?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Evert Timberg</b></sub></a><br /><a href="#ideas-etimberg" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-etimberg" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-etimberg" title="Maintenance">🚧</a> <a href="https://github.com/tophat/ormar-postgres-extensions/commits?author=etimberg" title="Documentation">📖</a> <a href="https://github.com/tophat/ormar-postgres-extensions/commits?author=etimberg" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

```
@all-contributors please add <username> for <contribution type>
```

_Find out more about All-Contributors on their website!_


## License

`ormar-postgres-extensions` is licensed under [Apache License Version 2.0](https://github.com/tophat/ormar-postgres-extensions/tree/main/LICENSE).
