import click
import pytest
from click.core import Command, Context

from devenv.fuzzy_click.fuzzy_click import FuzzyClick
from devenv.fuzzy_click.utils import to_fuzzy


def test_basic_functionality(fzf):
    @click.command("cli", help="cli help")
    def cli():
        pass

    fzf.should_return(["cli help"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [cli])


def test_basic_functionality__nothing_chosen(fzf):
    @click.command("cli", help="cli help")
    def cli():
        pass

    fzf.should_return([])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_callbacks(choices, [])


def test_basic_group(fzf):
    @click.group("cli", help="cli help")
    def cli():
        pass

    @cli.command("subcommand", help="subcommand help")
    def subcommand():
        pass

    fzf.should_return(["subcommand help"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_callbacks(fuzzy.commands, [subcommand])
    assert_same_callbacks(choices, [subcommand])


def test_string_option_with_default(fzf):
    @click.command("cli", help="cli help")
    @click.option("-s", default="some value", help="string option")
    def cli(_):
        pass

    fzf.should_return(["cli help -s some value"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_callbacks(fuzzy.commands, [cli, cli])
    assert_same_callbacks(choices, [cli])


@pytest.mark.parametrize("default", [True, False])
def test_boolean_flag(fzf, default):
    @click.command("cli", help="cli help")
    @click.option("-f", is_flag=True, default=default)
    def cli(_):
        pass

    fzf.should_return([f"cli help -f {str(default)}"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_callbacks(fuzzy.commands, [cli, cli])
    assert_same_fuzzies(fuzzy.commands, ["cli help -f True", "cli help -f False"])
    assert_same_fuzzies(choices, [f"cli help -f {str(default)}"])


def test_choice_option(fzf):
    @click.command("cli", help="cli help")
    @click.option("-m", type=click.Choice(["foo", "bar", "baz"]))
    def cli(_):
        pass

    fzf.should_return(["cli help -m foo"])

    fuzzy = FuzzyClick(cli, fzf=fzf)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_fuzzies(fuzzy.commands, ["cli help -m <none>", "cli help -m foo", "cli help -m bar", "cli help -m baz"])
    assert_same_callbacks(fuzzy.commands, [cli, cli, cli])
    assert_same_callbacks(choices, [cli])


def test_input_missing(fzf, input_function):
    @click.command("cli", help="cli help")
    @click.option("-m", type=str, default="default")
    def cli(_):
        pass

    fzf.should_return(["cli help -m <input>"])
    input_function.should_return("some value")

    fuzzy = FuzzyClick(cli, fzf=fzf, input_function=input_function)
    choices = fuzzy.choose(Context(cli, resilient_parsing=True))

    assert_same_fuzzies(fuzzy.commands, ["cli help -m some value", "cli help -m default"])
    assert_same_callbacks(fuzzy.commands, [cli])
    assert_same_fuzzies(choices, ["cli help -m some value"])
    assert_same_callbacks(choices, [cli])


def assert_same_callbacks(commands1: list[Command], commands2: list[Command]):
    for c1, c2 in zip(commands1, commands2):
        assert_same_callback(c1, c2)


def assert_same_callback(command1: Command, command2: Command):
    assert command1.callback == command2.callback


def assert_same_fuzzies(commands: list[Command], fuzzies: list[str]):
    assert [to_fuzzy(c) for c in commands] == fuzzies


def assert_same_fuzzy(command1: Command, fuzzy: str):
    assert to_fuzzy(command1) == fuzzy
