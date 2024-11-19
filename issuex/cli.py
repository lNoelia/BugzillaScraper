import click

from issuex.commands.test import test


class IssuexCLI(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        click.echo(f"No such command '{cmd_name}'.")
        click.echo("Try 'rosemary --help' for a list of available commands.")
        return None


@click.group(cls=IssuexCLI)
def cli():
    """A CLI tool to help with project development."""
    pass


cli.add_command(test)

if __name__ == '__main__':
    cli()
