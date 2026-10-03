import argparse
import re
import sys
import uuid
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub


_HEADING_RE = re.compile(r"^h[1-6]$")


def assign_heading_ids(soup: BeautifulSoup) -> None:
    for heading in soup.find_all(_HEADING_RE):
        if not heading.get("id"):
            heading["id"] = f"heading-{uuid.uuid4().hex}"


def build_chapter_toc(soup: BeautifulSoup, chapter: epub.EpubHtml) -> list:
    headings = soup.find_all(_HEADING_RE)

    toc = []
    for heading in headings:
        level = int(heading.name[1])
        title = " ".join(heading.find_all(string=True, recursive=False))
        href = f"{chapter.file_name}#{heading['id']}"
        link = epub.Link(href, title, heading["id"])
        toc.append((level, link))

    return toc


def build_toc(toc_flat: list[tuple[int, epub.Link]]):
    toc = []
    current_level = 2
    stack = [toc]
    for (level, link) in toc_flat[1:]:
        if level == current_level:
            pass
        elif level == current_level + 1:
            stack.append(stack[-1][-1][1])
        elif level < current_level:
            for _ in range(current_level - level):
                stack.pop()
        else:
            raise RuntimeError(f"Unexpected jump of the ToC level: {current_level} to {level}")

        current_level = level
        stack[-1].append((link, []))

    return clean_toc(toc)


def clean_toc(toc):
    new_toc = []
    for item in toc:
        if isinstance(item, epub.Link):
            new_toc.append(item)
        else:
            if len(item[1]) == 0:
                new_toc.append(item[0])
            else:
                new_toc.append([item[0], clean_toc(item[1])])

    return new_toc


def build_epub(
    input_dir: Path,
    output_path: Path,
    title: str,
    author: str,
    lang: str,
    css_path: Path,
    cover_path: Path,
) -> None:
    identifier = f"urn:uuid:{uuid.uuid4()}"

    css_item = None
    css_item = epub.EpubItem(
        uid="style",
        file_name=f"style/{css_path.name}",
        media_type="text/css",
        content=css_path.read_bytes(),
    )

    chapter_paths = sorted(input_dir.glob("*.html"))

    toc_flat = []
    chapters = []
    for chapter_path in chapter_paths:
        html = BeautifulSoup(chapter_path.read_text(encoding="utf-8"), "html.parser")
        assign_heading_ids(html)

        chapter = epub.EpubHtml(
            title=chapter_path.stem,
            file_name=f"{chapter_path.stem}.xhtml",
            lang=lang,
        )
        chapter.content = html.body.decode_contents()
        chapter.add_item(css_item)

        toc_flat.extend(build_chapter_toc(html, chapter))
        chapters.append(chapter)

    toc = build_toc(toc_flat)

    # Build the book

    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(lang)
    book.set_cover(cover_path.name, cover_path.read_bytes())

    book.add_author(author)
    book.add_item(css_item)

    # Put front matter before the ToC
    book.spine = [chapters[0]] + ["nav"] + chapters[1:]

    for chapter in chapters:
        book.add_item(chapter)

    book.toc = toc

    # Display ToC without numbers on the items
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content="nav ol { list-style-type: none; }",
    )
    book.add_item(nav_css)

    nav = epub.EpubNav()
    nav.title = "Contents"
    nav.add_item(nav_css)
    book.add_item(nav)

    book.add_item(epub.EpubNcx())

    epub.write_epub(str(output_path), book)


def main() -> int:
    """
    - make sure footnotes are not visible at the end of chapters
    - make an actual cover
    - build chapter IDs based on ToC instead of just random UUIDs
    """

    input_dir = Path("html")
    output_path = Path("book.epub")
    title = "A Hero Stands Alone"
    author = "Henty Lion Oldie"
    lang = "en"
    css_path = Path("assets/style.css")
    cover_path = Path("assets/cover.jpg")

    build_epub(
        input_dir=input_dir,
        output_path=output_path,
        title=title,
        author=author,
        lang=lang,
        css_path=css_path,
        cover_path=cover_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
