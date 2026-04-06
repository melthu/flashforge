# FlashForge

CLI tool that generates flashcard decks from notes and lets you review them in the terminal.

## File structure

```
flashforge/
  models.py      # Flashcard and Deck dataclasses + JSON serialization
  storage.py     # Save/load decks to ~/.flashforge/
  ingest.py      # Reads .txt, .md, .pdf files from a directory
  generate.py    # Card generation (mock mode now; real API stubbed)
  review.py      # Keyboard-driven review loop (rich + readchar)
  cli.py         # argparse entry point
requirements.txt
pyproject.toml
```

## Setup

```bash
pip install .
# or with pipx for a global install:
pipx install .
```

## Commands

```bash
flashforge generate --dir ./notes/ --name <deck-name>   # generate a deck (uses mock if no API key)
flashforge generate --dir ./notes/ --name <deck-name> --mock  # force mock mode
flashforge review <deck-name>                           # review a deck (arrow keys, enter to flip, q to quit)
flashforge list                                         # show all saved decks
```

Decks are saved as JSON in `~/.flashforge/`.

## TODO

- [ ] Write the generation prompt and implement `_generate_from_api()` in `generate.py`
- [ ] Set `ANTHROPIC_API_KEY` env var — mock mode disables automatically once the key is present
- [ ] Model to use: `claude-haiku-4-5-20251001`, max 4096 tokens
