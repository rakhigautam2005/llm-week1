from types import SimpleNamespace

from llm.client import ask


class FakeCompletions:
    def create(self, model, messages):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content="A token is a chunk of text."))
            ],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=8),
        )


class FakeClient:
    chat = SimpleNamespace(completions=FakeCompletions())


def test_ask_returns_text_tokens_and_cost():
    result = ask("What is a token?", "gpt-4o-mini", client=FakeClient())
    assert result.text == "A token is a chunk of text."
    assert result.input_tokens == 12
    assert result.output_tokens == 8
    assert result.cost_usd > 0
