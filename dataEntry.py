import regex as re
from regex import sub
from pyperclip import copy
from tkinter import Tk, Frame, Canvas, Text, Button, END, BooleanVar, Menu

## As nice as it is to have these declared separately for some reason different IDEs react poorly to them being * imported.
DC = r"DC (\d+)"

ABILITY_SCORES = r"(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
SAVES = r"(Reflex|Will|Fortitude)"
SKILLS = r"(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|" \
         r"Intimidation|Medicine|Nature|Computers|Piloting|" \
         r"Occultism|Performance|Religion|Society|Stealth|Survival|Thievery)"

CONDITION_COMPENDIUM = r"@Compendium[pf2e.conditionitems."

ACTIONS = ["Avoid Notice", "Balance", "Coerce", "Crawl",
           "Create a Diversion", "Demoralize", "Disable Device", "Disarm", "Earn Income", "Escape", "Feint",
           "Force Open", "Grab an Edge", "Grapple", "High Jump", "Leap", "Liberating Step", "Long Jump",
           "Make an Impression", "Mount", "Perform", "Reposition", "Search", "Seek", "Sense Motive", "Shove", "Sneak",
           "Steal", "Take Cover", "Track", "Treat Disease", "Treat Poison", "Treat Wounds",
           "Trip", "Tumble Through"]

CONDITIONS = ["Blinded", "Fatigued", "Confused", "Concealed", "Dazzled", "Deafened", "Invisible",
              "Flat-Footed", "Immobilized", "Prone", "Unconscious", "Fascinated", "Paralyzed",
              "Hidden", "Quickened", "Fleeing", "Restrained", "Grabbed", "Off-Guard"]

SF_CONDITIONS = ["Suppressed", "Untethered"]

NUMBERED_CONDITIONS = ["Clumsy", "Doomed", "Drained", "Enfeebled", "Slowed", "Frightened", "Sickened", "Stunned", "Stupefied", "Quickened", "Wounded"]

SF_NUMBERED_CONDITIONS = ["Glitching"]

BOOK_TITLES = ["Core Rulebook", "Advanced Player's Guide", "Bestiary", "Bestiary 2", "Bestiary 3", "Book of the Dead", "Guns & Gears", "Secrets of Magic", "Lost Omens Gods & Magic", "Lost Omens The Mwangi Expanse", "Lost Omens World Guide", "Lost Omens Character Guide", "Lost Omens Legends", "Lost Omens Pathfinder Society Guide", "Lost Omens Ancestry Guide", "Lost Omens The Grand Bazaar", "Lost Omens Absalom, City of Lost Omens", "Lost Omens Monsters of Myth", "Lost Omens Knights of Lastwall", "Lost Omens Travel Guide", "Lost Omens Impossible Lands", "Lost Omens Highhelm", "Lost Omens Firebrands", "Treasure Vault", "Player Core", "GM Core", "Pathfinder Player Core", "Pathfinder GM Core"]

DAMAGE_TYPES = r"(bludgeoning|piercing|slashing|bleed|positive|negative|vitality|void|acid|cold|electricity|fire|mental|sonic|force|chaotic|lawful|good|evil|spirit|poison|untyped)"

EQUIPMENT = []#"Handwraps of Mighty Blows"]

FEATS = []#"Canny Acumen", "Quick Jump"]

SPELLS = []#"Dimension Door", "Plane Shift", "Stone Tell", "divine lance", "protection", "searing light", "divine wrath",
          # "divine decree", "divine aura", "heroism", "chilling spray", "ray of frost", "cone of cold", "polar ray", 
          # "heal", "water walk", "electric arc", "shocking grasp", "lightning bolt", "lightning storm", "chain lightning",
          # "fireball", "chilling darkness", "produce flame", "burning hands", "flaming sphere", "wall of fire", "meteor swarm",
          # "magic missile", "spiritual weapon", "spirtual guardian", "spirit song", "hypercognition", "daze", 
          # "phantom pain", "warrior's regret", "phantasmal killer", "weird", "phantasmal calamity", "harm", "chill touch",
          # "sudden blight", "enervation", "wail of the banshee", "puff of poison", "spider sting", "noxious vapors",
          # "swarming wasp stings", "purple worm sting", "linnorm sting", "imp sting", "disrupt undead", "disrupting weapons",
          # "breath of life", "regenerate", "true seeing", "feather fall", "jump", "mending", "illusory disguise", "charm",
          # "fear", "share lore", "summon plant or fungus", "object reading", "enthrall", "bless", "mindblank", "invisibility",
          # "endure elements", "knock", "earth bind", "fly", "augury"]

def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def action_sub(string, action):
    return sub(r"\b" + action + r"\b", r"@Compendium[pf2e.actionspf2e.%s]{%s}" % (action, action), string, count = 1)


def condition_sub(string, condition):
    return sub(condition.lower(), r"%s%s]{%s}" % (CONDITION_COMPENDIUM, condition, condition), string, count = 1)


def condition_sub_with_stage(string, condition, stage):
    return sub(r"%s %s" % (condition.lower(), stage),
                  r"%s%s]{%s %s}" % (CONDITION_COMPENDIUM, condition, condition, stage),
                  string, count=1)


def equipment_sub(string, equipment):
    return sub(equipment, r"@Compendium[pf2e.equipment-srd.%s]{%s}" % (equipment, equipment), string, count = 1)


