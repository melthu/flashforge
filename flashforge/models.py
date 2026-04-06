from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class Flashcard:
    question: str
    answer: str
    tag: Optional[str] = None


@dataclass
class Deck:
    name: str
    cards: list
    created_at: str
    source_dir: str

    def shuffle(self) -> None:
        import random
        random.shuffle(self.cards)

    def filter_by_tag(self, tag: str) -> list:
        return [c for c in self.cards if c.tag == tag]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "created_at": self.created_at,
            "source_dir": self.source_dir,
            "cards": [
                {"question": c.question, "answer": c.answer, "tag": c.tag}
                for c in self.cards
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        cards = [Flashcard(**card) for card in data["cards"]]
        return cls(
            name=data["name"],
            created_at=data["created_at"],
            source_dir=data["source_dir"],
            cards=cards,
        )
