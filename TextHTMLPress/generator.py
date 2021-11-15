import shutil
import sys
from pathlib import Path
from typing import Optional
from yattag import Doc
import click
from typing import List
import frontmatter
import markdown
import jinja2


class Generator:
    """Basic Generator to produce static html files from txt and Markdown files, taking input either a .txt file or a
    folder"""

    _in_path: Path
    _out_path: Path
    _stylesheet_url: str
    _lang: str
    # static variables
    DEFAULT_FILES = ("*.txt", "*.md")
    # a relative path
    DEFAULT_OUTPUT = Path.cwd() / "dist/"

    def __init__(
        self,
        in_path: Path,
        out_path: Optional[Path],
        stylesheet_url: Optional[str],
        lang: Optional[str],
    ):
        self._in_path = in_path
        if not out_path:
            self._out_path = self.DEFAULT_OUTPUT
        self._out_path = out_path
        if not stylesheet_url:
            self._stylesheet_url = ""
        self._stylesheet_url = stylesheet_url
        self._lang = lang

    def generator_wrapper(self) -> None:
        # remove old output folder and its contents
        if self._out_path.exists():
            shutil.rmtree(self._out_path)
        # make new output folder
        self._out_path.mkdir(parents=True, exist_ok=False)

        # different conditions file vs folder
        if self._in_path.is_file():
            # TODO: decide .txt or .md
            # get file extension
            file_ext = self._in_path.suffix
            if file_ext == ".txt":
                self.generate_a_file(self._in_path)
            if file_ext == ".md":
                self.parse_markdown(self._in_path)
        # find all .txt in
        if self._in_path.is_dir():
            # TODO: only for txt path, should be able to find path of txt, md or sub-folder
            for txt_path in self._in_path.glob(self.DEFAULT_FILES[0]):
                # TODO: recursively, call the function it self
                # TODO: call itself generator_wrapper()
                self.generate_a_file(txt_path)

            for md_path in self._in_path.glob(self.DEFAULT_FILES[1]):
                self.parse_markdown(md_path)

    def parse_markdown(self, filepath: Path) -> None:
        # prepare meta data
        filename = filepath.stem
        title = get_title(filepath)
        # open the MarkDown file
        post = frontmatter.load(filepath)
        date = post["date"]
        author = post["author"]
        content = post.content

        # html body
        html_body = markdown.markdown(content)

        # write html, generate a template string
        doc, tag, text, line = Doc().ttl()
        doc.asis("<!DOCTYPE html>")

        with tag("html"):
            # fix issue 6
            doc.attr(lang=self._lang)
            with tag("head"):
                doc.stag("meta", charset="utf-8")
                doc.stag(
                    "meta",
                    name="viewport",
                    content="width=device-width, initial-scale=1",
                )
                with tag("title"):
                    if title:
                        text(title)
                    else:
                        text(filename)
                if self._stylesheet_url:
                    doc.stag("link", rel="stylesheet", href=self._stylesheet_url)

            with tag("body"):
                if not title:
                    line("h1", title)
                line("h2", "{{author}}")
                line("h2", "{{date}}")
                line("p", "temp")
        # temp_html has meta and body as a string
        temp_html = doc.getvalue()
        # insert content to body
        html = temp_html.replace("<p>temp</p>", html_body)
        final_html = jinja2.Template(html).render(author=author, date=date)

        try:
            if self._out_path.is_dir():
                html_name = filename + ".html"
                final_path = self._out_path / html_name
                with final_path.open("w+", encoding="utf-8") as w_f:
                    w_f.write(final_html)
                    click.echo(
                        f"{filepath} was exported as .html file to {self._out_path} successfully"
                    )
        except OSError as e:
            click.echo(f"Can not write file to {self._out_path}")
            sys.exit(1)

    def generate_a_html(self, filepath: Path) -> str:
        """return a raw html in str format with content from the .txt file"""
        doc, tag, text, line = Doc().ttl()
        title = get_title(filepath)
        filename = filepath.stem
        doc.asis("<!DOCTYPE html>")

        with tag("html"):
            # fix issue 6
            doc.attr(lang=self._lang)
            with tag("head"):
                doc.stag("meta", charset="utf-8")
                doc.stag(
                    "meta",
                    name="viewport",
                    content="width=device-width, initial-scale=1",
                )
                with tag("title"):
                    if title:
                        text(title)
                    else:
                        text(filename)
                if self._stylesheet_url:
                    doc.stag("link", rel="stylesheet", href=self._stylesheet_url)
            with tag("body"):
                # a list of paragraphs
                ps = get_paragraphs(filepath)
                if title:
                    line("h1", title)
                    for p in ps[1:]:
                        line("p", p)
                else:
                    for p in ps:
                        line("p", p)

        return doc.getvalue()

    def write_a_file(self, raw_html: str, filepath: Path) -> None:
        """write file from raw_html as str"""
        filename = filepath.stem
        try:
            if self._out_path.is_dir():
                html_name = filename + ".html"
                final_path = self._out_path / html_name
                with final_path.open("w+", encoding="utf-8") as w_f:
                    w_f.write(raw_html)
                    click.echo(
                        f"{filepath} was exported as .html file to {self._out_path} successfully"
                    )
        except OSError as e:
            click.echo(f"Can not write file to {self._out_path}")
            sys.exit(1)

    def generate_a_file(self, filepath: Path) -> None:
        """
        :param filepath: must be the path of a .txt file.
        :return:
        """
        raw_html = self.generate_a_html(filepath)
        self.write_a_file(raw_html, filepath)


# helper function
def get_title(filepath: Path) -> str:
    """
    The title is defined by the first line and followed by two blank lines.
    Or by yaml frontmatter in MarkDown files.
    :param filepath: must be the path of a .txt file
    :return:
    """
    try:
        file_ext = filepath.suffix
        with filepath.open("r", encoding="utf-8") as f:
            if file_ext == ".txt":
                blank_lines = 2
                n = 0
                lines = f.read().splitlines()
                for line in lines[: blank_lines + 1]:
                    if not line.strip():
                        n += 1

                if n == blank_lines:
                    return lines[0]

            if file_ext == ".md":
                post = frontmatter.load(f)
                if not post["title"]:
                    return post["title"]
        return ""
    except OSError as e:
        click.echo(f"Can not open {filepath}")
        # fix issue 7
        sys.exit(1)


def get_paragraphs(filepath: Path) -> List[str]:
    try:
        file_ext = filepath.suffix
        with filepath.open("r", encoding="utf-8") as f:
            if file_ext == ".txt":
                # single blank line between paragraphs
                paragraphs = f.read().split("\n\n")
                return paragraphs
    except OSError as e:
        click.echo(f"Can not open {filepath}")
        # fix issue 7
        sys.exit(1)
