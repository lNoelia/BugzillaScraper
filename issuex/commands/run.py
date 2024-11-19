import click

from src.run import run_scrapper


@click.command('run', help="Run the main issue processing flow.")
def run():
    """Wrapper to call the main function."""
    run_scrapper()


if __name__ == '__main__':
    run()
