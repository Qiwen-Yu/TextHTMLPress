# import pytest
# from click.testing import CliRunner
from TextHTMLPress.generator import Generator, get_title
from pathlib import Path


# test the CLI functionality through
# def test_ssg():
#     runner = CliRunner()
#     result = runner.invoke(__main__.main, ['-h'])
#     assert result.exit_code == 0


def test_title():
    filepath = Path("./inputs/Silver_Blaze.txt")
    title = get_title(filepath)
    assert title == "Silver Blaze"

    filepath = Path("./inputs/example1.md")
    title = get_title(filepath)
    assert title == "Zen"


def test_md():
    inp = Path("./inputs/test1.txt")
    output = Path("../dist")
    stylesheet = ""
    lang = "en-CA"
    g = Generator(inp, output, stylesheet, lang)
    html_md = g.generate_a_html(inp)
    assert html_md == """<!DOCTYPE html><html lang="en-CA"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Silver Blaze</title></head><body><h1>Silver Blaze</h1><p>
I am afraid, Watson, that I shall have to go</p></body></html>"""
