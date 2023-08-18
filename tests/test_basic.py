from unittest.mock import MagicMock

import click
import pytest

from devenv.fuzzy_click.fuzzy_click import FuzzyClick


def test_basic_functionality():

    @click.command("cli", help="cli help")
    def cli():
        pass

    fzf = MagicMock()
    fzf.prompt.return_value = ["cli help"]

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert fuzzy.fuzzy_to_commands == {"cli help": cli}
    assert choices == [cli]


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
