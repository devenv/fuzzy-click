from pytest import fixture


@fixture
def fzf():
    class FzfSpy:
        prompted = []
        returns = []

        def prompt(self, options: list[str], _: str):
            self.prompted.extend(options)
            return self.returns

        def should_return(self, choices: list[str]):
            self.returns = choices

    return FzfSpy()
