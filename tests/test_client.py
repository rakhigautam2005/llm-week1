from types import SimpleNamespace

from llm.client import ask


class FakeCompletions:
    def __init__(self):
        self.last_kwargs = {}

    def create(self, **kwargs):
        self.last_kwargs = kwargs  # remember what ask() sent
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content="A token is a chunk of text."))
            ],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=8),
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_ask_returns_text_tokens_and_cost():
    result = ask("What is a token?", "gpt-4o-mini", client=FakeClient())
    assert result.text == "A token is a chunk of text."
    assert result.input_tokens == 12
    assert result.output_tokens == 8
    assert result.cost_usd > 0


def test_ask_sends_only_chosen_settings():
    client = FakeClient()
    ask("hi", "gpt-4o-mini", client=client)
    assert "temperature" not in client.chat.completions.last_kwargs

    ask("hi", "gpt-4o-mini", client=client, temperature=0.0, reasoning_effort="high")
    sent = client.chat.completions.last_kwargs
    assert sent["temperature"] == 0.0
    assert sent["reasoning_effort"] == "high"
