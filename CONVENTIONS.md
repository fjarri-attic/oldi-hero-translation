# Translation Workflow & Style Conventions

Working notes for translating Genry Lion Oldi's «Герой должен быть один» ("The Hero Must Be Alone") from Russian to English. Read this file at the start of every session before continuing the translation.

## Files

- The folder `ru` contains the original text split into chapters (in Markdown format).
- The folder `en` contains the translation with the file names matching those in the `ru` folder.
- `GLOSSARY.md`---names, places, epithets, and terms with their settled English renderings. Update this whenever a new proper noun or term is introduced, or a existing one is corrected.
- `CONVENTIONS.md`---this file.

Ignore other files unless specifically instructed.

## Workflow

Don't make commits - I will handle it. Change files only when specifically instructed. When we are working on a chapter, avoid looking into files other than the chapter itself, the glossary, and the conventions, unless necessary to check for consistency.

## Formatting

- **Footnotes** (explanatory content that should actually accompany the word): Markdown style---a reference anchor near the word (without a space), and the actual footnote under the paragpaph. E.g. `... lawagetas[\*](#fn-9){.noteref} ...` in a paragraph, and `[^9]: A Mycenaean military title---leader of the host, second in rank only to the wanax.` after the paragraph.
- Thoughts are rendered as `[Character thoughts go here]{.thoughts}`.
- Em-dashes use `---` instead of a single unicode symbol. En-dashes use `--`. Ellipsis uses `...`.
- Em-dashes and en-dashes are closed (not separated with spaces from the surrounding text).
- Interrupted speech uses an em-dash and not an ellipsis ("rejoice, thou marked by Zeus, for---").
- Dialogue: Russian em-dash dialogue markers (`— ...`) become standard English quotation marks in translation.

## Style notes

- Register: literary, matching Oldi's long, clause-heavy sentences, semicolons, ellipses, and mid-sentence dashes. Translate fluently rather than word-for-word, but preserve sentence rhythm and structure where possible.
- All-caps words/sentences are italicized in the translation (using the Markdown syntax enclosing them in single asterisks)
- Chapter/section structure borrows Greek tragedy vocabulary from the original (Parodos, epeisodion, etc.)---keep these terms transliterated, not translated.
- Character epithets (in the original usually attached to a name with a hyphen, occasionally preceding it):
  * An epithet denoting a group the character belongs to is written in the end with the definite artice: "Мойра Атропос" -> "Atropos the Moira", "Медуза Горгона"/"Горгона Медуза" -> "Medusa the Gorgon".
  * An epithet denoting the geographical origin is written in the end with the definite article, and translated: "Ифит-Ойхаллиец"/"Ифит-ойхаллиец" -> "Iphitos the Oichalian", "Миртил-фиванец" -> "Myrtilos the Theban".
  * An epithet that is a common word and in the original is hyphenated, is written in the end with the definite article, capitalized, and translated: "Метида-мысль" -> "Metis the Thought".
  * An epithet that is an adjective and in the original is written before the name, is written before the name in English as well: "Трехтелая Геката" -> "Three-Formed Hekate".
  * An epithet that is a transliterated Greek word is written in the end, transliterated in English, without an article: "Гермес-Киллений" -> "Hermes Kyllenios", "Зевс-Бротолойгос" -> "Zeus Brotoloigos".
- See `GLOSSARY.md` for settled names, places, and terms. Check it before translating a proper noun that may have appeared before.
