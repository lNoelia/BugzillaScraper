import click

from src.run import run_scrapper


@click.command('run', help="Run the main issue processing flow.")
def run():
    """Wrapper to call the main function."""
    run_scrapper()


@click.command('run:default', help="Run the issue processing flow with default parameters ('---' and 'None').")
def run_default():
    """Wrapper to call the main function with default parameters."""
    run_scrapper(resolution="---", status=None)


if __name__ == '__main__':
    run()
