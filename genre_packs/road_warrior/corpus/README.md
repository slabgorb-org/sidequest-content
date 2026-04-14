# Road Warrior Corpus

Road Warrior's primary naming path is `word_list` (handles, road names, crew
nicknames). The language corpora in this directory are a secondary source:
the Markov name generator uses them when a world within Road Warrior needs
linguistic flavor grounded in a real-world language tradition.

## Files

| File | Purpose |
|------|---------|
| `english.txt` | English-language corpus for Markov name gen |
| `french.txt` | French corpus |
| `german.txt` | German corpus |
| `italian.txt` | Italian corpus |
| `japanese.txt` | Japanese corpus (romaji) |
| `portuguese.txt` | Portuguese corpus |
| `spanish.txt` | Spanish corpus |
| `swahili.txt` | Swahili corpus |
| `swedish.txt` | Swedish corpus |
| `thai_khmer.txt` | Thai / Khmer corpus |
| `reject_common.txt` | Shared reject list (common words the generator should never emit as names) |

## World-level overrides

A world inside Road Warrior can add its own corpora at
`worlds/<world>/corpus/` and those will override the pack-level files for
that world only.
