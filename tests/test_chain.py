import click


def test_basic_chaining():
    @click.group(chain=True)
    def cli():
        pass

    @cli.command("sdist")
    def sdist():
        pass

    @cli.command("bdist")
    def bdist():
        pass


def test_chaining_with_options():
    @click.group(chain=True)
    def cli():
        pass

    @cli.command("sdist")
    @click.option("--format")
    def sdist(format):
        pass

    @cli.command("bdist")
    @click.option("--format")
    def bdist(format):
        pass


def test_chaining_with_arguments():
    @click.group(chain=True)
    def cli():
        pass

    @cli.command("sdist")
    @click.argument("format")
    def sdist(format):
        pass

    @cli.command("bdist")
    @click.argument("format")
    def bdist(format):
        pass
