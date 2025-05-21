from dataclasses import dataclass
from model.airport import Airport

@dataclass
class Arco:
    aeroportoP: Airport
    aeroportoA: Airport
    peso: int