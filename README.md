<div align="right">
    <img src="https://raw.githubusercontent.com/GuinsooLab/sheenflow/main/airflow/www/static/guinsoolab-badge.png" width="60" alt="badge">
    <br />
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/GuinsooLab/sheenflow/main/airflow/www/static/sheenflow.svg" alt="logo" width="120" />
  <br />
  <small>a platform to programmatically author, schedule, and monitor workflows</small>
</div>

# [Sheenflow](https://ciusji.gitbook.io/sheenflow/)

[![GitHub Build](https://github.com/apache/airflow/workflows/CI%20Build/badge.svg)](https://github.com/apache/airflow/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/apache/airflow/main.svg)](https://codecov.io/github/apache/airflow?branch=main)
[![License](https://img.shields.io/:license-Apache%202-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.txt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/apache-airflow.svg)](https://pypi.org/project/apache-airflow/)
[![Docker Pulls](https://img.shields.io/docker/pulls/apache/airflow.svg)](https://hub.docker.com/r/apache/airflow)

Sheenflow is a platform to programmatically author, schedule, and monitor workflows.

When workflows are defined as code, they become more maintainable, versional, testable, and collaborative.

Use Sheenflow to author workflows as directed acyclic graphs (DAGs) of tasks. The Sheenflow scheduler executes your tasks
on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries
on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress,
and troubleshoot issues when needed.

## Overview

![sheenflow-overview](https://raw.githubusercontent.com/GuinsooLab/sheenflow/main/airflow/www/static/sheenflow-overview.jpg)

## Getting started

Visit the official Sheenflow website documentation (latest **stable** release) for help with
[installing Sheenflow](https://ciusji.gitbook.io/sheenflow/overview/installation)
and [getting started](https://ciusji.gitbook.io/sheenflow/overview/quickstart).

For more information on Sheenflow Improvement Proposals (AIPs), visit
the [Sheenflow Docs](https://ciusji.gitbook.io/sheenflow/).

## Documentation

- [Welcome to Sheenflow!](https://ciusji.gitbook.io/sheenflow/)
- [Overview](https://ciusji.gitbook.io/sheenflow/overview/quickstart)
  - [Quickstart](https://ciusji.gitbook.io/sheenflow/overview/quickstart)
  - [Installation](https://ciusji.gitbook.io/sheenflow/overview/installation)
  - [Concepts](https://ciusji.gitbook.io/sheenflow/overview/concepts)
- [Executors](https://ciusji.gitbook.io/sheenflow/executors/local-executors)
  - [Local Executors](https://ciusji.gitbook.io/sheenflow/executors/local-executors)
  - [Remote Executors](https://ciusji.gitbook.io/sheenflow/executors/remote-executors)
- [DAGs](https://ciusji.gitbook.io/sheenflow/dags/dag-run-status)
  - [DAG Run Status](https://ciusji.gitbook.io/sheenflow/dags/dag-run-status)
  - [Cron Presets](https://ciusji.gitbook.io/sheenflow/dags/cron-presets)
  - [External Triggers](https://ciusji.gitbook.io/sheenflow/dags/external-triggers)
- [Lineage](https://ciusji.gitbook.io/sheenflow/lineage/shorthand-notation)
  - [Shorthand Notation](https://ciusji.gitbook.io/sheenflow/lineage/shorthand-notation)
  - [Lineage Backend](https://ciusji.gitbook.io/sheenflow/lineage/lineage-backend)
- [Reference](https://ciusji.gitbook.io/sheenflow/references/operators-and-hooks)
  - [Operators and Hooks](https://ciusji.gitbook.io/sheenflow/references/operators-and-hooks)
  - [CLI](https://ciusji.gitbook.io/sheenflow/references/cli)
  - [Template](https://ciusji.gitbook.io/sheenflow/references/templates)
  - [APIs](https://ciusji.gitbook.io/sheenflow/references/apis)
  - [Configurations](https://ciusji.gitbook.io/sheenflow/references/configurations)
- [Appendix](https://ciusji.gitbook.io/sheenflow/appendix/faq)
  - [FAQ](https://ciusji.gitbook.io/sheenflow/appendix/faq)

## Project Focus

Sheenflow works best with workflows that are mostly static and slowly changing. When the DAG structure is similar from one run to the next, it clarifies the unit of work and continuity. Other similar projects include [Dagster](https://github.com/dagster-io/dagster) and [Prefect](https://github.com/prefecthq/prefect).

Sheenflow is commonly used to process data, but has the opinion that tasks should ideally be idempotent (i.e., results of the task will be the same, and will not create duplicated data in a destination system), and should not pass large quantities of data from one task to the next. For high-volume, data-intensive tasks, a best practice is to delegate to external services specializing in that type of work.

Sheenflow is not a streaming solution, but it is often used to process real-time data, pulling data off streams in batches.

## Principles

- **Dynamic**: Sheenflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
- **Extensible**: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant**: Sheenflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Sheenflow using the powerful **Jinja** templating engine.
- **Scalable**: Sheenflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers.

## Requirements

Sheenflow is tested with:

|                     | Main version (dev)           | Stable version (2.3.3)       |
|---------------------|------------------------------|------------------------------|
| Python              | 3.7, 3.8, 3.9, 3.10          | 3.7, 3.8, 3.9, 3.10          |
| Platform            | AMD64/ARM64(\*)              | AMD64/ARM64(\*)              |
| Kubernetes          | 1.20, 1.21, 1.22, 1.23, 1.24 | 1.20, 1.21, 1.22, 1.23, 1.24 |
| PostgreSQL          | 10, 11, 12, 13, 14           | 10, 11, 12, 13, 14           |
| MySQL               | 5.7, 8                       | 5.7, 8                       |
| SQLite              | 3.15.0+                      | 3.15.0+                      |
| MSSQL               | 2017(\*), 2019 (\*)          | 2017(\*), 2019 (\*)          |
| Guinsoo             | coming                       | coming                       |

**Note**: Sheenflow currently can be run on POSIX-compliant Operating Systems. For development it is regularly
tested on fairly modern Linux Distros and recent versions of MacOS.
On Windows you can run it via WSL2 (Windows Subsystem for Linux 2) or via Linux Containers.

## Approach for dependencies for Sheenflow Core

Those `extras` and `providers` dependencies are maintained in `setup.cfg`.

There are few dependencies that we decided are important enough to upper-bound them by default, as they are
known to follow predictable versioning scheme, and we know that new versions of those are very likely to
bring breaking changes. We commit to regularly review and attempt to upgrade to the newer versions of
the dependencies as they are released, but this is manual process.

The important dependencies are:

* `SQLAlchemy`: upper-bound to specific MINOR version (SQLAlchemy is known to remove deprecations and
   introduce breaking changes especially that support for different Databases varies and changes at
   various speed (example: SQLAlchemy 1.4 broke MSSQL integration for Sheenflow)
* `Alembic`: it is important to handle our migrations in predictable and performant way. It is developed
   together with SQLAlchemy. Our experience with Alembic is that it very stable in MINOR version
* `Flask`: We are using Flask as the back-bone of our web UI and API. We know major version of Flask
   are very likely to introduce breaking changes across those so limiting it to MAJOR version makes sense
* `werkzeug`: the library is known to cause problems in new versions. It is tightly coupled with Flask
   libraries, and we should update them together
* `celery`: Celery is crucial component of Sheenflow as it used for CeleryExecutor (and similar). Celery
   [follows SemVer](https://docs.celeryq.dev/en/stable/contributing.html?highlight=semver#versions), so
   we should upper-bound it to the next MAJOR version. Also, when we bump the upper version of the library,
   we should make sure Celery Provider minimum Sheenflow version is updated).
* `kubernetes`: Kubernetes is a crucial component of Sheenflow as it is used for the KubernetesExecutor
   (and similar). Kubernetes Python library [follows SemVer](https://github.com/kubernetes-client/python#compatibility),
   so we should upper-bound it to the next MAJOR version. Also, when we bump the upper version of the library,
   we should make sure Kubernetes Provider minimum Sheenflow version is updated.

## Support for providers

Providers released by the community have limitation of a minimum supported version of Sheenflow. The minimum
version of Sheenflow is the `MINOR` version (2.1, 2.2 etc.) indicating that the providers might use features
that appeared in this release. The default support timespan for the minimum version of Sheenflow
(there could be justified exceptions) is that we increase the minimum Sheenflow version, when 12 months passed
since the first release for the MINOR version of Sheenflow.

For example this means that by default we upgrade the minimum version of Sheenflow supported by providers
to 2.2.0 in the first Provider's release after 21st of May 2022 (21st of May 2021 is the date when the
first `PATCHLEVEL` of 2.1 (2.1.0) has been released.

## Contributing

Want to help build Sheenflow? Check out our [contributing documentation](https://github.com/GuinsooLab/sheenflow/blob/main/CONTRIBUTING.rst).

## License

[Apache License Version 2.0](./LICENSE)
