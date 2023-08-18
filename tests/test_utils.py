from click import Command, Option

from devenv.fuzzy_click.utils import describe_param, param_to_decl, to_fuzzy


def test_to_fuzzy():
    assert to_fuzzy(Command("cli", help="cli help")) == "cli help"


def test_describe_param():
    assert describe_param(Option(["-p"])) == "-p <input>"
    assert describe_param(Option(["-p"], default="value")) == "-p value"


def test_param_to_decl():
    assert param_to_decl(Option(["-p"])) == "-p"
