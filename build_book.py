#!/usr/bin/env python3
"""
convert_chapters.py — batch-convert Markdown chapter files to HTML.

Every ``*.md`` file in an input directory is converted to an HTML file of the
same name (``chapter03.md`` -> ``chapter03.html``) in an output directory.

Markdown dialect
-----------------
Parsing is done with markdown-it-py (a pure-Python, CommonMark-compliant
parser) plus two plugins from mdit-py-plugins, giving three extra pieces of
syntax on top of plain Markdown:

1. Headings, ``#`` .. ``######``, nest by level as usual — no change needed.

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

3. Bracketed spans, for inline custom formatting::

       Here is a [special phrase]{.smallcaps}.

   -> ``<span class="smallcaps">special phrase</span>``

   The same ``{...}`` attribute syntax can also be dropped on the line right
   before an ordinary paragraph or heading, to tag it without wrapping it in
   a div::

       {.dedication}
       For my cat.

   -> ``<p class="dedication">For my cat.</p>``

4. Footnotes, standard Markdown syntax::

       Here is a claim that needs backing up.[^src]

       [^src]: Cited from the 1962 edition, page 40.

   -> a superscript link at the call site and a collected list of footnotes
   at the end of the document, each with a backlink.

Everything else — plain paragraphs, emphasis, lists, blockquotes, tables —
is standard Markdown and needs no special instructions at all.

Usage
-----
    python convert_chapters.py <input_dir> <output_dir> [--css style.css] [--lang en]

Dependencies
------------
    pip install markdown-it-py mdit-py-plugins
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.attrs.parse import parse as parse_attrs
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.footnote import footnote_plugin


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------

def _validate_container(params: str, *_args: object) -> bool:
    """Accept a ``:::`` fence regardless of what follows it.

    The default behaviour of container_plugin only matches a fence against
    one fixed name (``::: warning`` only opens a container registered as
    "warning"). We want *any* name to work, so every fence is accepted here
    and the real parsing happens in ``_render_container`` below.
    """
    return True


def _render_container(self, tokens, idx, options, env):  # type: ignore[no-untyped-def]
    """Turn ``::: <info>`` / ``::: {<attrs>}`` into ``<div ...>``.

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


def build_parser() -> MarkdownIt:
    """Construct the Markdown parser used for every chapter file."""
    md = (
        MarkdownIt("commonmark", {"typographer": True})
        .enable(["replacements", "smartquotes"])
        .enable("table")
        .use(
            container_plugin,
            name="container",
            validate=_validate_container,
            render=_render_container,
        )
        .use(attrs_plugin, spans=True)   # enables [text]{.class} bracketed spans
        .use(attrs_block_plugin)         # enables a lone {.class} line before a block
        .use(footnote_plugin)            # enables [^name] / [^name]: ... footnotes
    )
    return md


# ---------------------------------------------------------------------------
# HTML document wrapping
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
{css_link}</head>
<body>
{body}</body>
</html>
"""


def wrap_page(body_html: str, title: str, lang: str, css: str | None) -> str:
    css_link = f'<link rel="stylesheet" href="{html.escape(css)}">\n' if css else ""
    return PAGE_TEMPLATE.format(
        lang=html.escape(lang),
        title=html.escape(title),
        css_link=css_link,
        body=body_html,
    )


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def convert_file(md: MarkdownIt, src: Path, dst: Path, *, lang: str, css: str | None) -> None:
    text = src.read_text(encoding="utf-8")
    body_html = md.render(text)
    page = wrap_page(body_html, title=src.stem, lang=lang, css=css)
    dst.write_text(page, encoding="utf-8")


def convert_directory(input_dir: Path, output_dir: Path, *, lang: str, css: str | None) -> list[Path]:
    md = build_parser()
    output_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for src in sorted(input_dir.glob("*.md")):
        dst = output_dir / (src.stem + ".html")
        convert_file(md, src, dst, lang=lang, css=css)
        written.append(dst)
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("input_dir", type=Path, help="Directory containing chapter .md files")
    parser.add_argument("output_dir", type=Path, help="Directory to write chapter .html files into")
    parser.add_argument("--css", default=None, help="Stylesheet href to link from each page")
    parser.add_argument("--lang", default="en", help="HTML lang attribute (default: en)")
    args = parser.parse_args(argv)

    if not args.input_dir.is_dir():
        parser.error(f"{args.input_dir} is not a directory")

    written = convert_directory(args.input_dir, args.output_dir, lang=args.lang, css=args.css)

    if not written:
        print(f"No .md files found in {args.input_dir}", file=sys.stderr)
        return 1

    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
