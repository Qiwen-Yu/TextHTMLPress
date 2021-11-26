# import pytest
# from click.testing import CliRunner
from TextHTMLPress import Generator, get_title, get_paragraphs
from pathlib import Path


# test the CLI functionality through
# def test_ssg():
#     runner = CliRunner()
#     result = runner.invoke(__main__.main, ['-h'])
#     assert result.exit_code == 0


def test_get_paragraphs() -> None:
    filepath = Path("./inputs/test1.txt")
    para = get_paragraphs(filepath)
    assert para == ["Silver Blaze", "\nI am afraid, Watson, that I shall have to go"]


def test_title() -> None:
    filepath = Path("./inputs/Silver_Blaze.txt")
    title = get_title(filepath)
    assert title == "Silver Blaze"

    filepath = Path("./inputs/example1.md")
    title = get_title(filepath)
    assert title == "Zen"


def test_md() -> None:
    inp = Path("./inputs/test1.txt")
    output = Path("../dist")
    stylesheet = ""
    lang = "en-CA"
    g = Generator(inp, output, stylesheet, lang)
    html_md = g.generate_a_html(inp)
    assert (
        html_md
        == """<!DOCTYPE html><html lang="en-CA"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Silver Blaze</title></head><body><h1>Silver Blaze</h1><p>
I am afraid, Watson, that I shall have to go</p></body></html>"""
    )


def test_generate_html_from_md() -> None:
    inp = Path("./inputs/example1.md")
    output = Path("./dist")
    expected_output_file = Path("./dist/example1.html")
    stylesheet = ""
    lang = "fr"
    g = Generator(inp, output, stylesheet, lang)
    g.parse_markdown(inp)
    g.generator_wrapper()
    assert expected_output_file.exists()

