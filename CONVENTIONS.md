# Translation Workflow & Style Conventions

Working notes for translating Genry Lion Oldi's «Герой должен быть один» ("The Hero Must Be Alone") from Russian to English. Read this file at the start of every session before continuing the translation.

## Files

- The folder `ru` contains the original text split into chapters (in Markdown format).
- The folder `en` contains the translation with the file names matching those in the `ru` folder.
- `GLOSSARY.md` --- names, places, epithets, and terms with their settled English renderings. Update this whenever a new proper noun or term is introduced, or a existing one is corrected.
- `CONVENTIONS.md` --- this file.

Ignore other files unless specifically instructed.

## Workflow

Don't make commits - I will handle it. Change files only when specifically instructed. When we are working on a chapter, avoid looking into files other than the chapter itself, the glossary, and the conventions, unless necessary to check for consistency.

## Footnotes

- **Footnotes** (explanatory content that should actually accompany the word): Markdown style --- a reference anchor near the word (without a space), and the actual footnote under the paragpaph. E.g. `... lawagetas[^9] ...` in a paragraph, and `[^9]: A Mycenaean military title --- leader of the host, second in rank only to the wanax]` after the paragraph.
- The original book has its own numbered endnote system: markers like `[13]`, `[14]` in the running text correspond to a "Примечания" (Notes) section (placed in `ru/131_footnotes.md`). These will be translated and converted to footnotes.
- Don't add new footnotes yourself. If some term is used by the authors without a footnote, we will keep at as is.

## Style notes

- Register: literary, matching Oldi's long, clause-heavy sentences, semicolons, ellipses, and mid-sentence dashes. Translate fluently rather than word-for-word, but preserve sentence rhythm and structure where possible.
- Dialogue: Russian em-dash dialogue markers (`— ...`) become standard English quotation marks in translation.
- Internal thoughts (rendered in quotes in Russian) are rendered in quotes like the direct speech in English.
- All-caps words/sentences are italicized in the translation (using the Markdown syntax enclosing them in single asterisks)
- Chapter/section structure borrows Greek tragedy vocabulary from the original (Parodos, epeisodion, etc.) --- keep these terms transliterated, not translated.
- Character epithets that pair a name with a descriptive word (e.g. «Мойра Атропос» → "Atropos the Moira", «Метида-Мысль» → "Metis-Thought") should preserve that paired/disambiguating presentation --- this is a deliberate authorial device, not decoration to be dropped.
- See `GLOSSARY.md` for settled names, places, and terms. Check it before translating a proper noun that may have appeared before.
