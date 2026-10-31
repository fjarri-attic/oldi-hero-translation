"""
Markdown dialect
-----------------

1. Headings: ``#`` .. ``######``, nest by level as usual.

2. Fenced containers, for block-level custom formatting::

       ::: epigraph
       *"It was the best of times."*

       — Someone Famous
       :::

   renders as ``<div class="epigraph">...</div>``. Multiple classes and full
   attributes are supported too::

       ::: {.scene-break #sb1}
       :::

   -> ``<div id="sb1" class="scene-break"></div>``

3. A shortcut for single-paragraph containers::

       {.dedication}
       For my cat.

   -> ``<p class="dedication">For my cat.</p>``

4. Bracketed spans, for inline custom formatting::

       Here is a [special phrase]{.smallcaps}.

   -> ``<span class="smallcaps">special phrase</span>``

5. Footnotes. Standard Markdown syntax can be used, but that will render the footnotes
   at the end of each chapter (since we usually don't have a book in a single file).
   So instead we do the following. In a chapter::

       Here is a claim that needs backing up.[\\*](#fn-src){.noteref}

   Then in a separate footnotes chapter:

       {#fn-src .footnote}
       Cited from the 1962 edition, page 40.

   The hyperlink (and the hyperlink back from the footnote) are added in post-processing.

Everything else is standard Markdown.

"""

import argparse
import html
import sys
import shutil
from pathlib import Path
import textwrap

from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.attrs.parse import parse as parse_attrs
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.footnote import footnote_plugin


def _render_container(self, tokens, idx, options, env):  # type: ignore[no-untyped-def]
    """
    Turn ``::: <info>`` / ``::: {<attrs>}`` into ``<div ...>``.

    ``<info>`` is treated as one or more space-separated class names
    (``::: epigraph`` or ``::: epigraph highlight``). If it starts with
    ``{``, it's parsed with the same attribute mini-language used for
    bracketed spans and block attributes, so ids and arbitrary key=value
    attributes are also available (``::: {.scene-break #sb1}``).
    """
    token = tokens[idx]
    if token.nesting == 1:  # opening fence
        info = token.info.strip()
        if info.startswith("{"):
            _, attrs = parse_attrs(info)
        else:
            attrs = {"class": info} if info else {}
        for key, value in attrs.items():
            if key == "class":
                token.attrJoin("class", value)
            else:
                token.attrSet(key, value)
        return "<div" + self.renderAttrs(token) + ">\n"
    return "</div>\n"


def build_markdown_parser() -> MarkdownIt:
    """Construct the Markdown parser used for every chapter file."""
    md_parser = (
        MarkdownIt("commonmark", {"typographer": True})
        .enable(["replacements", "smartquotes"])
        .enable("table")
        .use(
            container_plugin,
            name="container",
            validate=lambda params, *args: True,
            render=_render_container,
        )
        .use(attrs_plugin, spans=True)  # enables [text]{.class} bracketed spans
        .use(attrs_block_plugin)        # enables a lone {.class} line before a block
        .use(footnote_plugin)           # enables [\*](#fn-name){.noteref} / [^name]: ... footnotes
    )
    return md_parser


def convert_md_to_html(md_parser: MarkdownIt, style_path: Path, src: Path, dst: Path) -> None:
    PAGE_TEMPLATE = textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="{style_path}">
        </head>
        <body>
        {body}
        </body>
        </html>
    """).strip()

    text = src.read_text(encoding="utf-8")
    body_html = md_parser.render(text).strip()
    page = PAGE_TEMPLATE.format(body=body_html, style_path=style_path)
    dst.write_text(page, encoding="utf-8")


def convert_directory_md_to_html(style_path: Path, markdown_dir_path: Path, html_dir_path: Path) -> list[Path]:
    if not markdown_dir_path.is_dir():
        raise RuntimeError(f"{markdown_dir_path} is not a directory")

    md_parser = build_markdown_parser()

    if html_dir_path.exists():
        if not html_dir_path.is_dir():
            raise RuntimeError(f"{html_dir_path} is not a directory")
        for src in html_dir_path.glob("*.*"):
            src.unlink()
    else:
        html_dir_path.mkdir(parents=True)

    ref_style_path = style_path.relative_to(html_dir_path, walk_up=True)

    for src in sorted(markdown_dir_path.glob("*.md")):
        dst = html_dir_path / (src.stem + ".html")
        convert_md_to_html(md_parser, ref_style_path, src, dst)


def main():
    markdown_dir_path = Path("en")
    html_dir_path = Path("html")
    style_path = Path("assets/style.css")

    convert_directory_md_to_html(style_path, markdown_dir_path, html_dir_path)

if __name__ == "__main__":
    main()
