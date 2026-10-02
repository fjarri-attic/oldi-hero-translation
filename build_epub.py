#!/usr/bin/env python3
"""
build_epub.py — merge chapter HTML files (from convert_chapters.py) into an EPUB.

Library: EbookLib (https://github.com/aerkalov/ebooklib) — a pure-Python
EPUB2/EPUB3 reader/writer, actively maintained, and the de facto standard for
this in Python (nothing else comes close in adoption). It builds books out
of ``EpubHtml`` items plus a spine (reading order) and a toc (table of
contents); it does not parse HTML itself, so a light HTML parse of each
chapter (BeautifulSoup) is used here to pull out the <title>, the <body>
content, and the heading structure.

What this script does
----------------------
1. Reads every chapter .html file (as produced by convert_chapters.py) from
   the input directory, in filename order.
2. Assigns an id="..." to any heading that doesn't already have one, so
   individual sections can be deep-linked.
3. Builds a NESTED table of contents from each chapter's heading levels
   (h1 > h2 > h3 ...), not just a flat list of chapters — this is what makes
   your book's nested-heading structure show up as a real nested TOC in
   e-readers, not just a flat chapter list.
4. Packages everything — chapters, an optional stylesheet, and metadata —
   into a single .epub with EbookLib.

Usage
-----
    python build_epub.py chapters_html/ book.epub \\
        --title "The Long Crossing" --author "Jane Translator" --lang en \\
        --css style.css

Dependencies
------------
    pip install ebooklib beautifulsoup4
"""

from __future__ import annotations

import argparse
import re
import sys
import uuid
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub


# ---------------------------------------------------------------------------
# Heading ids + nested TOC
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^h[1-6]$")


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text) or "section"


def assign_heading_ids(soup: BeautifulSoup, used_ids: set[str]) -> None:
    """Give every heading a stable id, without clobbering ids you set by hand."""
    for heading in soup.find_all(_HEADING_RE):
        if not heading.get("id"):
            base = slugify(heading.get_text())
            candidate, n = base, 2
            while candidate in used_ids:
                candidate = f"{base}-{n}"
                n += 1
            heading["id"] = candidate
        used_ids.add(heading["id"])


def build_chapter_toc(soup: BeautifulSoup, chapter: epub.EpubHtml) -> list:
    """
    Turn one chapter's h1..h6 tags into a nested toc fragment for EbookLib.

    EbookLib expects nesting as (link_or_section, [children]) tuples; a
    heading becomes a child of the most recently seen heading of a shallower
    level. The first heading in the file is linked straight to the chapter
    file (no #fragment) so it also serves as the "open this chapter" entry.
    """
    headings = soup.find_all(_HEADING_RE)
    if not headings:
        return [chapter]  # nothing to nest on; just link the whole file

    root: list = []
    # stack of (level, children_list) currently open
    stack: list[tuple[int, list]] = [(0, root)]

    for i, heading in enumerate(headings):
        level = int(heading.name[1])
        title = heading.get_text(strip=True)
        href = chapter.file_name if i == 0 else f"{chapter.file_name}#{heading['id']}"
        link = epub.Link(href, title, heading["id"] or f"{chapter.file_name}-{i}")

        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_children = stack[-1][1]

        node_children: list = []
        parent_children.append((link, node_children))
        stack.append((level, node_children))

    return root


# ---------------------------------------------------------------------------
# Building the book
# ---------------------------------------------------------------------------

def build_epub(
    input_dir: Path,
    output_path: Path,
    *,
    title: str,
    author: str,
    lang: str,
    css_path: Path | None,
    identifier: str | None,
) -> None:
    book = epub.EpubBook()
    book.set_identifier(identifier or f"urn:uuid:{uuid.uuid4()}")
    book.set_title(title)
    book.set_language(lang)
    if author:
        book.add_author(author)

    css_item = None
    if css_path is not None:
        css_item = epub.EpubItem(
            uid="style",
            file_name=f"style/{css_path.name}",
            media_type="text/css",
            content=css_path.read_bytes(),
        )
        book.add_item(css_item)

    used_ids: set[str] = set()
    spine: list = ["nav"]
    toc: list = []

    for i, src in enumerate(sorted(input_dir.glob("*.html")), start=1):
        soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
        assign_heading_ids(soup, used_ids)

        body = soup.body
        body_html = body.decode_contents() if body else str(soup)
        page_title = soup.title.get_text() if soup.title else src.stem

        chapter = epub.EpubHtml(
            title=page_title,
            file_name=f"{src.stem}.xhtml",
            lang=lang,
        )
        chapter.content = body_html
        if css_item is not None:
            chapter.add_item(css_item)

        book.add_item(chapter)
        spine.append(chapter)
        toc.extend(build_chapter_toc(soup, chapter))

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    epub.write_epub(str(output_path), book)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge chapter HTML files into an EPUB.")
    parser.add_argument("input_dir", type=Path, help="Directory of chapter .html files")
    parser.add_argument("output_path", type=Path, help="Path to write the .epub to")
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--css", type=Path, default=None, help="Stylesheet to embed")
    parser.add_argument("--identifier", default=None, help="Book UID (default: random uuid)")
    args = parser.parse_args(argv)

    if not args.input_dir.is_dir():
        parser.error(f"{args.input_dir} is not a directory")

    build_epub(
        args.input_dir,
        args.output_path,
        title=args.title,
        author=args.author,
        lang=args.lang,
        css_path=args.css,
        identifier=args.identifier,
    )
    print(f"wrote {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
