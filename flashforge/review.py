import readchar
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from flashforge.models import Deck, Flashcard


def make_panel(card: Flashcard, flipped: bool, i: int, total: int) -> Panel:
    side = "Answer" if flipped else "Question"
    content = card.answer if flipped else card.question
    footer = "[dim]← prev   → next   enter flip   q quit[/dim]"
    body = Align.center(f"{content}\n\n{footer}", vertical="middle")
    return Panel(body, title=f"[bold]{side}[/bold]", subtitle=f"Card {i+1} of {total}")


def run_review(deck: Deck) -> None:
    deck.shuffle()
    i = 0
    flipped = False

    with Live(make_panel(deck.cards[i], flipped, i, len(deck.cards)),
              auto_refresh=False) as live:
        while True:
            key = readchar.readkey()
            if key == readchar.key.ENTER:
                flipped = not flipped
            elif key == readchar.key.RIGHT:
                i = (i + 1) % len(deck.cards)
                flipped = False
            elif key == readchar.key.LEFT:
                i = (i - 1) % len(deck.cards)
                flipped = False
            elif key == "q":
                break
            live.update(make_panel(deck.cards[i], flipped, i, len(deck.cards)))
            live.refresh()
