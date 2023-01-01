# Makefile oddities:
# - Commands must start with literal tab characters (\t), not spaces.
# - Multi-command rules (like `black` below) by default terminate as soon as a command has a non-0
#   exit status. Prefix the command with "-" to instruct make to continue to the next command
#   regardless of the preceding command's exit status.

# NOTE: See pyproject.toml [tool.black] for majority of black config. Only include/exclude options
# and format targets should be specified here. Note there are separate pyproject.toml for the root
# and examples/docs_snippets.
#
# NOTE: Use `extend-exclude` instead of `exclude`. If `exclude` is provided, it stops black from
# reading gitignore. `extend-exclude` is layered on top of gitignore. See:
#   https://black.readthedocs.io/en/stable/usage_and_configuration/file_collection_and_discovery.html#gitignore
black:
	black --fast \
    --extend-exclude="examples/docs_snippets|snapshots" \
    examples integration_tests helm python_modules .buildkite
	black --fast \
    examples/docs_snippets

check_black:
	black --check --fast \
    --extend-exclude="examples/docs_snippets|snapshots" \
    examples integration_tests helm python_modules .buildkite
	black --check --fast \
    examples/docs_snippets

# NOTE: We use `git ls-files` instead of isort's built-in recursive discovery
# because it is much faster. Note that we also need to skip files with `git
# ls-files` (the `:!:` directives are exclued patterns). Even isort
# `--skip`/`--filter-files` is very slow.
isort:
	isort \
    `git ls-files '.buildkite/*.py' 'examples/*.py' 'integration_tests/*.py' 'helm/*.py' 'python_modules/*.py' \
      ':!:examples/docs_snippets' \
      ':!:*/snapshots/*.py'`
	isort \
   `git ls-files 'examples/docs_snippets/*.py'`

check_isort:
	isort --check \
    `git ls-files '.buildkite/*.py' 'examples/*.py' 'integration_tests/*.py' 'helm/*.py' 'python_modules/*.py' \
      ':!:examples/docs_snippets' \
      ':!:*/snapshots/*.py'`
	isort --check \
    `git ls-files 'examples/docs_snippets/*.py'`

pylint:
	pylint \
    `git ls-files '.buildkite/*.py' 'examples/*.py' 'integration_tests/*.py' \
      'helm/*.py' 'python_modules/*.py' 'scripts/*.py' \
      ':!:examples/with_airflow' \
      ':!:python_modules/libraries/sheenflow-airflow' \
      ':!:vendor' \
      ':!:*/snapshots/*.py'`

yamllint:
	yamllint -c .yamllint.yaml --strict \
    `git ls-files 'helm/*.yml' 'helm/*.yaml' ':!:helm/**/templates/*.yml' ':!:helm/**/templates/*.yaml'`

# NOTE: pkg_config with M1 chip: PKG_CONFIG_PATH=/opt/homebrew/opt/openblas/lib/pkgconfig
# See: https://lightrun.com/answers/scipy-scipy-bug-pip-install-scipy-from-git-fails-with-openblas-not-found
install_dev_python_modules:
	python scripts/install_dev_python_modules.py -qqq

install_dev_python_modules_verbose:
	python scripts/install_dev_python_modules.py

graphql:
	cd js_modules/sheenlet/; make generate-graphql; make generate-perms

sanity_check:
# NOTE:  fails on nonPOSIX-compliant shells (e.g. CMD, powershell)
	@echo Checking for prod installs - if any are listed below reinstall with 'pip -e'
	@! (pip list --exclude-editable | grep -e sheenflow -e sheenlet)

rebuild_sheenlet: sanity_check
	cd js_modules/sheenlet/; yarn install && yarn build

rebuild_sheenlet_with_profiling: sanity_check
	cd js_modules/sheenlet/; yarn install && yarn build-with-profiling

dev_install: install_dev_python_modules_verbose rebuild_sheenlet

dev_install_quiet: install_dev_python_modules rebuild_sheenlet

graphql_tests:
	pytest python_modules/sheenflow-graphql/sheenflow_graphql_tests/graphql/ -s -vv

check_manifest:
	check-manifest python_modules/sheenflow
	check-manifest python_modules/sheenlet
	check-manifest python_modules/sheenflow-graphql
	ls python_modules/libraries | xargs -n 1 -Ipkg check-manifest python_modules/libraries/pkg