def feat_sub(string, feat):
    return sub(feat, r"@Compendium[pf2e.feats-srd.%s]{%s}" % (feat, feat), string, count = 1)


def spell_sub(string, spell):
    return sub(spell, r"<em>@Compendium[pf2e.spells-srd.%s]{%s}</em>" % (spell, spell), string, count = 1)


def handle_actions(string):
    for action in ACTIONS:
        string = action_sub(string, action)
    return string


def handle_conditions(string, condition_list, numbered_condition_list):
    for condition in condition_list:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = sub(r"flat footed", r"%sFlat-Footed]" % CONDITION_COMPENDIUM, string, count = 1)
    # Catch flat-footed and turn it into off-guard. Eventually this will be swapped.
    # string = sub(r"off-guard", r"@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]", string, count = 1)
    string = sub(r"{Flat-Footed}", "", string)

    for condition in numbered_condition_list:
        for i in range(1, 6):
            string = condition_sub_with_stage(string, condition, i)
    return string


def handle_equipment(string):
    for equipment in EQUIPMENT:
        string = equipment_sub(string, equipment)
    return string


def handle_feats(string):
    for feat in FEATS:
        string = feat_sub(string, feat)
    return string


def handle_spells(string):
    for spell in SPELLS:
        string = spell_sub(string, spell)
    return string


def handle_activation_actions(string):
    string = sub(r"\[free-action\]", r"<span class='pf2-icon'>F</span>", string)
    string = sub(r"\[reaction\]", r"<span class='pf2-icon'>R</span>", string)
    string = sub(r"\[one-action\]", r"<span class='pf2-icon'>1</span>", string)
    string = sub(r"\[two-actions\]", r"<span class='pf2-icon'>2</span>", string)
    string = sub(r"\[three-actions\]", r"<span class='pf2-icon'>3</span>", string)
    return string


def handle_damage_rolls(string):
    string = sub(r" (\d+) %s damage" % DAMAGE_TYPES, r" @Damage[\1[\2]] damage", string)
    string = sub(r"(\d+)d(\d+)\+(\d+) %s damage" % DAMAGE_TYPES, r"@Damage[(\1d\2+\3)[\4]] damage", string)
    string = sub(r"(\d+)d(\d+) persistent %s damage" % DAMAGE_TYPES, r"@Damage[\1d\2[persistent,\3]] damage", string)
    string = sub(r"(\d+)d(\d+) %s damage" % DAMAGE_TYPES, r"@Damage[\1d\2[\3]] damage", string)
    string = sub(r"(\d+)d(\d+) damage", r"@Damage[\1d\2[untyped]] damage", string)
    string = sub(r"(\d+)d(\d+) (\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]].", string)
    
    string = string.replace(r"[negative]", r"[void]")
    string = string.replace(r"[positive]", r"[vitality]")
    return string


def handle_spell_heightening(string):
    string = sub(r"Heightened \(", r"<hr />Heightened (", string, count=1)
    string = sub(r"Heightened \(\+(\d+)\)", r"</p><p><strong>Heightened (+\1)</strong>", string)
    string = sub(r"Heightened \((\d+)(\w+)\)", r"</p><p><strong>Heightened (\1\2)</strong>", string)
    string = sub(r"<hr /></p><p><strong>Heightened", r"</p><hr /><p><strong>Heightened", string)
    return string

def handle_level_heightening(string):
    string = sub(r"Level \(", r"<hr />Level (", string, count=1)
    string = sub(r"Level \(\+(\d+)\)", r"</p><p><strong>Level (+\1)</strong>", string)
    string = sub(r"Level \((\d+)(\w+)\)", r"</p><p><strong>Level (\1\2)</strong>", string)
    string = sub(r"<hr /></p><p><strong>Level", r"</p><hr /><p><strong>Level", string)
    return string


def handle_bullet_lists(string):
    # Removing bullet points, should replace with the actual bullet points.
    string = sub(r"•", "<ul><li>", string, count=1)
    string = sub(r"•", "</li><li>", string)
    return string


def handle_templates(string):
    # Add template buttons
    string = sub(r"(\d+)-(foot|Foot) (emanation|burst|cone|line|Emanation|Burst|Cone|Line)", r"@Template[type:\3|distance:\1]", string)
    string = sub(r"type:%s" % r"(Emanation|Burst|Cone|Line)", convert_to_lower, string)
    
    return string


def handle_third_party(string):
    # Handling for 3rd party formatting.
    string = sub(r"» (Critical Success|Success|Failure|Critical Failure)", r"</p><p><strong>\1</strong>", string)
    string = sub(r"»", r"•", string)
    return string


def handle_background(string):
    string = sub(r"Choose two ability boosts.", r"</p><p>Choose two ability boosts.", string)
    string = sub(r"Choose two attribute boosts.", r"</p><p>Choose two attribute boosts.", string)
    string = sub(r"%s" % ABILITY_SCORES, r"<strong>\1</strong>", string, count=2)
    string = sub(r"You're trained in", r"</p><p>You're trained in", string)
    # string = sub(r"You gain the (.*) skill feat",r"You gain the @Compendium[pf2e.feats-srd.\1]{\1} skill feat",string)
    return string


def handle_aura(string):
    string = sub(r"<p>(\d+) feet.",r"<p>@Template[type:emanation|distance:\1] @Compendium[pf2e.bestiary-ability-glossary-srd.Aura]{Aura}</p><p>", string)
    return string


