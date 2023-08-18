import pytest

import click


def test_basic_functionality():
    @click.command()
    def cli():
        pass


def test_basic_group():
    @click.group()
    def cli():
        pass

    @cli.command()
    def subcommand():
        pass


def test_string_option():
    @click.command()
    @click.option("--s", default="no value")
    def cli(s):
        pass


@pytest.mark.parametrize("default", [True, False])
def test_boolean_flag(default):
    @click.command()
    @click.option("--f", is_flag=True, default=default)
    def cli(f):
        pass


def test_choice_option():
    @click.command()
    @click.option("--method", type=click.Choice(["foo", "bar", "baz"]))
    def cli(method):
        pass


def test_choice_argument():
    @click.command()
    @click.argument("method", type=click.Choice(["foo", "bar", "baz"]))
    def cli(method):
        pass
