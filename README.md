# Fuzzy Click

## What?

Given a click root command `FuzzyClick(root).choose()` will generate all the permutation of commands and their parameters, and show `fzf` to choose one (or multiple).

If a command permutation that was chosen has a string parameter - a text input will be shown (WIP).

## Demo

```python
import click
from devenv.fuzzy_click import FuzzyClick

@click.group("cmd", help="cmd help")
def cmd():
    pass

@cmd.command("sub", help="sub help")
def sub():
    pass

FuzzyClick(cmd).choose(ctx)
```

will show fzf and return a list of commands that you can `command.invoke()`.

![fzf options](relative%20../../_static/demo.png?raw=true "FZF options")