def companion_format(string):
    string = sub(r"Size (Tiny|Small|Medium|Large)", r"<p><strong>Size</strong> \1</p>", string)
    string = sub(r"Melee \? (\w+)(,|;) Damage (\d+)d(\d+) (\w+)", r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1, <strong>Damage</strong> \3d\4 \5</p>", string)
    string = sub(r"Melee \? (\w+) \(([^\)]+)\)(,|;) Damage (\d+)d(\d+) (\w+)", r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1 (\2), <strong>Damage</strong> \4d\5 \6</p>", string)
    string = sub(r"Str ", r"<p><strong>Str</strong> ", string)
    string = sub(r"(Dex|Con|Int|Wis|Cha) ", r"<strong>\1</strong> ", string)
    string = sub(r"Hit Points (\d+)", r"</p><p><strong>Hit Points</strong> \1</p>", string)
    string = sub(r"(Skill|Senses|Speed|Support Benefit|Advanced Maneuver)", r"</p><p><strong>\1</strong>", string)
    return string


def eidolon_format(string):
    string = sub(r"(Tradition|Traits|Alignment|Home Plane|Size|Suggested Attacks|Skills|Senses|Language|Speed|Eidolon Abilities)", r"</p><p><strong>\1</strong>", string)
    string = sub(r"(\w+) (\w+) Str (\d+), Dex (\d+), Con (\d+), Int (\d+), Wis (\d+), Cha (\d+); \+(\d+) AC \(\+(\d+) Dex cap\)", r"</p><p><strong>\1 \2</strong> Str \3, Dex \4, Con \5, Int \6, Wis \7, Cha \8; +\9 AC (+\10 Dex cap)", string)
    return string


def handle_inlines_checks(string):
    # Skills and saves
    string = sub(r"%s basic (\w+) save" % DC, r"@Check[type:\2|dc:\1|basic:true] save", string)
    string = sub(r"basic (\w+) save %s" % DC, r"@Check[type:\1|dc:\2|basic:true] save", string)
    string = sub(r"basic (\w+) %s" % DC, r"@Check[type:\1|dc:\2|basic:true]", string)
    string = sub(r"%s %s" % (DC, SAVES), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s save \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2] save", string)

    string = sub(r"%s %s or %s" % (DC, SKILLS, SKILLS), r"@Check[type:\2|dc:\1] or @Check[type:\3|dc:\1]", string)
    string = sub(r"%s %s (trained|expert|master|legendary) or %s" % (DC, SKILLS, SKILLS), r"@Check[type:\2|dc:\1] (\3) or @Check[type:\4|dc:\1]", string)
    string = sub(r"%s %s" % (DC, SKILLS), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SKILLS, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SKILLS, DC), r"@Check[type:\1|dc:\2", string)

    string = sub(r"(\w+) Lore %s" % DC, r"@Check[type:\2-lore|dc:\1]{\1 Lore}", string)
    string = sub(r"%s (\w+) save" % DC, r"@Check[type:\2|dc:\1] save", string)
    string = sub(r"%s flat check" % DC, r"@Check[type:flat|dc:\1]", string)
    
    string = sub(r"basic %s save against your class DC or spell DC" % SAVES, r"@Check[type:\1|dc:resolve(@actor.system.attributes.classOrSpellDC.value)|basic:true] save against your class DC or spell DC", string)
    string = sub(r"%s save against your class DC or spell DC" % SAVES, r"@Check[type:\1|dc:resolve(@actor.system.attributes.classOrSpellDC.value)] save against your class DC or spell DC", string)
    string = sub(r"basic %s save against your class DC" % SAVES, r"@Check[type:\1|dc:resolve(@actor.system.attributes.classDC.value)|basic:true] save against your class DC", string)
    string = sub(r"%s save against your class DC" % SAVES, r"@Check[type:\1|dc:resolve(@actor.system.attributes.classDC.value)] save against your class DC", string)
    

    # Catch capitalized saves
    string = sub(r"type:%s" % SAVES, convert_to_lower, string)
    string = sub(r"type:%s" % SKILLS, convert_to_lower, string)
    
    # Lores - capture 1-2 words between 'DC ##' and 'Lore'    
    string = sub(r"%s ((?:\w+\s+){1,2})Lore" % DC, r"@Check[type:\2Lore|dc:\1]", string)
    
    return string


def handle_counteract(string):
    string = sub(r"counteract modifier of \+(\d+)", r"counteract modifier of [[/r 1d20+\1 #Counteract]]{+\1}", string)
    string = sub(r"\+(\d+) counteract modifier", r"[[/r 1d20+\1 #Counteract]]{+\1} counteract modifier", string)
    return string


def ancestry_format(string):
    string = sub(r"(?i)Y\s*O\s*U M\s*I\s*G\s*H\s*T\s*...", r"</p><h2>You Might...</h2>", string)
    string = sub(r"O\s*T\s*H\s*E\s*R\s*S P\s*R\s*O\s*B\s*A\s*B\s*L\s*Y\s*...", r"</ul><h2>Others Probably...</h2><ul>", string, flags=re.IGNORECASE)
    string = sub(r"(?i)P\s*H\s*Y\s*S\s*I\s*C\s*A\s*L D\s*E\s*S\s*C\s*R\s*I\s*P\s*T\s*I\s*O\s*N", r"</ul><h2>Physical Description</h2><p>", string)
    string = sub(r"(?i)S\s*O\s*C\s*I\s*E\s*T\s*Y", r"</p><h2>Society</h2><p>", string, count = 1)
    string = sub(r"(?i)A\s*L\s*I\s*G\s*N\s*M\s*E\s*N\s*T A\s*N\s*D R\s*E\s*L\s*I\s*G\s*I\s*O\s*N", r"</p><h2>Alignment and religion</h2><p>", string)
    string = sub(r"NAMES", r"</p><h2>Names</h2><p>", string)
    string = sub(r"(?i)S\s*a\s*m\s*p\s*l\s*e N\s*a\s*m\s*e\s*S", r"</p><h3>Sample Names</h3><p>", string)
    return string


def handle_areas(string):
    string = sub(r" ([A-Z][0-9]{1,3})", r" <strong>\1</strong>", string)
    return string


def handle_innate_spell_links(string):
    string = sub(r"You can cast (\w+) (.*?) innate", r"You can cast <em>@Compendium[pf2e.spells-srd.\1]{\1}</em> \2 innate", string)
    return string


def remove_books(string):
    for book in BOOK_TITLES:
        string = sub(r" \((Pathfinder |)%s (\d+)\)" % book, r"", string)
    
    string = sub(r" \(page (\d+)\)", r"", string)
    
    return string


def format_monster_parts(string):
    string = string.replace("Monster Parts", "<h2>Suggested Monster Parts</h2><p><strong>Monster Parts</strong>")\
        .replace("Eligible Refinements", "</p><p><strong>Eligible Refinements</strong>")\
        .replace("Eligible Imbued Properties", "</p><p><strong>Eligible Imbued Properties</strong>")

    return string

# Fix the links, until we have a better way to do it.
def fix_links(string):
    string = string.replace("@Compendium[pf2e.conditionitems.Blinded]", "@UUID[Compendium.pf2e.conditionitems.Item.XgEqL1kFApUbl5Z2]")\
        .replace("@Compendium[pf2e.conditionitems.Fatigued]", "@UUID[Compendium.pf2e.conditionitems.Item.HL2l2VRSaQHu9lUw]")\
        .replace("@Compendium[pf2e.conditionitems.Confused]", "@UUID[Compendium.pf2e.conditionitems.Item.yblD8fOR1J8rDwEQ]")\
        .replace("@Compendium[pf2e.conditionitems.Concealed]", "@UUID[Compendium.pf2e.conditionitems.Item.DmAIPqOBomZ7H95W]")\
        .replace("@Compendium[pf2e.conditionitems.Dazzled]", "@UUID[Compendium.pf2e.conditionitems.Item.TkIyaNPgTZFBCCuh]")\
        .replace("@Compendium[pf2e.conditionitems.Deafened]", "@UUID[Compendium.pf2e.conditionitems.Item.9PR9y0bi4JPKnHPR]")\
        .replace("@Compendium[pf2e.conditionitems.Invisible]", "@UUID[Compendium.pf2e.conditionitems.Item.zJxUflt9np0q4yML]")\
        .replace("@Compendium[pf2e.conditionitems.Flat-Footed]", "@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]")\
        .replace("@Compendium[pf2e.conditionitems.Off-Guard]", "@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]")\
        .replace("@Compendium[pf2e.conditionitems.Immobilized]", "@UUID[Compendium.pf2e.conditionitems.Item.eIcWbB5o3pP6OIMe]")\
        .replace("@Compendium[pf2e.conditionitems.Prone]", "@UUID[Compendium.pf2e.conditionitems.Item.j91X7x0XSomq8d60]")\
        .replace("@Compendium[pf2e.conditionitems.Unconscious]", "@UUID[Compendium.pf2e.conditionitems.Item.fBnFDH2MTzgFijKf]")\
        .replace("@Compendium[pf2e.conditionitems.Fascinated]", "@UUID[Compendium.pf2e.conditionitems.Item.AdPVz7rbaVSRxHFg]")\
        .replace("@Compendium[pf2e.conditionitems.Paralyzed]", "@UUID[Compendium.pf2e.conditionitems.Item.6uEgoh53GbXuHpTF]")\
        .replace("@Compendium[pf2e.conditionitems.Hidden]", "@UUID[Compendium.pf2e.conditionitems.Item.iU0fEDdBp3rXpTMC]")\
        .replace("@Compendium[pf2e.conditionitems.Quickened]", "@UUID[Compendium.pf2e.conditionitems.Item.nlCjDvLMf2EkV2dl]")\
        .replace("@Compendium[pf2e.conditionitems.Fleeing]", "@UUID[Compendium.pf2e.conditionitems.Item.sDPxOjQ9kx2RZE8D]")\
        .replace("@Compendium[pf2e.conditionitems.Restrained]", "@UUID[Compendium.pf2e.conditionitems.Item.VcDeM8A5oI6VqhbM]")\
        .replace("@Compendium[pf2e.conditionitems.Grabbed]", "@UUID[Compendium.pf2e.conditionitems.Item.kWc1fhmv9LBiTuei]")\
        .replace("@Compendium[pf2e.conditionitems.Clumsy]", "@UUID[Compendium.pf2e.conditionitems.Item.i3OJZU2nk64Df3xm]")\
        .replace("@Compendium[pf2e.conditionitems.Doomed]", "@UUID[Compendium.pf2e.conditionitems.Item.3uh1r86TzbQvosxv]")\
        .replace("@Compendium[pf2e.conditionitems.Drained]", "@UUID[Compendium.pf2e.conditionitems.Item.4D2KBtexWXa6oUMR]")\
        .replace("@Compendium[pf2e.conditionitems.Enfeebled]", "@UUID[Compendium.pf2e.conditionitems.Item.MIRkyAjyBeXivMa7]")\
        .replace("@Compendium[pf2e.conditionitems.Slowed]", "@UUID[Compendium.pf2e.conditionitems.Item.xYTAsEpcJE1Ccni3]")\
        .replace("@Compendium[pf2e.conditionitems.Frightened]", "@UUID[Compendium.pf2e.conditionitems.Item.TBSHQspnbcqxsmjL]")\
        .replace("@Compendium[pf2e.conditionitems.Sickened]", "@UUID[Compendium.pf2e.conditionitems.Item.fesd1n5eVhpCSS18]")\
        .replace("@Compendium[pf2e.conditionitems.Stunned]", "@UUID[Compendium.pf2e.conditionitems.Item.dfCMdR4wnpbYNTix]")\
        .replace("@Compendium[pf2e.conditionitems.Stupefied]", "@UUID[Compendium.pf2e.conditionitems.Item.e1XGnhKNSQIm5IXg]")\
        .replace("@Compendium[pf2e.conditionitems.Wounded]", "@UUID[Compendium.pf2e.conditionitems.Item.Yl48xTdMh3aeQYL2]")\
        .replace("@Compendium[pf2e.conditionitems.Glitching]", "@UUID[Compendium.starfinder-field-test-for-pf2e.conditions.Item.6A2QDy8wRGCVQsSd]")\
        .replace("@Compendium[pf2e.conditionitems.Suppressed]", "@UUID[Compendium.starfinder-field-test-for-pf2e.conditions.Item.enA7BxAjBb7ns1iF]")\
        .replace("@Compendium[pf2e.conditionitems.Untethered]", "@UUID[Compendium.starfinder-field-test-for-pf2e.conditions.Item.z1ucw4CLwLqHoAp3]")\
        .replace("@Compendium[pf2e.actionspf2e.Avoid Notice]", "@UUID[Compendium.pf2e.actionspf2e.Item.IE2nThCmoyhQA0Jn]")\
        .replace("@Compendium[pf2e.actionspf2e.Balance]", "@UUID[Compendium.pf2e.actionspf2e.Item.M76ycLAqHoAgbcej]")\
        .replace("@Compendium[pf2e.actionspf2e.Coerce]", "@UUID[Compendium.pf2e.actionspf2e.Item.tHCqgwjtQtzNqVvd]")\
        .replace("@Compendium[pf2e.actionspf2e.Crawl]", "@UUID[Compendium.pf2e.actionspf2e.Item.Tj055UcNm6UEgtCg]")\
        .replace("@Compendium[pf2e.actionspf2e.Create a Diversion]", "@UUID[Compendium.pf2e.actionspf2e.Item.GkmbTGfg8KcgynOA]")\
        .replace("@Compendium[pf2e.actionspf2e.Demoralize]", "@UUID[Compendium.pf2e.actionspf2e.Item.2u915NdUyQan6uKF]")\
        .replace("@Compendium[pf2e.actionspf2e.Disable Device]", "@UUID[Compendium.pf2e.actionspf2e.Item.cYdz2grcOcRt4jk6]")\
        .replace("@Compendium[pf2e.actionspf2e.Disarm]", "@UUID[Compendium.pf2e.actionspf2e.Item.Dt6B1slsBy8ipJu9]")\
        .replace("@Compendium[pf2e.actionspf2e.Earn Income]", "@UUID[Compendium.pf2e.actionspf2e.Item.QyzlsLrqM0EEwd7j]")\
        .replace("@Compendium[pf2e.actionspf2e.Escape]", "@UUID[Compendium.pf2e.actionspf2e.Item.SkZAQRkLLkmBQNB9]")\
        .replace("@Compendium[pf2e.actionspf2e.Feint]", "@UUID[Compendium.pf2e.actionspf2e.Item.QNAVeNKtHA0EUw4X]")\
        .replace("@Compendium[pf2e.actionspf2e.Force Open]", "@UUID[Compendium.pf2e.actionspf2e.Item.SjmKHgI7a5Z9JzBx]")\
        .replace("@Compendium[pf2e.actionspf2e.Grab an Edge]", "@UUID[Compendium.pf2e.actionspf2e.Item.3yoajuKjwHZ9ApUY]")\
        .replace("@Compendium[pf2e.actionspf2e.Grapple]", "@UUID[Compendium.pf2e.actionspf2e.Item.PMbdMWc2QroouFGD]")\
        .replace("@Compendium[pf2e.actionspf2e.High Jump]", "@UUID[Compendium.pf2e.actionspf2e.Item.2HJ4yuEFY1Cast4h]")\
        .replace("@Compendium[pf2e.actionspf2e.Leap]", "@UUID[Compendium.pf2e.actionspf2e.Item.d5I6018Mci2SWokk]")\
        .replace("@Compendium[pf2e.actionspf2e.Long Jump]", "@UUID[Compendium.pf2e.actionspf2e.Item.JUvAvruz7yRQXfz2]")\
        .replace("@Compendium[pf2e.actionspf2e.Make an Impression]", "@UUID[Compendium.pf2e.actionspf2e.Item.OX4fy22hQgUHDr0q]")\
        .replace("@Compendium[pf2e.actionspf2e.Mount]", "@UUID[Compendium.pf2e.actionspf2e.Item.PM5jvValFkbFH3TV]")\
        .replace("@Compendium[pf2e.actionspf2e.Perform]", "@UUID[Compendium.pf2e.actionspf2e.Item.EEDElIyin4z60PXx]")\
        .replace("@Compendium[pf2e.actionspf2e.Reposition]", "@UUID[Compendium.pf2e.actionspf2e.Item.lOE4yjUnETTdaf2T]")\
        .replace("@Compendium[pf2e.actionspf2e.Search]", "@UUID[Compendium.pf2e.actionspf2e.Item.TiNDYUGlMmxzxBYU]")\
        .replace("@Compendium[pf2e.actionspf2e.Seek]", "@UUID[Compendium.pf2e.actionspf2e.Item.BlAOM2X92SI6HMtJ]")\
        .replace("@Compendium[pf2e.actionspf2e.Sense Motive]", "@UUID[Compendium.pf2e.actionspf2e.Item.1xRFPTFtWtGJ9ELw]")\
        .replace("@Compendium[pf2e.actionspf2e.Shove]", "@UUID[Compendium.pf2e.actionspf2e.Item.7blmbDrQFNfdT731]")\
        .replace("@Compendium[pf2e.actionspf2e.Sneak]", "@UUID[Compendium.pf2e.actionspf2e.Item.VMozDqMMuK5kpoX4]")\
        .replace("@Compendium[pf2e.actionspf2e.Steal]", "@UUID[Compendium.pf2e.actionspf2e.Item.RDXXE7wMrSPCLv5k]")\
        .replace("@Compendium[pf2e.actionspf2e.Take Cover]", "@UUID[Compendium.pf2e.actionspf2e.Item.ust1jJSCZQUhBZIz]")\
        .replace("@Compendium[pf2e.actionspf2e.Track]", "@UUID[Compendium.pf2e.actionspf2e.Item.EA5vuSgJfiHH7plD]")\
        .replace("@Compendium[pf2e.actionspf2e.Treat Disease]", "@UUID[Compendium.pf2e.actionspf2e.Item.TC7OcDa7JlWbqMaN]")\
        .replace("@Compendium[pf2e.actionspf2e.Treat Poison]", "@UUID[Compendium.pf2e.actionspf2e.Item.KjoCEEmPGTeFE4hh]")\
        .replace("@Compendium[pf2e.actionspf2e.Treat Wounds]", "@UUID[Compendium.pf2e.actionspf2e.Item.1kGNdIIhuglAjIp9]")\
        .replace("@Compendium[pf2e.actionspf2e.Trip]", "@UUID[Compendium.pf2e.actionspf2e.Item.ge56Lu1xXVFYUnLP]")\
        .replace("@Compendium[pf2e.actionspf2e.Tumble Through]", "@UUID[Compendium.pf2e.actionspf2e.Item.21WIfSu7Xd7uKqV8]")
        
    return string


def preProcessSpellHeader(string):
    string = sub(r"\nRange (\d+) feet; (Targets|Target) (.*?)\n", r"<hr>", string)
    string = sub(r"\nRange (\d+) feet;\n", r"<hr>", string)
    string = sub(r"\nArea (\d+)-foot (\w+)\n", r"<hr>", string)
    string = sub(r"\nArea (\d+)-foot (\w+) (Targets|Target) (.*?)\n", r"<hr>", string)
    string = sub(r"Defense (\w+)\n", r"<hr>", string)
    string = sub(r"(<hr>)+", r"<hr>", string)
    
    return string

def eldamonMode(string):
    # Skills and saves
    string = sub(r"basic (\w+) save", r"@Check[type:\1|dc:resolve(@actor.system.proficiencies.classDCs.eldamon.dc)|basic:true] save", string, count = 1)
    string = sub(r"(\w+) save", r"@Check[type:\1|dc:resolve(@actor.system.proficiencies.classDCs.eldamon.dc)] save", string, count = 1)
    string = sub(r"@Damage\[1d(\d+)\[(\w+)\]\] damage plus \@Damage\[1d(\d+)\[(\w+)\]\] damage for (each|every) level you have", r"@Damage[(1+@actor.level)d\1[\2]]", string)
    string = sub(r"(melee|ranged) power attack roll", r"@Check[type:eldamon|defense:ac]{\1 power attack roll}", string, count = 1)
    string = string.replace(r"roll}s", r"rolls}")
    
    return string

def reformat(text, third_party = False, companion = False, eidolon = False, ancestry = False, use_clipboard=True, add_gm_text = True, inline_rolls = True, starfinder_mode = True, add_conditions = True, add_actions = True, add_inline_checks = True, add_inline_templates = True, remove_non_ASCII = True, replacement_mode = False, monster_parts = False, eldamon_mode = False):
    # Initial handling not using regex.
    string = "<p>" + text
    string = preProcessSpellHeader(string)
    string = string.replace("Trigger", "<p><strong>Trigger</strong>")\
        .replace(" "," ")\
        .replace("\nCritical Success", "</p><hr /><p><strong>Critical Success</strong>")\
        .replace("\nSuccess", "</p><p><strong>Success</strong>")\
        .replace("\nFailure", "</p><p><strong>Failure</strong>")\
        .replace("\nCritical Failure", "</p><p><strong>Critical Failure</strong>")\
        .replace("\nSpecial", "</p><hr><p><strong>Special</strong>")\
        .replace("-\n","-")\
        .replace("—\n","—")\
        .replace("\n", " ")\
        .replace("Frequency", "<p><strong>Frequency</strong>")\
        .replace("Effect", "</p><hr /><p><strong>Effect</strong>")\
        .replace("Cost", "<strong>Cost</strong>") + "</p>"
    string = string.replace("<p><p>", "<p>")\
        .replace("Maximum Duration", "</p><p><strong>Maximum Duration</strong>")\
        .replace("Onset", "</p><p><strong>Onset</strong>")\
        .replace("Saving Throw", "</p><p><strong>Saving Throw</strong>")\
        .replace("f at-footed", "flat-footed").replace("Ef ect", "Effect") # Fix common Paizo pre-release PDF formatting errors
        
    if starfinder_mode:
        condition_list = CONDITIONS + SF_CONDITIONS
        numbered_condition_list = SF_NUMBERED_CONDITIONS
        
    if remove_non_ASCII:
        string = string.replace("’", "'").replace(r"”", r'"').replace(r"“", r'"')
    
    string = sub(r"(Requirements|Requirement)", r"</p><p><strong>Requirements</strong>", string)
    string = sub(r" Craft </p><p><strong>Requirements</strong>", r"</p><hr /><p><strong>Craft Requirements</strong>", string)
    
    string = sub(r"Stage (\d)", r"</p><p><strong>Stage \1</strong>", string)

    string = sub("Access", "<p><strong>Access</strong>", string, count=1)
    string = sub(r"Activate \?", r"</p><p><strong>Activate</strong> <span class='pf2-icon'>1</span>", string)
    string = sub(r"Activate (\d+) (minute|minutes|hour|hours)", r"</p><p><strong>Activate</strong> \1 \2", string)
    string = sub(r"Activate—(.*?) \?", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>1</span>", string)
    string = sub(r"Activate—(.*?) \[reaction\]", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>r</span>", string)
    string = sub(r"Activate—(.*?) \[one-action\]", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>1</span>", string)
    string = sub(r"Activate—(.*?) \[two-actions\]", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>2</span>", string)
    string = sub(r"Activate—(.*?) \[three-actions\]", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>3</span>", string)
    string = sub(r"Activate—(.*?) \[free-action\]", r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>f</span>", string)
    string = sub(r"Activate—(.*?) (\d+) (minute|minutes|hour|hours)", r"</p><p><strong>Activate—\1</strong> \2 \3", string)
    string = string.replace(r"<p><strong></p>",r"")
    
    string = sub(r"can't use (.*?) again for (\d)d(\d) rounds", r"can't use \1 again for [[/br \2d\3 #Recharge \1]]{\2d\3 rounds}", string)
    string = sub(r"can't (.*?) again for (\d)d(\d) rounds", r"can't \1 again for [[/br \2d\3 #Recharge \1]]{\2d\3 rounds}", string)
    string = sub(r" (\d)d(\d) (rounds|minutes|hours|days)", r" [[/br \1d\2 #\3]]{\1d\2 \3}", string)
    string = string.replace(r"or dispel magic (", r"or @UUID[Compendium.pf2e.spells-srd.Item.9HpwDN4MYQJnW0LG] (")

    if third_party:
        string = handle_third_party(string)
    
    if companion:
        string = companion_format(string)
    
    if eidolon:
        string = eidolon_format(string)
    
    if ancestry:
        string = ancestry_format(string)
        
    if add_inline_checks:
        string = handle_inlines_checks(string)
    
    if add_conditions:
        string = handle_conditions(string, condition_list, numbered_condition_list)

    if inline_rolls:
        string = handle_damage_rolls(string)
    
    if add_inline_templates:
        string = handle_templates(string)
    
    string = handle_spell_heightening(string)
    string = handle_level_heightening(string)
    string = handle_bullet_lists(string)
    
    if add_actions:
        string = handle_actions(string)
    
    if monster_parts:
        string = format_monster_parts(string)
    
    string = fix_links(string)
    # string = handle_equipment(string)
    # string = handle_feats(string)
    # string = handle_spells(string)
    # string = handle_innate_spell_links(string)
    string = handle_counteract(string)
    
    string = handle_activation_actions(string)
    # string = handle_aura(string)
    
    string = handle_areas(string)
    
    string = remove_books(string)    

    if "Choose two ability boosts" in string or "Choose two attribute boosts" in string:
        string = handle_background(string)
        
    string = string.replace("<p></p>","").replace("<p><p>","<p>")
    string = string.replace(" <p>","</p><p>")
    string = string.replace(" </p>", "</p>")
    string = string.replace(";</p>","</p>")
    string = string.replace("<p> ","<p>")
    
    # Catch non-link references to flat footed.
    string = string.replace("flat footed", "off-guard").replace("flat-footed", "off-guard")
    
    # # Sneak attack features have different text requirements so we undo some of the changes made
    # string = sub(r"deals an additional \[\[/r {(\d)d(\d)}\[precision\]\]\]{(\d)d(\d) precision damage} to @Compendium\[pf2e.conditionitems.Flat-Footed\]{Flat-Footed} creatures.", r"deals an additional \1d\2 precision damage to flat-footed creatures.", string)
    
    if eldamon_mode:
        string = eldamonMode(string)
            
    if add_gm_text:
        string = string.replace("<p><strong>Trigger</strong>", "<p data-visibility='gm'><strong>Trigger</strong>")
        string = string.replace("<p><strong>Requirements</strong>", "<p data-visibility='gm'><strong>Requirements</strong>")
        string = string.replace("<p><strong>Frequency</strong>", "<p data-visibility='gm'><strong>Frequency</strong>")

    # This is for text replacement without the wrapping <p></p> tags around the entire block. Easiest to just strip them.
    if replacement_mode:
        string = string[3:]
        string = string[:-4]

    # print("\n")
    # print(string)

    if use_clipboard:
        copy(string)

    # return string
    outputText.delete("1.0", END)
    outputText.insert(END, string)
    
    
###############################################################################
# If you want to run the console version of this instead of the GUI comment out
# the outputText lines above and uncomment `return string`. Then comment out 
# everything below up to `def main()` then comment out `root.mainloop()` and 
# uncomment `reformat(...)`.
#
# Build with `pyinstaller --noconsole --icon="D20_icon.ico" --onefile dataEntry.py`
###############################################################################

def clearInput():
    inputText.delete("1.0", END)

Height = 700
Width = 800

root = Tk()

root.title("PF2e on Foundry VTT Data Entry v 2.25")

canvas = Canvas(root, height = Height, width = Width)
canvas.pack()

frame = Frame(root, bg = '#80c0ff')
frame.place(relwidth = 1, relheight = 1)

inputText = Text(frame, bg = 'white')
inputText.place(rely = 0.2, relwidth = 0.49, relheight = 0.8)

outputText = Text(frame, bg = 'white')
outputText.place(relx = 0.51, rely = 0.2, relwidth = 0.49, relheight = 0.8)

## Settings
###############################################################################
third_party = BooleanVar(value = False)
monster_parts = BooleanVar(value = False)
companion = BooleanVar(value = False)
eidolon = BooleanVar(value = False)
ancestry = BooleanVar(value = False)
replacement_mode = BooleanVar(value = False)
use_clipboard = BooleanVar(value = True)
add_gm_text = BooleanVar(value = False)
inline_rolls = BooleanVar(value = True)
add_conditions = BooleanVar(value = True)
add_actions = BooleanVar(value = True)
add_inline_checks = BooleanVar(value = True)
starfinder_mode = BooleanVar(value = True)
add_inline_templates = BooleanVar(value = True)
remove_non_ASCII = BooleanVar(value = True)
eldamon_mode = BooleanVar(value = False)
###############################################################################


# Build settings menu
##############################################################################

menu = Menu(root)

settings_menu = Menu(menu)
settings_menu.add_checkbutton(label = "Copy Output to Clipboard", variable = use_clipboard)
settings_menu.add_checkbutton(label = "Add GM Only Tags", variable = add_gm_text)
settings_menu.add_checkbutton(label = "Handle Inline rolls", variable = inline_rolls)
settings_menu.add_checkbutton(label = "Handle Starfinder 2e formatting", variable = starfinder_mode)
settings_menu.add_checkbutton(label = "Add Inline Templates", variable = add_inline_templates)
settings_menu.add_checkbutton(label = "Add Inline Checks", variable = add_inline_checks)
settings_menu.add_checkbutton(label = "Add Condition Links", variable = add_conditions)
settings_menu.add_checkbutton(label = "Add Action Links", variable = add_actions)
settings_menu.add_checkbutton(label = "Remove non-ASCII characters", variable = remove_non_ASCII)
settings_menu.add_checkbutton(label = "No Wrapping <p> tags", variable = replacement_mode)
settings_menu.add_checkbutton(label = "Handle Animal Companion Blocks", variable = companion)
settings_menu.add_checkbutton(label = "Handle Eidolon Blocks", variable = eidolon)
settings_menu.add_checkbutton(label = "Handle Ancestry Description Text", variable = ancestry)
settings_menu.add_checkbutton(label = "Handle Third Party Formatting (legacy)", variable = third_party)
settings_menu.add_checkbutton(label = "Handle Monster Part Formatting (third party)", variable = monster_parts)
settings_menu.add_checkbutton(label = "Handle Eldamon Powers (third party)", variable = eldamon_mode)

menu.add_cascade(label = "Settings", menu = settings_menu)
root.config(menu = menu)

##############################################################################

reformatButton = Button(root, text="Reformat Text", command = lambda: reformat(inputText.get("1.0", "end-1c"), third_party.get(), companion.get(), eidolon.get(), ancestry.get(), use_clipboard.get(), add_gm_text.get(), inline_rolls.get(), starfinder_mode.get(), add_conditions.get(), add_actions.get(), add_inline_checks.get(), add_inline_templates.get(), remove_non_ASCII.get(), replacement_mode.get(), monster_parts.get(), eldamon_mode.get()))
reformatButton.place(relx = 0.75, rely= 0, relwidth = 0.25, relheight = 0.2)

resetButton = Button(root, text="Clear Input", command = lambda: clearInput())
resetButton.place(relx = 0, rely= 0, relwidth = 0.25, relheight = 0.2)

def main():
    # reformat(input(), third_party = False, companion = False, eidolon = False, ancestry = False, use_clipboard=True, add_gm_text = False, inline_rolls = True, add_conditions = True, add_inline_checks = True, add_inline_templates = True, remove_non_ASCII = True)
    root.mainloop()


if __name__ == "__main__":
    main()