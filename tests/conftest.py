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


@fixture
def input_function():
    class PromptStub:
        prompted = []
        returns = ""

        def __call__(self, prompt: str):
            self.prompted.append(prompt)
            return self.returns

        def should_return(self, prompt: str):
            self.returns = prompt

    return PromptStub()
