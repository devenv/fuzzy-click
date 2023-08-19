# Fuzzy Click

## What?

Given a click root command `FuzzyClick(root).choose(ctx)` will generate all the permutation of commands and possible parameters, and show `fzf` search to choose one (or multiple) commands.

If a command permutation that was chosen has a string parameter - a text input will be shown.

## Demo

```python
import click
from devenv.fuzzy_click import FuzzyClick


@click.group("cmd", help="root cmd help")
def cmd():
    pass


@cmd.command("command", help="command help")
@click.option("-c", type=click.Choice(["foo", "bar"]))
@click.option("-s", type=str, default="default")
def choice():
    pass


FuzzyClick(cmd).choose(click.Context(cmd, resilient_parsing=True))
```

will show fzf and return a list of commands that you can `command.invoke(command.make_context(command.name, parent=ctx, args=[]))`.

![fzf options](relative%20../../_static/demo.png?raw=true "FZF options")

## Caveats

- Only boolean, choice, and strings are supported.
- Only basic functionality is supported (works for me), no fancy click stuff.
