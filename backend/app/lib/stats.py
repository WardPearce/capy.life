import random
import secrets

from ..models.submit import CLASSES, WEAPONS


def generate_stats() -> dict:
    return {
        "muncher_lvl": random.randint(0, 1000),
        "weapon": secrets.SystemRandom().choice(WEAPONS),
        "class": secrets.SystemRandom().choice(CLASSES),
    }
