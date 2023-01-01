import click

try:
    from sheenflow_managed_elements.cli import apply_cmd, check_cmd

    @click.group()
    def main():
        pass

    main.add_command(check_cmd)
    main.add_command(apply_cmd)


except ImportError:

    @click.group(
        help="In order to use managed Airbyte config, the sheenflow-managed-elements package must be installed."
    )
    def main():
        pass
