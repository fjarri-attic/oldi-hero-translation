# Translation Workflow & Style Conventions

Working notes for translating Genry Lion Oldi's «Герой должен быть один» ("The Hero Must Be Alone") from Russian to English. Read this file at the start of every session before continuing the translation.

## Files

- The folder `ru` contains the original text split into chapters (in Markdown format).
- The folder `en` contains the translation with the file names matching those in the `ru` folder.
- `GLOSSARY.md` — names, places, epithets, and terms with their settled English renderings. Update this whenever a new proper noun or term is introduced, or a existing one is corrected.
- `CONVENTIONS.md` — this file.

Ignore other files unless specifically instructed.

## Workflow

- Only ever work on a single file from the `ru` folder unless specifically instructed. When one of those is translated, put the translation in the file with the same name in the `en` folder.
- Commit granularity: **one scene/beat per commit** (a natural narrative chunk — a few paragraphs to a page — not single paragraphs, not full chapters).
- Commit message style: short, matching existing history (e.g. "New paragraphs", "Corrections"). No need for elaborate messages.
- **Commit locally only** — never `git push` to `origin` unless explicitly asked.
- Only stage/commit the contents of `en` folder (and `GLOSSARY.md` / `CONVENTIONS.md` when they change). Never add other files to git.
- When starting a new session on this project, check `git log` and the last file in the `en` folder (alphabetically, since they have enumerated prefixes) to find exactly where the translation left off before continuing.

## Translator queries vs. footnotes — two different bracket styles

- **Open questions for the user** (word choice uncertain, needs research, ambiguous in source): bold bracket note right after the relevant word/phrase, e.g. `**[a better word? waterboarded?]**`. These are flags for discussion, not meant to survive into a final draft.
- **Footnotes** (explanatory content that should actually accompany the word): Markdown style - a reference anchor near the word (without a space), and the actual footnote under the paragpaph. E.g. `... lawagetas[^9] ...` in a paragraph, and `[^9] A Mycenaean military title - leader of the host, second in rank only to the wanax]` after the paragraph.
- Once a translator query is resolved, either delete the bracket note or convert it into a proper footnote — don't leave stale open questions sitting in finished text.

## Footnote policy going forward

- **All Classical Greek / Mycenaean terminology gets a footnote by default** — this matches the style of the original book, which glosses specialist terms for the reader.
- The original book has its own numbered endnote system: markers like `[13]`, `[14]` in the running text correspond to a "Примечания" (Notes) section near the end of `hero_ru.md` (starting around line 13884). When we eventually integrate with that system, our new footnotes will need numbers of their own and an entry in the notes section.
- For now, don't try to slot new footnotes into that numbered system — just use the inline square-bracket style described above.
- Before adding a footnote, check whether the term already has one earlier in the text (the book's own numbered endnotes, or one we added) - footnote/gloss on **first occurrence only**, then use the term plain afterward. This matters a lot for recurring terms like "lawagetas," which shows up dozens of times.
- When the original book already has its own endnote for a term (see «Примечания» in `hero_ru.md`), prefer the author's own definition over inventing a more elaborate scholarly one - it keeps the translation's register matching the original's.

## Style notes

- Register: literary, matching Oldi's long, clause-heavy sentences, semicolons, ellipses, and mid-sentence dashes. Translate fluently rather than word-for-word, but preserve sentence rhythm and structure where possible.
- Dialogue: Russian em-dash dialogue markers (`— ...`) become standard English quotation marks in translation.
- Chapter/section structure borrows Greek tragedy vocabulary from the original (Parodos, epeisodion, etc.) — keep these terms transliterated, not translated.
- Character epithets that pair a name with a descriptive word (e.g. «Мойра Атропос» → "Atropos the Moira", «Метида-Мысль» → "Metis-Thought") should preserve that paired/disambiguating presentation — this is a deliberate authorial device, not decoration to be dropped.
- See `GLOSSARY.md` for settled names, places, and terms. Check it before translating a proper noun that may have appeared before.
