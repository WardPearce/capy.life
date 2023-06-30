import random

from ..models.submit import CLASSES, WEAPONS


def generate_stats() -> dict:
    random.shuffle(WEAPONS)
    random.shuffle(CLASSES)
    return {
        "muncher_lvl": random.randint(0, 1000),
        "weapon": WEAPONS[0],
        "class": CLASSES[0],
    }
