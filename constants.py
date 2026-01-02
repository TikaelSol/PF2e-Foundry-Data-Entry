DC = r"DC (\d+)"

ABILITY_SCORES = r"(%s)" % r"|".join([
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
])
SAVES = r"(Reflex|Will|Fortitude)"
SKILLS = r"(%s)" % r"|".join([
    "Perception",
    "Acrobatics",
    "Arcana",
    "Athletics",
    "Crafting",
    "Deception",
    "Diplomacy",
    "Intimidation",
    "Medicine",
    "Nature",
    "Computers",
    "Piloting",
    "Occultism",
    "Performance",
    "Religion",
    "Society",
    "Stealth",
    "Survival",
    "Thievery"
])

CONDITION_COMPENDIUM = r"@Compendium[pf2e.conditionitems."

INLINE_ACTIONS = [
    "Avoid Notice",
    "Balance",
    "Coerce",
    "Crawl",
    "Create a Diversion",
    "Demoralize",
    "Disable Device",
    "Disarm",
    "Feint",
    "Force Open",
    "Grab an Edge",
    "Grapple",
    "Hide",
    "High Jump",
    "Leap",
    "Long Jump",
    "Make an Impression",
    "Perform",
    "Reposition",
    "Search",
    "Seek",
    "Sense Motive",
    "Shove",
    "Sneak",
    "Steal",
    "Take Cover",
    "Track",
    "Treat Disease",
    "Treat Poison",
    "Trip",
    "Tumble Through",
]

LINKED_ACTIONS = [
    {"name": "Administer First Aid", "id": "HLuKy4nQO2Z4Am1"},
    {"name": "Earn Income", "id": "QyzlsLrqM0EEwd7j"},
    {"name": "Recall Knowledge", "id": "1OagaWtBpVXExToo"},
    {"name": "Treat Wounds", "id": "1kGNdIIhuglAjIp9"}
]

CONDITIONS = [
    "Blinded",
    "Grabbed",
    "Concealed",
    "Confused",
    "Dazzled",
    "Deafened",
    "Fatigued",
    "Fascinated",
    "Flat-Footed",
    "Fleeing",
    "Immobilized",
    "Off-Guard"
    "Paralyzed",
    "Prone",
    "Quickened",
    "Restrained",
    "Unconscious",
]

SF_CONDITIONS = [
    "Suppressed",
    "Untethered"
]

NUMBERED_CONDITIONS = [
    "Clumsy",
    "Doomed",
    "Drained",
    "Enfeebled",
    "Frightened",
    "Sickened",
    "Slowed",
    "Stunned",
    "Stupefied",
    "Quickened",
    "Wounded"
]

SF_NUMBERED_CONDITIONS = [
    "Glitching"
]

BOOK_TITLES = [
    "Core Rulebook",
    "Advanced Player's Guide",
    "Bestiary",
    "Bestiary 2",
    "Bestiary 3",
    "Book of the Dead",
    "Guns & Gears",
    "Secrets of Magic",
    "Lost Omens Gods & Magic",
    "Lost Omens The Mwangi Expanse",
    "Lost Omens World Guide",
    "Lost Omens Character Guide",
    "Lost Omens Legends",
    "Lost Omens Pathfinder Society Guide" "Lost Omens Ancestry Guide",
    "Lost Omens The Grand Bazaar",
    "Lost Omens Absalom, City of Lost Omens",
    "Lost Omens Monsters of Myth",
    "Lost Omens Knights of Lastwall",
    "Lost Omens Travel Guide",
    "Lost Omens Impossible Lands",
    "Lost Omens Highhelm",
    "Lost Omens Firebrands",
    "Treasure Vault",
    "Player Core",
    "GM Core",
    "Pathfinder Player Core",
    "Pathfinder GM Core"
]

DAMAGE_TYPES = r"(%s)" % r"|".join([
    "bludgeoning",
    "piercing",
    "slashing",
    "bleed",
    "positive",
    "negative",
    "vitality",
    "void",
    "acid",
    "cold",
    "electricity",
    "fire",
    "mental",
    "sonic",
    "force",
    "chaotic",
    "lawful",
    "good",
    "evil",
    "spirit",
    "poison",
    "untyped"
])

EQUIPMENT = []
# "Handwraps of Mighty Blows"]

FEATS = []
# "Canny Acumen", "Quick Jump"]

SPELLS = []
# "Dimension Door", "Plane Shift", "Stone Tell", "divine lance", "protection",
# "searing light", "divine wrath", "divine decree", "divine aura", "heroism",
# "chilling spray", "ray of frost", "cone of cold", "polar ray", "heal",
# "water walk", "electric arc", "shocking grasp", "lightning bolt",
# "lightning storm", "chain lightning", "fireball", "chilling darkness",
# "produce flame", "burning hands", "flaming sphere", "wall of fire",
# "meteor swarm", "magic missile", "spiritual weapon", "spirtual guardian",
# "spirit song", "hypercognition", "daze",  "phantom pain", "warrior's regret",
# "phantasmal killer", "weird", "phantasmal calamity", "harm", "chill touch",
# "sudden blight", "enervation", "wail of the banshee", "puff of poison",
# "spider sting", "noxious vapors", "swarming wasp stings",
# "purple worm sting", "linnorm sting", "imp sting", "disrupt undead",
# "disrupting weapons", "breath of life", "regenerate", "true seeing",
# "feather fall", "jump", "mending", "illusory disguise", "charm", "fear",
# "share lore", "summon plant or fungus", "object reading", "enthrall",
# "bless", "mindblank", "invisibility", "endure elements", "knock",
# "earth bind", "fly", "augury"]

ACTIVATION_ACTIONS = [
    (r"\[free-action\]", r"F"),
    (r"\[reaction\]", r"R"),
    (r"\[one-action\]", r"1"),
    (r"\[two-actions\]", r"2"),
    (r"\[three-actions\]", r"3"),
]

DAMAGE_ROLLS = [
    (
        r" (\d+) %s damage" % DAMAGE_TYPES,
        r" @Damage[\1[\2]] damage"
    ),
    (
        r"(\d+)d(\d+)\+(\d+) %s damage" % DAMAGE_TYPES,
        r"@Damage[(\1d\2+\3)[\4]] damage"
    ),
    (
        r"(\d+)d(\d+) persistent %s damage" % DAMAGE_TYPES,
        r"@Damage[\1d\2[persistent,\3]] damage"
    ),
    (
        r"(\d+)d(\d+) %s damage" % DAMAGE_TYPES,
        r"@Damage[\1d\2[\3]] damage"
    ),
    (
        r"(\d+)d(\d+) damage",
        r"@Damage[\1d\2[untyped]] damage"
    ),
    (
        r" (\d+) damage",
        r" @Damage[\1[untyped]] damage"
    ),
    (
        r"(\d+)d(\d+) Hit Points",
        r"@Damage[\1d\2[healing]] Hit Points"
    ),
    (
        r"(\d+)d(\d+)\+(\d+) Hit Points",
        r"@Damage[(\1d\2+\3)[healing]] Hit Points"
    ),
    (
        r" (\d+) Hit Points",
        r" @Damage[\1[healing]] Hit Points"
    ),
]

TEMPLATES = r"(%s)" % r"|".join([
    "emanation",
    "burst",
    "cone",
    "line",
    "Emanation",
    "Burst",
    "Cone",
    "Line"
])
