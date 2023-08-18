from click import Command, Parameter


def to_fuzzy(command: Command) -> str:
    help = command.get_short_help_str()
    params = [describe_param(param) for param in command.params]
    return f"{help} {' '.join(params)}".strip()


def describe_param(param: Parameter) -> str:
    name = param_to_decl(param)
    if param.default is not None:
        return f"{name} {param.default}"
    return f"{name} <input>"


def param_to_decl(param: Parameter) -> str:
    return f"-{param.human_readable_name}"
