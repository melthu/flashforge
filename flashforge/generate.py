import os
import json
from flashforge.models import Flashcard

MOCK_CARDS_JSON = [
    {"question": "What is the time complexity of binary search?", "answer": "O(log n)"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is a deadlock?", "answer": "A state where two or more processes are waiting on each other indefinitely"},
    {"question": "What is the difference between a stack and a queue?", "answer": "A stack is LIFO (last in, first out); a queue is FIFO (first in, first out)"},
    {"question": "What does HTTP stand for?", "answer": "HyperText Transfer Protocol"},
    {"question": "What is memoization?", "answer": "Caching the results of expensive function calls to avoid recomputation"},
    {"question": "What is a hash collision?", "answer": "When two different keys hash to the same index in a hash table"},
]


def generate_mock() -> list[Flashcard]:
    """Return hardcoded flashcards for testing without an API key."""
    return [Flashcard(**card) for card in MOCK_CARDS_JSON]


def _generate_from_api(text: str) -> list[Flashcard]:
    """Real implementation — fill in once API key and prompt are ready."""
    raise NotImplementedError("API key and prompt not configured yet")


def generate_cards(text: str, mock: bool = False) -> list[Flashcard]:
    """Entry point for card generation. Uses mock if --mock flag is set or no API key found."""
    if mock or not os.getenv("ANTHROPIC_API_KEY"):
        print("[mock mode] Skipping API call — returning mock flashcards")
        return generate_mock()
    return _generate_from_api(text)
