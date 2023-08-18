import click
import pytest
from click.core import Command

from devenv.fuzzy_click.fuzzy_click import FuzzyClick
from devenv.fuzzy_click.utils import to_fuzzy


def test_basic_functionality(fzf):
    @click.command("cli", help="cli help")
    def cli():
        pass

    fzf.should_return(["cli help"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [cli])


def test_basic_functionality__nothing_chosen(fzf):
    @click.command("cli", help="cli help")
    def cli():
        pass

    fzf.should_return([])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [])


def test_basic_group(fzf):
    @click.group("cli", help="cli help")
    def cli():
        pass

    @cli.command("subcommand", help="subcommand help")
    def subcommand():
        pass

    fzf.should_return(["cli help", "subcommand help"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [subcommand, cli])
    assert_same_callbacks(choices, [cli, subcommand])


def test_string_option_with_default(fzf):
    @click.command("cli", help="cli help")
    @click.option("-s", default="some value", help="string option")
    def cli(_):
        pass

    fzf.should_return(["cli help -s some value"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [cli])


@pytest.mark.parametrize("default", [True, False])
def test_boolean_flag(fzf, default):
    @click.command("cli", help="cli help")
    @click.option("-f", is_flag=True, default=default)
    def cli(_):
        pass

    fzf.should_return([f"cli help -f {str(default)}"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [cli])


def test_choice_option(fzf):
    @click.command("cli", help="cli help")
    @click.option("-m", type=click.Choice(["foo", "bar", "baz"]))
    def cli(_):
        pass

    fzf.should_return(["cli help -m foo"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose()

    assert_same_callbacks(fuzzy.commands, [cli, cli, cli, cli])
    assert_same_callbacks(choices, [cli])
    assert_same_fuzzies(fuzzy.commands, ["cli help -m <input>", "cli help -m foo", "cli help -m bar", "cli help -m baz"])


def assert_same_callbacks(commands1: list[Command], commands2: list[Command]):
    assert len(commands1) == len(commands2)
    for c1, c2 in zip(commands1, commands2):
        assert_same_callback(c1, c2)


def assert_same_callback(command1: Command, command2: Command):
    assert command1.callback == command2.callback


def assert_same_fuzzies(commands: list[Command], fuzzies: list[str]):
    assert len(commands) == len(fuzzies)
    assert [to_fuzzy(c) for c in commands] == fuzzies


def assert_same_fuzzy(command1: Command, fuzzy: str):
    assert to_fuzzy(command1) == fuzzy
