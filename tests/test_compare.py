from llm.compare import count_distinct, short


def test_count_distinct_ignores_case_and_spaces():
    assert count_distinct(["Brew", "brew ", "BREW"]) == 1
    assert count_distinct(["Brew", "Bean", "Brew"]) == 2


def test_short_keeps_tables_tidy():
    assert short("a | b") == "a / b"
    assert len(short("x" * 100)) == 60
