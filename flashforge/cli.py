import argparse
from datetime import datetime
from rich.table import Table
from rich.console import Console
from flashforge import generate, review, storage
from flashforge.ingest import ingest_directory
from flashforge.models import Deck


def main():
    parser = argparse.ArgumentParser(prog="flashforge")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate a deck from a directory of notes")
    gen.add_argument("--dir", required=True, help="Directory containing note files")
    gen.add_argument("--name", required=True, help="Name for the saved deck")
    gen.add_argument("--mock", action="store_true",
                     help="Skip API call and use mock flashcards (for testing)")

    rev = sub.add_parser("review", help="Review a saved deck")
    rev.add_argument("name", help="Name of the deck to review")

    sub.add_parser("list", help="Show all saved decks")

    args = parser.parse_args()

    if args.command == "generate":
        text = ingest_directory(args.dir)
        cards = generate.generate_cards(text, mock=args.mock)
        deck = Deck(
            name=args.name,
            cards=cards,
            created_at=datetime.now().isoformat(timespec="seconds"),
            source_dir=args.dir,
        )
        storage.save_deck(deck)
        print(f"Saved deck '{args.name}' with {len(cards)} cards.")

    elif args.command == "review":
        deck = storage.load_deck(args.name)
        review.run_review(deck)

    elif args.command == "list":
        decks = storage.list_decks()
        if not decks:
            print("No decks found. Run 'flashforge generate' to create one.")
            return
        console = Console()
        table = Table(title="Saved Decks")
        table.add_column("Name", style="bold cyan")
        table.add_column("Cards", justify="right")
        table.add_column("Created At")
        table.add_column("Source Dir")
        for deck in decks:
            table.add_row(deck.name, str(len(deck.cards)), deck.created_at, deck.source_dir)
        console.print(table)


if __name__ == "__main__":
    main()
