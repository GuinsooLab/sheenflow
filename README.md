<div align="center">
  <img src="./airflow/www/static/sheenflow.svg" alt="logo" width="120" />
  <br />
  <small>a platform to programmatically author, schedule, and monitor workflows</small>
</div>

# Sheenflow

Sheenflow is a platform to programmatically author, schedule, and monitor workflows.

When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative.

Use Sheenflow to author workflows as directed acyclic graphs (DAGs) of tasks. The Sheenflow scheduler executes your
tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing
complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production,
monitor progress, and troubleshoot issues when needed.

**Table of contents**

- [Project Focus](#project-focus)
- [Principles](#principles)
- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Official source code](#official-source-code)
- [Convenience packages](#convenience-packages)
- [Semantic versioning](#semantic-versioning)
- [Version Life Cycle](#version-life-cycle)
- [Support for Python and Kubernetes versions](#support-for-python-and-kubernetes-versions)
- [Contributing](#contributing)
- [Who uses Apache Airflow?](#who-uses-apache-airflow)
- [Who Maintains Apache Airflow?](#who-maintains-apache-airflow)
- [Can I use the Apache Airflow logo in my presentation?](#can-i-use-the-apache-airflow-logo-in-my-presentation)
- [Airflow merchandise](#airflow-merchandise)
- [Links](#links)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Project Focus

Sheenflow works best with workflows that are mostly static and slowly changing. When the DAG structure is similar from one run to the next, it clarifies the unit of work and continuity. Other similar projects include [Luigi](https://github.com/spotify/luigi), [Oozie](https://oozie.apache.org/) and [Azkaban](https://azkaban.github.io/).

Sheenflow is commonly used to process data, but has the opinion that tasks should ideally be idempotent (i.e., results of the task will be the same, and will not create duplicated data in a destination system), and should not pass large quantities of data from one task to the next (though tasks can pass metadata using Airflow's [Xcom feature](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#xcoms)). For high-volume, data-intensive tasks, a best practice is to delegate to external services specializing in that type of work.

Sheenflow is not a streaming solution, but it is often used to process real-time data, pulling data off streams in batches.

## Principles

- **Dynamic**: Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
- **Extensible**: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant**: Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful **Jinja** templating engine.
- **Scalable**: Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers.

## Requirements

Apache Airflow is tested with:

|                      | Main version (dev)   | Stable version (2.2.2)   |
| -------------------- | -------------------- | ------------------------ |
| Python               | 3.6, 3.7, 3.8, 3.9   | 3.6, 3.7, 3.8, 3.9       |
| Kubernetes           | 1.20, 1.21           | 1.18, 1.19, 1.20         |
| PostgreSQL           | 10, 11, 12, 13       | 9.6, 10, 11, 12, 13      |
| MySQL                | 5.7, 8               | 5.7, 8                   |
| SQLite               | 3.15.0+              | 3.15.0+                  |
| MSSQL(Experimental)  | 2017, 2019           |                          |

**Note**: MySQL 5.x versions are unable to or have limitations with
running multiple schedulers -- please see the [Scheduler docs](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html).
MariaDB is not tested/recommended.

**Note**: SQLite is used in Airflow tests. Do not use it in production. We recommend
using the latest stable version of SQLite for local development.

**Note**: Python v3.10 is not supported yet. For details, see [#19059](https://github.com/apache/airflow/issues/19059).

**Note**: Airflow currently can be run on POSIX-compliant Operating Systems. For development it is regularly
tested on fairly modern Linux Distros and recent versions of MacOS.
On Windows you can run it via WSL2 (Windows Subsystem for Linux 2) or via Linux Containers.
The work to add Windows support is tracked via [#10388](https://github.com/apache/airflow/issues/10388) but
it is not a high priority. You should only use Linux-based distros as "Production" execution environment
as this is the only environment that is supported. The only distro that is used in our CI tests and that
is used in the [Community managed DockerHub image](https://hub.docker.com/p/apache/airflow) is
`Debian Buster`.

## Getting started

Visit the official Airflow website documentation (latest **stable** release) for help with
[installing Airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation.html),
[getting started](https://airflow.apache.org/docs/apache-airflow/stable/start/index.html), or walking
through a more complete [tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html).

> Note: If you're looking for documentation for the main branch (latest development branch): you can find it on [s.apache.org/airflow-docs](https://s.apache.org/airflow-docs/).

For more information on Airflow Improvement Proposals (AIPs), visit
the [Airflow Wiki](https://cwiki.apache.org/confluence/display/AIRFLOW/Airflow+Improvements+Proposals).

Documentation for dependent projects like provider packages, Docker image, Helm Chart, you'll find it in [the documentation index](https://airflow.apache.org/docs/).

## Official source code

Apache Airflow is an [Apache Software Foundation](https://www.apache.org) (ASF) project,
and our official source code releases:

- Follow the [ASF Release Policy](https://www.apache.org/legal/release-policy.html)
- Can be downloaded from [the ASF Distribution Directory](https://downloads.apache.org/airflow)
- Are cryptographically signed by the release manager
- Are officially voted on by the PMC members during the
  [Release Approval Process](https://www.apache.org/legal/release-policy.html#release-approval)

Following the ASF rules, the source packages released must be sufficient for a user to build and test the
release provided they have access to the appropriate platform and tools.

## Convenience packages

There are other ways of installing and using Airflow. Those are "convenience" methods - they are
not "official releases" as stated by the `ASF Release Policy`, but they can be used by the users
who do not want to build the software themselves.

Those are - in the order of most common ways people install Airflow:

- [PyPI releases](https://pypi.org/project/apache-airflow/) to install Airflow using standard `pip` tool
- [Docker Images](https://hub.docker.com/r/apache/airflow) to install airflow via
  `docker` tool, use them in Kubernetes, Helm Charts, `docker-compose`, `docker swarm`, etc. You can
  read more about using, customising, and extending the images in the
  [Latest docs](https://airflow.apache.org/docs/docker-stack/index.html), and
  learn details on the internals in the [IMAGES.rst](https://github.com/apache/airflow/blob/main/IMAGES.rst) document.
- [Tags in GitHub](https://github.com/apache/airflow/tags) to retrieve the git project sources that
  were used to generate official source packages via git

All those artifacts are not official releases, but they are prepared using officially released sources.
Some of those artifacts are "development" or "pre-release" ones, and they are clearly marked as such
following the ASF Policy.

## Semantic versioning

As of Airflow 2.0.0, we support a strict [SemVer](https://semver.org/) approach for all packages released.

There are few specific rules that we agreed to that define details of versioning of the different
packages:

* **Airflow**: SemVer rules apply to core airflow only (excludes any changes to providers).
  Changing limits for versions of Airflow dependencies is not a breaking change on its own.
* **Airflow Providers**: SemVer rules apply to changes in the particular provider's code only.
  SemVer MAJOR and MINOR versions for the packages are independent of the Airflow version.
  For example, `google 4.1.0` and `amazon 3.0.3` providers can happily be installed
  with `Airflow 2.1.2`. If there are limits of cross-dependencies between providers and Airflow packages,
  they are present in providers as `install_requires` limitations. We aim to keep backwards
  compatibility of providers with all previously released Airflow 2 versions but
  there will sometimes be breaking changes that might make some, or all
  providers, have minimum Airflow version specified. Change of that minimum supported Airflow version
  is a breaking change for provider because installing the new provider might automatically
  upgrade Airflow (which might be an undesired side effect of upgrading provider).
* **Airflow Helm Chart**: SemVer rules apply to changes in the chart only. SemVer MAJOR and MINOR
  versions for the chart are independent from the Airflow version. We aim to keep backwards
  compatibility of the Helm Chart with all released Airflow 2 versions, but some new features might
  only work starting from specific Airflow releases. We might however limit the Helm
  Chart to depend on minimal Airflow version.
* **Airflow API clients**: SemVer MAJOR and MINOR versions follow MAJOR and MINOR versions of Airflow.
  The first MAJOR or MINOR X.Y.0 release of Airflow should always be followed by X.Y.0 release of
  all clients. The clients then can release their own PATCH releases with bugfixes,
  independently of Airflow PATCH releases.

## Version Life Cycle

Apache Airflow version life cycle:

| Version | Current Patch/Minor | State     | First Release | Limited Support | EOL/Terminated |
|---------|---------------------|-----------|---------------|-----------------|----------------|
| 2       | 2.2.2               | Supported | Dec 17, 2020  | TBD             | TBD            |
| 1.10    | 1.10.15             | EOL       | Aug 27, 2018  | Dec 17, 2020    | June 17, 2021  |
| 1.9     | 1.9.0               | EOL       | Jan 03, 2018  | Aug 27, 2018    | Aug 27, 2018   |
| 1.8     | 1.8.2               | EOL       | Mar 19, 2017  | Jan 03, 2018    | Jan 03, 2018   |
| 1.7     | 1.7.1.2             | EOL       | Mar 28, 2016  | Mar 19, 2017    | Mar 19, 2017   |

Limited support versions will be supported with security and critical bug fix only.
EOL versions will not get any fixes nor support.
We always recommend that all users run the latest available minor release for whatever major version is in use.
We **highly** recommend upgrading to the latest Airflow major release at the earliest convenient time and before the EOL date.

## Support for Python and Kubernetes versions

As of Airflow 2.0, we agreed to certain rules we follow for Python and Kubernetes support.
They are based on the official release schedule of Python and Kubernetes, nicely summarized in the
[Python Developer's Guide](https://devguide.python.org/#status-of-python-branches) and
[Kubernetes version skew policy](https://kubernetes.io/docs/setup/release/version-skew-policy/).

1. We drop support for Python and Kubernetes versions when they reach EOL. We drop support for those
   EOL versions in main right after EOL date, and it is effectively removed when we release the
   first new MINOR (Or MAJOR if there is no new MINOR version) of Airflow
   For example, for Python 3.6 it means that we drop support in main right after 23.12.2021, and the first
   MAJOR or MINOR version of Airflow released after will not have it.

2. The "oldest" supported version of Python/Kubernetes is the default one until we decide to switch to
   later version. "Default" is only meaningful in terms of "smoke tests" in CI PRs, which are run using this
   default version and the default reference image available. Currently `apache/airflow:latest`
   and `apache/airflow:2.2.1` images are Python 3.7 images as we are preparing for 23.12.2021 when will
   Python 3.6 reaches end of life.

3. We support a new version of Python/Kubernetes in main after they are officially released, as soon as we
   make them work in our CI pipeline (which might not be immediate due to dependencies catching up with
   new versions of Python mostly) we release new images/support in Airflow based on the working CI setup.

### Additional notes on Python version requirements

* Previous versions [require](https://github.com/apache/airflow/issues/8162) at least Python 3.5.3
  when using Python 3.

## Contributing

Want to help build Apache Airflow? Check out our [contributing documentation](https://github.com/apache/airflow/blob/main/CONTRIBUTING.rst).

Official Docker (container) images for Apache Airflow are described in [IMAGES.rst](https://github.com/apache/airflow/blob/main/IMAGES.rst).

## Links

- [Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Chat](https://s.apache.org/airflow-slack)
