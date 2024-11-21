import click


@click.command('test', help="A simple command to print a test message.")
def test():
    click.echo("This is a test")


if __name__ == '__main__':
    test()
