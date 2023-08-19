from itertools import product
from typing import Iterator, Optional

from click import Choice, Command, Context, Group, Option, Parameter
from click.types import BoolParamType, StringParamType
from pyfzf import FzfPrompt

from .utils import to_fuzzy


class FuzzyClick:
    def __init__(self, root: Command, fzf: Optional[FzfPrompt] = None):
        self.fzf = fzf or FzfPrompt()
        self.root = root
        self.commands: list[Command] = list(self._traverse(root))

    def choose(self, ctx: Context) -> list[Command]:
        fuzzy_to_commands = {to_fuzzy(command): command for command in self.commands}
        choices = self.fzf.prompt(choices=fuzzy_to_commands.keys())

        for choice in choices:
            if choice not in fuzzy_to_commands:
                raise ValueError(f"Invalid choice: {choice}, expected one of {fuzzy_to_commands.keys()}")

        self.root.parse_args(ctx, [])

        return [fuzzy_to_commands[choice] for choice in choices]

    def _traverse(self, command: Command) -> Iterator[Command]:
        if isinstance(command, Group):
            for subcommand in command.commands.values():
                yield from self._traverse(subcommand)
        elif isinstance(command, Command):
            yield from self._explode(command)

    def _explode(self, command: Command) -> Iterator[Command]:
        exploded_params: list[list[Parameter]] = list(list(self._explode_param(param)) for param in command.params)
        combos: list[list[Parameter]] = list(product(*exploded_params))
        for combo in combos:
            combo: list[Parameter] = list(combo)
            yield Command(
                command.name,
                help=command.help,
                params=combo,
                callback=command.callback,
                context_settings=command.context_settings,
            )

    def _explode_param(self, param: Parameter) -> Iterator[Parameter]:
        if isinstance(param, Option):
            if issubclass(param.type.__class__, BoolParamType):
                yield Option(param_decls=param.opts, type=param.type, default=True)
                yield Option(param_decls=param.opts, type=param.type, default=False)

            if issubclass(param.type.__class__, StringParamType):
                yield Option(param_decls=param.opts, type=param.type, default="<input>")
                yield Option(param_decls=param.opts, type=param.type, default=param.default)

            if issubclass(param.type.__class__, Choice):
                if not param.required:
                    yield Option(param_decls=param.opts, type=param.type, default="<none>")
                choices = param.type.choices  # type: ignore
                for choice in choices:
                    yield Option(param_decls=param.opts, type=param.type, default=choice)
        else:
            raise NotImplementedError
