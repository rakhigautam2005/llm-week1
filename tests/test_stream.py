from types import SimpleNamespace

from llm.stream import stream_answer


def chunk(text=None, usage=None):
    choices = [SimpleNamespace(delta=SimpleNamespace(content=text))] if text is not None else []
    return SimpleNamespace(choices=choices, usage=usage)


class FakeCompletions:
    def create(self, **kwargs):
        assert kwargs["stream"] is True
        return iter(
            [
                chunk("Hel"),
                chunk("lo"),
                chunk(" world"),
                chunk(usage=SimpleNamespace(prompt_tokens=5, completion_tokens=3)),
            ]
        )


class FakeClient:
    chat = SimpleNamespace(completions=FakeCompletions())


def test_stream_yields_pieces_in_order():
    pieces = list(stream_answer("hi", "gpt-4o-mini", client=FakeClient()))
    assert pieces == ["Hel", "lo", " world"]
    assert "".join(pieces) == "Hello world"
