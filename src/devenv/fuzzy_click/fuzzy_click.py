from typing import Optional
from click import Command, Group
from pyfzf import FzfPrompt


class FuzzyClick:
    def __init__(self, root: Command, fzf: Optional[FzfPrompt] = None):
        self.fzf = fzf or FzfPrompt()
        self.fuzzy_to_commands = self._traverse(root)

    def choose(self) -> list[Command]:
        fuzzy_options = list(self.fuzzy_to_commands.keys())
        choices = self.fzf.prompt(fuzzy_options, "Choose a command: ")
        return [self.fuzzy_to_commands[choice] for choice in choices]

    def _traverse(self, command: Command) -> dict[str, Command]:
        if isinstance(command, Group):
            subcommands = {}
            for subcommand in command.commands.values():
                subcommands.update(self._traverse(subcommand))
            return {command.get_short_help_str(): command, **subcommands}
        else:
            return {command.get_short_help_str(): command}
