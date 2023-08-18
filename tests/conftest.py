from pytest import fixture


@fixture
def fzf():
    class FzfSpy:
        prompted = []
        returns = []

        def prompt(self, choices: list[str]):
            self.prompted.extend(choices)
            return self.returns

        def should_return(self, choices: list[str]):
            self.returns = choices

    return FzfSpy()
