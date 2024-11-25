import click

from src.run import run_scrapper
from datetime import datetime

def validate_date(ctx, param, value):
    if value is None:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise click.BadParameter('Datetime must be in format YYYY-MM-DD')

@click.command('run', help="Run the main issue processing flow.")
@click.option('--from-date', default=None, callback=validate_date, help='Start date in format YYYY-MM-DD')
def run(from_date):
    """Wrapper to call the main function."""
    run_scrapper(from_date=from_date)


@click.command('run:default', short_help="Run the issue processing flow with default parameters (No filter applied to status or resolution).")
@click.option('--from-date', default=None, callback=validate_date, help='Start date in format YYYY-MM-DD')
def run_default(from_date):
    """Wrapper to call the main function with default parameters."""
    run_scrapper(resolution="TOTAL", status="TOTAL", from_date=from_date)


if __name__ == '__main__':
    run()
