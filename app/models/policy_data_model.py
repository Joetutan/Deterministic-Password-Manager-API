from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AccountPolicy:
    
        length: int = 20
        lower: bool = True
        upper: bool = True
        digits: bool = True
        symbols: bool = False

        def to_dict(self) -> dict:
                return {
                        "length": self.length,
                        "lower": self.lower,
                        "upper": self.upper,
                        "digits": self.digits,
                        "symbols": self.symbols
                }

        @classmethod
        def from_dict(cls, data:dict)-> AccountPolicy:
                return cls(
                        length = data["length"],
                        lower = data["lower"],
                        upper = data["upper"],
                        digits= data["digits"],
                        symbols= data["symbols"]
                )

