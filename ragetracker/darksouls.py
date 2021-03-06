from models import db, BossKill
from ragetracker import app
class DarkSouls:
    enemies = [
    'Asylum Demon',
    'Taurus Demon',
    'Belfry Gargoyles',
    'Moonlight Butterfly',
    'Capra Demon',
    'Gaping Dragon',
    'Stray Demon',
    'Chaos Witch Quelaag',
    'Ceaseless Discharge',
    'Iron Golem',
    'Ornstein & Smough',
    'Crossbreed Priscilla',
    'Seath the Scaleless',
    'Pinwheel',
    'Dark Sun Gwyndolin',
    'Gravelord Nito',
    'Demon Firesage',
    'Centipede Demon',
    'The Bed of Chaos',
    'Sif',
    'The Four Kings',
    'Sanctuary Guardian',
    'Knight Artorias',
    'Manus, Father of the Abyss',
    'Black Dragon Kalameet',
    'Gwyn'
    ]

    def getBoss(self, boss_id):
        return self.enemies[boss_id]

# also include for jinja templates
def getBoss(boss_id):
    souls = DarkSouls()
    return souls.enemies[boss_id]
app.jinja_env.globals.update(get_boss=getBoss)
