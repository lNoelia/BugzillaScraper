import click

from src.run import run_scrapper


@click.command('run', help="Run the main issue processing flow.")
def run():
    """Wrapper to call the main function."""
    run_scrapper()


@click.command('run:default', short_help="Run the issue processing flow with default parameters (No filter applied to status or resolution).")
def run_default():
    """Wrapper to call the main function with default parameters."""
    run_scrapper(resolution="TOTAL", status="TOTAL")


if __name__ == '__main__':
    run()
