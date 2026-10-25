from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Circuito:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: int
    url: str

    risultati_per_anno: dict = field(default_factory=dict)
    gare_completate: int = 0
    piloti_totali:int=0

    #PER LA RICORSIONE:
    gare_totali: int = 0
    def __hash__(self):
        return hash(self.circuitId)

    def __eq__(self, other):
        if isinstance(other, Circuito):
            return self.circuitId == other. circuitId
        return False

    def __repr__(self):
        return (f"{self.name} ({self. circuitId}) ")
                # if self.year is not None else 'N/D'})")