import regex as re
from regex import sub

from pyperclip import copy
from tkinter import (
    BooleanVar,
    Button,
    Canvas,
    END,
    Frame,
    Menu,
    Text,
    Tk,
)

import constants


def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def action_sub(string, action):
    return sub(
        r"\b" + action["name"] + r"\b",
        r"@UUID[Compendium.pf2e.actionspf2e.Item.%s]" % action["id"],
        string,
        count=1
    )


def inline_action_sub(string, action):
    return sub(
        r"\b" + action + r"\b",
        r"[[/act %s]]" % (action.lower().replace(" ", "-")),
        string,
        count=1
    )


def condition_sub(string, condition):
    return sub(
        condition.lower(),
        r"%s%s]{%s}" % (constants.CONDITION_COMPENDIUM, condition, condition),
        string,
        count=1
    )


def condition_sub_with_stage(string, condition, stage):
    return sub(
        r"%s %s" % (condition.lower(), stage),
        r"%s%s]{%s %s}" % (
            constants.CONDITION_COMPENDIUM, condition, condition, stage
        ),
        string,
        count=1
        )


def equipment_sub(string, equipment):
    return sub(
        equipment,
        r"@Compendium[pf2e.equipment-srd.%s]{%s}" % (equipment, equipment),
        string,
        count=1
    )


def feat_sub(string, feat):
    return sub(
        feat,
        r"@Compendium[pf2e.feats-srd.%s]{%s}" % (feat, feat),
        string,
        count=1
    )


def spell_sub(string, spell):
    return sub(
        spell,
        r"<em>@Compendium[pf2e.spells-srd.%s]{%s}</em>" % (spell, spell),
        string,
        count=1
    )


def handle_actions(string):
    for action in constants.INLINE_ACTIONS:
        string = inline_action_sub(string, action)

    for action in constants.LINKED_ACTIONS:
        string = action_sub(string, action)

    return string


def handle_conditions(string, condition_list, numbered_condition_list):
    for condition in condition_list:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = sub(
        r"flat footed",
        r"%sFlat-Footed]" % constants.CONDITION_COMPENDIUM,
        string,
        count=1
    )
    # Catch flat-footed and turn it into off-guard.
    # Eventually this will be swapped.
    # string = sub(
    #   r"off-guard",
    #   r"@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]",
    #   string,
    #   count=1
    # )
    string = sub(r"{Flat-Footed}", "", string)

    for condition in numbered_condition_list:
        for i in range(1, 6):
            string = condition_sub_with_stage(string, condition, i)
    return string


def handle_equipment(string):
    for equipment in constants.EQUIPMENT:
        string = equipment_sub(string, equipment)
    return string


def handle_feats(string):
    for feat in constants.FEATS:
        string = feat_sub(string, feat)
    return string


def handle_spells(string):
    for spell in constants.SPELLS:
        string = spell_sub(string, spell)
    return string


def handle_activation_actions(string):
    for pair in constants.ACTIVATION_ACTIONS:
        string = sub(
            pair[0],
            r"<span class='pf2-icon'>%s</span>" % pair[1],
            string)
    return string


def handle_damage_rolls(string):
    for pair in constants.DAMAGE_ROLLS:
        string = sub(*pair, string)

    string = string.replace("@Damage[0[healing]]", "0")

    if "@Template" in string:
        string = sub(
            r"@Damage\[(.*?)\]\]", r"@Damage[\1]|options:area-damage]", string
        )

    string = sub(
        r"(\d+)d(\d+) (\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string
    )

    string = string.replace(r"[negative]", r"[void]")
    string = string.replace(r"[positive]", r"[vitality]")
    return string


def handle_spell_heightening(string):
    string = sub(r"Heightened \(", r"<hr />Heightened (", string, count=1)
    string = sub(
        r"Heightened \(\+(\d+)\)",
        r"</p><p><strong>Heightened (+\1)</strong>",
        string
    )
    string = sub(
        r"Heightened \((\d+)(\w+)\)",
        r"</p><p><strong>Heightened (\1\2)</strong>",
        string
    )
    string = sub(
        r"<hr /></p><p><strong>Heightened",
        r"</p><hr /><p><strong>Heightened",
        string
    )
    return string


def handle_level_heightening(string):
    string = sub(r"Level \(", r"<hr />Level (", string, count=1)
    string = sub(
        r"Level \(\+(\d+)\)",
        r"</p><p><strong>Level (+\1)</strong>",
        string
    )
    string = sub(
        r"Level \((\d+)(\w+)\)",
        r"</p><p><strong>Level (\1\2)</strong>",
        string
    )
    string = sub(
        r"<hr /></p><p><strong>Level",
        r"</p><hr /><p><strong>Level",
        string
    )
    return string


def handle_bullet_lists(string):
    # Removing bullet points, should replace with the actual bullet points.
    string = sub(r"•", "<ul><li>", string, count=1)
    string = sub(r"•", "</li><li>", string)
    return string


def handle_templates(string):
    # Add template buttons
    string = sub(
        r"(\d+)-(foot|Foot) %s" % constants.TEMPLATES,
        r"@Template[type:\3|distance:\1]",
        string
    )
    string = sub(
        r"(\d+)-(foot|Foot)-%s" % constants.TEMPLATES,
        r"@Template[type:\3|distance:\1]",
        string
    )
    string = sub(
        r"type:%s" % r"(Emanation|Burst|Cone|Line)",
        convert_to_lower,
        string
    )

    return string


def handle_third_party(string):
    # Handling for 3rd party formatting.
    string = sub(r"Accuracy \(", r"<strong>Accuracy</strong> (", string)
    string = sub(r"Damage \(", r"<strong>Damage</strong> (", string)
    string = sub(r"Defence \(", r"<strong>Defence</strong> (", string)
    string = sub(r"Hit Points \(", r"<strong>Hit Points</strong> (", string)
    string = sub(r"Utility \(", r"<strong>Utility</strong> (", string)
    return string


def handle_background(string):
    string = sub(
        r"(?:Choose two ability boosts|Choose two attribute boosts).",
        r"</p><p>Choose two attribute boosts.",
        string
    )

    string = sub(
        r"%s" % constants.ABILITY_SCORES,
        r"<strong>\1</strong>",
        string,
        count=2
    )
    string = sub(r"You're trained in", r"</p><p>You're trained in", string)
    # string = sub(
    #     r"You gain the (.*) skill feat",
    #     r"You gain the @Compendium[pf2e.feats-srd.\1]{\1} skill feat",
    #     string
    # )
    return string


def handle_aura(string):
    string = sub(
        r"<p>(\d+) feet.",
        (
            r"<p>@Template[type:emanation|distance:\1] "
            r"@Compendium[pf2e.bestiary-ability-glossary-srd.Aura]"
            r"{Aura}</p><p>"
        ),
        string)
    return string


def companion_format(string):
    MELEE = r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span>"
    string = sub(
        r"Size (Tiny|Small|Medium|Large)",
        r"<p><strong>Size</strong> \1</p>",
        string
    )
    string = sub(
        r"Melee \? (\w+)(,|;) Damage (\d+)d(\d+) (\w+)",
        r"%s \1,  <strong>Damage</strong> \3d\4 \5</p>" % MELEE,
        string
    )
    string = sub(
        r"Melee \? (\w+) \(([^\)]+)\)(,|;) Damage (\d+)d(\d+) (\w+)",
        r"%s \1 (\2), <strong>Damage</strong> \4d\5 \6</p>" % MELEE,
        string
        )
    string = sub(r"Str ", r"<p><strong>Str</strong> ", string)
    string = sub(r"(Dex|Con|Int|Wis|Cha) ", r"<strong>\1</strong> ", string)
    string = sub(
        r"Hit Points (\d+)", r"</p><p><strong>Hit Points</strong> \1</p>",
        string
    )
    string = sub(
        r"(Skill|Senses|Speed|Support Benefit|Advanced Maneuver)",
        r"</p><p><strong>\1</strong>",
        string
    )
    return string


def eidolon_format(string):
    string = sub(
        (
            r"(Tradition|Traits|Alignment|Home Plane|Size|Suggested "
            r"Attacks|Skills|Senses|Language|Speed|Eidolon Abilities)"
        ),
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        (
            r"(\w+) (\w+) Str (\d+), Dex (\d+), Con (\d+), Int (\d+), Wis "
            r"(\d+), Cha (\d+); \+(\d+) AC \(\+(\d+) Dex cap\)"
        ),
        (
            r"</p><p><strong>\1 \2</strong> Str \3, Dex \4, Con \5, Int \6, "
            r"Wis \7, Cha \8; +\9 AC (+\10 Dex cap)"
        ),
        string
    )
    return string


def handle_inlines_checks(string):
    # Skills and saves
    string = sub(
        r"%s basic (\w+) save" % constants.DC,
        r"@Check[\2|dc:\1|basic] save",
        string
    )
    string = sub(
        r"basic (\w+) save %s" % constants.DC,
        r"@Check[\1|dc:\2|basic] save",
        string
    )
    string = sub(
        r"basic (\w+) %s" % constants.DC,
        r"@Check[\1|dc:\2|basic]",
        string
        )
    string = sub(
        r"%s basic %s" % (constants.DC, constants.SAVES),
        r"@Check[\2|dc:\1|basic]",
        string
    )
    string = sub(
        r"%s %s" % (constants.DC, constants.SAVES),
        r"@Check[\2|dc:\1]",
        string
    )
    string = sub(
        r"%s %s" % (constants.SAVES, constants.DC),
        r"@Check[\1|dc:\2]",
        string
    )
    string = sub(
        r"%s \(%s\)" % (constants.SAVES, constants.DC),
        r"@Check[\1|dc:\2]",
        string
    )
    string = sub(
        r"%s save \(%s\)" % (constants.SAVES, constants.DC),
        r"@Check[\1|dc:\2] save",
        string
    )

    string = sub(
        r"%s %s or %s" % (constants.DC, constants.SKILLS, constants.SKILLS),
        r"@Check[\2|dc:\1] or @Check[\3|dc:\1]",
        string
    )
    string = sub(
        r"%s %s (trained|expert|master|legendary) or %s" % (
            constants.DC,
            constants.SKILLS,
            constants.SKILLS
        ),
        r"@Check[\2|dc:\1] (\3) or @Check[\4|dc:\1]",
        string
    )
    string = sub(
        r"%s %s" % (constants.DC, constants.SKILLS),
        r"@Check[\2|dc:\1]",
        string
    )
    string = sub(
        r"%s %s" % (constants.SKILLS, constants.DC),
        r"@Check[\1|dc:\2]",
        string
    )
    string = sub(
        r"%s \(%s\)" % (constants.SKILLS, constants.DC),
        r"@Check[\1|dc:\2",
        string
    )

    string = sub(
        r"(\w+) Lore %s" % constants.DC,
        r"@Check[\2-lore|dc:\1]{\1 Lore}",
        string
    )
    string = sub(
        r"%s (\w+) save" % constants.DC,
        r"@Check[\2|dc:\1] save",
        string
    )
    string = sub(
        r"%s flat check" % constants.DC,
        r"@Check[flat|dc:\1]",
        string
    )

    string = sub(
        r"basic %s (save against your class DC or spell DC)" % constants.SAVES,
        r"@Check[\1|against:class-spell|basic] \2",
        string
    )
    string = sub(
        r"%s (save against your class DC or spell DC)" % constants.SAVES,
        r"@Check[\1|against:class-spell] \2",
        string
        )
    string = sub(
        r"basic %s (save against your class DC)" % constants.SAVES,
        r"@Check[\1|against:class|basic] \2",
        string
    )
    string = sub(
        r"%s (save against your class DC)" % constants.SAVES,
        r"@Check[\1|against:class] \2",
        string
    )

    # Escape
    string = sub(
        r"Escapes \(%s\)" % constants.DC,
        r"[[/act escape dc=\1]]{Escapes}",
        string
    )
    string = sub(
        r"Escape \(%s\)" % constants.DC,
        r"[[/act escape dc=\1]]",
        string
    )
    string = sub(
        r"Escape %s" % constants.DC,
        r"[[/act escape dc=\1]]",
        string
    )
    string = sub(
        r"Escape it \(%s\)" % constants.DC,
        r"[[/act escape dc=\1]] it",
        string
    )

    # Catch capitalized saves
    string = sub(r"\[%s" % constants.SAVES, convert_to_lower, string)
    string = sub(r"\[%s" % constants.SKILLS, convert_to_lower, string)

    # Lores - capture 1-2 words between 'DC ##' and 'Lore'
    string = sub(
        r"%s ((?:\w+\s+){1,2})Lore" % constants.DC,
        r"@Check[\2Lore|dc:\1]",
        string
    )

    return string


def handle_counteract(string):
    string = sub(
        r"counteract modifier of \+(\d+)",
        r"counteract modifier of [[/r 1d20+\1 #Counteract]]{+\1}",
        string
    )
    string = sub(
        r"counteract modifier \+(\d+)",
        r"counteract modifier [[/r 1d20+\1 #Counteract]]{+\1}",
        string
    )
    string = sub(
        r"Counteract modifier of \+(\d+)",
        r"Counteract modifier of [[/r 1d20+\1 #Counteract]]{+\1}",
        string
    )
    string = sub(
        r"Counteract modifier \+(\d+)",
        r"Counteract modifier [[/r 1d20+\1 #Counteract]]{+\1}",
        string
    )
    string = sub(
        r"\+(\d+) counteract modifier",
        r"[[/r 1d20+\1 #Counteract]]{+\1} counteract modifier",
        string
    )
    return string


def ancestry_format(string):
    string = sub(
        r"(?i)Y\s*O\s*U M\s*I\s*G\s*H\s*T\s*...",
        r"</p><h2>You Might...</h2>",
        string
    )
    string = sub(
        r"O\s*T\s*H\s*E\s*R\s*S P\s*R\s*O\s*B\s*A\s*B\s*L\s*Y\s*...",
        r"</ul><h2>Others Probably...</h2><ul>",
        string,
        flags=re.IGNORECASE
    )
    string = sub(
        (
            r"(?i)P\s*H\s*Y\s*S\s*I\s*C\s*A\s*L "
            r"D\s*E\s*S\s*C\s*R\s*I\s*P\s*T\s*I\s*O\s*N"
        ),
        r"</ul><h2>Physical Description</h2><p>",
        string
    )
    string = sub(
        r"(?i)S\s*O\s*C\s*I\s*E\s*T\s*Y",
        r"</p><h2>Society</h2><p>",
        string,
        count=1
    )
    string = sub(
        (
            r"(?i)A\s*L\s*I\s*G\s*N\s*M\s*E\s*N\s*T "
            r"A\s*N\s*D R\s*E\s*L\s*I\s*G\s*I\s*O\s*N"
        ),
        r"</p><h2>Alignment and religion</h2><p>",
        string
    )
    string = sub(
        r"NAMES",
        r"</p><h2>Names</h2><p>",
        string
    )
    string = sub(
        r"(?i)S\s*a\s*m\s*p\s*l\s*e N\s*a\s*m\s*e\s*S",
        r"</p><h3>Sample Names</h3><p>",
        string
    )
    return string


def handle_areas(string):
    string = sub(r" ([A-Z][0-9]{1,3})", r" <strong>\1</strong>", string)
    return string


def handle_innate_spell_links(string):
    string = sub(
        r"You can cast (\w+) (.*?) innate",
        r"You can cast <em>@Compendium[pf2e.spells-srd.\1]{\1}</em> \2 innate",
        string
    )
    return string


def handle_deities(string):
    string = sub(
        r"(Areas of Concern)",
        r"<strong>\1</strong>",
        string
    )
    string = sub(
        r"(Edicts)",
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        r"(Anathema)",
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        r"(Religious Symbol)",
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        r"(Sacred Animal)",
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        r"(Sacred Colors)",
        r"</p><p><strong>\1</strong>",
        string
    )
    string = sub(
        r"Divine Attribute",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Devotee Benefits",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Cleric Spells",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Divine Font",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Divine Sanctification",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Divine Skill",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Domains",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Alternate Domains",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    string = sub(
        r"Favored Weapon",
        r"</p><p><strong>REMOVE ME</strong>",
        string
    )
    return string


def remove_books(string):
    for book in constants.BOOK_TITLES:
        string = sub(r" \((Pathfinder |)%s (\d+)\)" % book, r"", string)

    string = sub(r" \(page (\d+)\)", r"", string)

    return string


def format_monster_parts(string):
    string = string.replace(
        "Monster Parts",
        "<h2>Suggested Monster Parts</h2><p><strong>Monster Parts</strong>"
    ).replace(
        "Eligible Refinements",
        "</p><p><strong>Eligible Refinements</strong>"
    ).replace(
        "Eligible Imbued Properties",
        "</p><p><strong>Eligible Imbued Properties</strong>"
    )

    return string


# Fix the links, until we have a better way to do it.
def fix_links(string):
    string = string.replace(
        "@Compendium[pf2e.conditionitems.Blinded]",
        "@UUID[Compendium.pf2e.conditionitems.Item.XgEqL1kFApUbl5Z2]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Fatigued]",
        "@UUID[Compendium.pf2e.conditionitems.Item.HL2l2VRSaQHu9lUw]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Confused]",
        "@UUID[Compendium.pf2e.conditionitems.Item.yblD8fOR1J8rDwEQ]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Concealed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.DmAIPqOBomZ7H95W]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Dazzled]",
        "@UUID[Compendium.pf2e.conditionitems.Item.TkIyaNPgTZFBCCuh]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Deafened]",
        "@UUID[Compendium.pf2e.conditionitems.Item.9PR9y0bi4JPKnHPR]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Flat-Footed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Off-Guard]",
        "@UUID[Compendium.pf2e.conditionitems.Item.AJh5ex99aV6VTggg]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Immobilized]",
        "@UUID[Compendium.pf2e.conditionitems.Item.eIcWbB5o3pP6OIMe]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Prone]",
        "@UUID[Compendium.pf2e.conditionitems.Item.j91X7x0XSomq8d60]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Unconscious]",
        "@UUID[Compendium.pf2e.conditionitems.Item.fBnFDH2MTzgFijKf]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Fascinated]",
        "@UUID[Compendium.pf2e.conditionitems.Item.AdPVz7rbaVSRxHFg]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Paralyzed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.6uEgoh53GbXuHpTF]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Quickened]",
        "@UUID[Compendium.pf2e.conditionitems.Item.nlCjDvLMf2EkV2dl]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Fleeing]",
        "@UUID[Compendium.pf2e.conditionitems.Item.sDPxOjQ9kx2RZE8D]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Restrained]",
        "@UUID[Compendium.pf2e.conditionitems.Item.VcDeM8A5oI6VqhbM]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Grabbed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.kWc1fhmv9LBiTuei]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Clumsy]",
        "@UUID[Compendium.pf2e.conditionitems.Item.i3OJZU2nk64Df3xm]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Doomed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.3uh1r86TzbQvosxv]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Drained]",
        "@UUID[Compendium.pf2e.conditionitems.Item.4D2KBtexWXa6oUMR]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Enfeebled]",
        "@UUID[Compendium.pf2e.conditionitems.Item.MIRkyAjyBeXivMa7]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Slowed]",
        "@UUID[Compendium.pf2e.conditionitems.Item.xYTAsEpcJE1Ccni3]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Frightened]",
        "@UUID[Compendium.pf2e.conditionitems.Item.TBSHQspnbcqxsmjL]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Sickened]",
        "@UUID[Compendium.pf2e.conditionitems.Item.fesd1n5eVhpCSS18]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Stunned]",
        "@UUID[Compendium.pf2e.conditionitems.Item.dfCMdR4wnpbYNTix]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Stupefied]",
        "@UUID[Compendium.pf2e.conditionitems.Item.e1XGnhKNSQIm5IXg]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Wounded]",
        "@UUID[Compendium.pf2e.conditionitems.Item.Yl48xTdMh3aeQYL2]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Glitching]",
        "@UUID[Compendium.sf2e.conditions.Item.6A2QDy8wRGCVQsSd]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Suppressed]",
        "@UUID[Compendium.sf2e.conditions.Item.enA7BxAjBb7ns1iF]"
    ).replace(
        "@Compendium[pf2e.conditionitems.Untethered]",
        "@UUID[Compendium.sf2e.conditions.Item.z1ucw4CLwLqHoAp3]"
    )

    return string


def preProcessSpellHeader(string):
    string = sub(
        r"\nRange (\d+) feet; (Targets|Target) (.*?)\n",
        r"<hr>",
        string
    )
    string = sub(r"\nRange (\d+) feet;\n", r"<hr>", string)
    string = sub(r"\nArea (\d+)-foot (\w+)\n", r"<hr>", string)
    string = sub(
        r"\nArea (\d+)-foot (\w+) (Targets|Target) (.*?)\n",
        r"<hr>",
        string
    )
    string = sub(r"Defense (\w+)\n", r"<hr>", string)
    string = sub(r"(<hr>)+", r"<hr>", string)

    return string


def eldamonMode(string):
    # Skills and saves
    string = sub(
        r"basic (\w+) save",
        r"@Check[\1|against:eldamon|basic] save",
        string,
        count=1
    )
    string = sub(
        r"(\w+) save",
        r"@Check[\1|against:eldamon] save",
        string,
        count=1
    )
    string = sub(
        (
            r"(@Damage\[1d(\d+)\[(\w+)\]\] damage) plus \1 for (each|every) "
            r"level you have"
        ),
        r"@Damage[(1+@actor.level)d\2[\3]]",
        string
    )
    string = sub(
        r"(melee|ranged) power attack roll",
        r"@Check[eldamon|defense:ac]{\1 power attack roll}",
        string,
        count=1
    )
    string = string.replace(r"roll}s", r"rolls}")

    return string


def reformat(
        text,
        third_party=False,
        companion=False,
        eidolon=False,
        ancestry=False,
        use_clipboard=True,
        add_gm_text=True,
        inline_rolls=True,
        starfinder_mode=False,
        add_conditions=True,
        add_actions=True,
        add_inline_checks=True,
        add_inline_templates=True,
        remove_non_ASCII=True,
        replacement_mode=False,
        monster_parts=False,
        eldamon_mode=False,
        deity=False
):
    # Initial handling not using regex.
    string = "<p>" + text
    string = preProcessSpellHeader(string)
    string = string.replace(
        "Trigger", "<p><strong>Trigger</strong>"
    ).replace(
        " ", " "
    ).replace(
        "\nCritical Success", "</p><hr /><p><strong>Critical Success</strong>"
    ).replace(
        "\nSuccess", "</p><p><strong>Success</strong>"
    ).replace(
        "\nFailure", "</p><p><strong>Failure</strong>"
    ).replace(
        "\nCritical Failure", "</p><p><strong>Critical Failure</strong>"
    ).replace(
        "\nSpecial", "</p><hr><p><strong>Special</strong>"
    ).replace(
        "-\n", "-"
    ).replace(
        "—\n", "—"
    ).replace(
        "\n", " "
    ).replace(
        "Frequency", "<p><strong>Frequency</strong>"
    ).replace(
        "Effect", "</p><hr /><p><strong>Effect</strong>"
    ).replace(
        "Cost", "<strong>Cost</strong>"
    ) + "</p>"
    string = string.replace(
        "<p><p>", "<p>"
    ).replace(
        "Maximum Duration", "</p><p><strong>Maximum Duration</strong>"
    ).replace(
        "Onset", "</p><p><strong>Onset</strong>"
    ).replace(
        "Saving Throw", "</p><p><strong>Saving Throw</strong>"
    ).replace(
        "Demoralise", "Demoralize"
    ).replace(
        "f at-footed", "flat-footed"
    ).replace(
        "Ef ect", "Effect"
    )  # Fix common Paizo pre-release PDF formatting errors

    if starfinder_mode:
        condition_list = constants.CONDITIONS + constants.SF_CONDITIONS
        numbered_condition_list = (constants.NUMBERED_CONDITIONS
                                   + constants.SF_NUMBERED_CONDITIONS)
    else:
        condition_list = constants.CONDITIONS
        numbered_condition_list = constants.NUMBERED_CONDITIONS

    if remove_non_ASCII:
        string = string.replace(
            "’", "'"
        ).replace(
            r"”", r'"'
        ).replace(
            r"“", r'"'
        )

    string = sub(
        r"(Requirements|Requirement)",
        r"</p><p><strong>Requirements</strong>",
        string
    )
    string = sub(
        r" Craft </p><p><strong>Requirements</strong>",
        r"</p><hr /><p><strong>Craft Requirements</strong>",
        string
    )

    string = sub(r"Stage (\d)", r"</p><p><strong>Stage \1</strong>", string)

    string = sub("Access", "<p><strong>Access</strong>", string, count=1)
    string = sub(r"Usage", r"<strong>Usage</strong>", string)
    string = sub(
        r"Activate \?",
        r"</p><p><strong>Activate</strong> <span class='pf2-icon'>1</span>",
        string
    )
    string = sub(
        r"Activate (\d+) (minute|minutes|hour|hours)",
        r"</p><p><strong>Activate</strong> \1 \2",
        string
    )
    string = sub(
        r"Activate—(.*?) \?",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>1</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) \[reaction\]",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>r</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) \[one-action\]",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>1</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) \[two-actions\]",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>2</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) \[three-actions\]",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>3</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) \[free-action\]",
        r"</p><p><strong>Activate—\1</strong> <span class='pf2-icon'>f</span>",
        string
    )
    string = sub(
        r"Activate—(.*?) (\d+) (minute|minutes|hour|hours)",
        r"</p><p><strong>Activate—\1</strong> \2 \3",
        string
    )
    string = string.replace(
        r"<p><strong></p>",
        r""
    )
    string = sub(
        r"Transcendence—(.*?) \((.*?)\) \?",
        (
            r"</p><p><strong>Transcendence—\1</strong> "
            r"<span class='pf2-icon'>1</span> (\2)"
        ),
        string
    )
    string = sub(
        r"Transcendence—(.*?) \?",
        (
            r"</p><p><strong>Transcendence—\1</strong> "
            r"<span class='pf2-icon'>1</span>"
        ),
        string
    )
    string = sub(
        r"Immanence",
        r"</p><p><strong>Immanence</strong>",
        string
    )
    string = sub(
        r"Lead by Example",
        "</p><p><strong>Lead by Example</strong>",
        string
    )
    string = sub(
        r"Graviton-Attuned",
        "</p><p><strong>Graviton-Attuned</strong>",
        string
    )
    string = sub(
        r"Photon-Attuned",
        "</p><p><strong>Photon-Attuned</strong>",
        string
    )
    string = sub(
        r"Awakening",
        r"</p><p><strong>Awakening</strong>",
        string
    )
    string = sub(
        r"\[(1|2|3|r|f)\]",
        r"<span class='pf2-icon'>\1</span>",
        string
    )

    string = sub(
        r"can't use (.*?) again for (\d)d(\d) rounds",
        r"can't use \1 again for [[/gmr \2d\3 #Recharge \1]]{\2d\3 rounds}",
        string
    )
    string = sub(
        r"can't (.*?) again for (\d)d(\d) rounds",
        r"can't \1 again for [[/gmr \2d\3 #Recharge \1]]{\2d\3 rounds}",
        string
    )
    string = sub(
        r" (\d)d(\d) (rounds|minutes|hours|days)",
        r" [[/gmr \1d\2 #\3]]{\1d\2 \3}",
        string
    )
    string = string.replace(
        r"or dispel magic (",
        r"or @UUID[Compendium.pf2e.spells-srd.Item.9HpwDN4MYQJnW0LG] ("
    )

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
        string = handle_conditions(
            string, condition_list, numbered_condition_list
        )

    if add_inline_templates:
        string = handle_templates(string)

    if inline_rolls:
        string = handle_damage_rolls(string)

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

    if deity:
        string = handle_deities(string)

    if any(
        _ in string for _ in [
            "Choose two ability boosts", "Choose two attribute boosts"
        ]
    ):
        string = handle_background(string)

    string = string.replace(" <p>", "</p><p>")
    string = string.replace(" </p>",  "</p>")
    string = string.replace(";</p>", "</p>")
    string = string.replace("<p> ", "<p>")
    string = string.replace("<p></p>", "").replace("<p><p>", "<p>")

    # Catch non-link references to flat footed.
    string = string.replace(
        "flat footed", "off-guard"
    ).replace(
        "flat-footed", "off-guard"
    )

    # Sneak attack features have different text requirements
    # so we undo some of the changes made:
    # string = sub(
    #     (
    #         r"deals an additional "
    #         r"\[\[/r {(\d)d(\d)}\[precision\]\]\]{(\d)d(\d) precision damage} "
    #         r"to @Compendium\[pf2e.conditionitems.Flat-Footed\]{Flat-Footed} "
    #         r"creatures."
    #     ),
    #     r"deals an additional \1d\2 precision damage to flat-footed creatures.",
    #     string
    # )

    if eldamon_mode:
        string = eldamonMode(string)

    if add_gm_text:
        string = string.replace(
            "<p><strong>Trigger</strong>",
            "<p data-visibility='gm'><strong>Trigger</strong>"
        )
        string = string.replace(
            "<p><strong>Requirements</strong>",
            "<p data-visibility='gm'><strong>Requirements</strong>"
        )
        string = string.replace(
            "<p><strong>Frequency</strong>",
            "<p data-visibility='gm'><strong>Frequency</strong>"
        )

    # This is for text replacement without the wrapping <p></p> tags around
    # the entire block. Easiest to just strip them.
    if replacement_mode:
        string = string[3:]
        string = string[:-4]

    if starfinder_mode:
        string = string.replace("pf2e.conditionitems", "sf2e.conditions").replace("pf2e.actionspf2e","sf2e.actions")

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

root.title("PF2e on Foundry VTT Data Entry v 2.35")

canvas = Canvas(root, height=Height, width=Width)
canvas.pack()

frame = Frame(root, bg='#80c0ff')
frame.place(relwidth=1, relheight=1)

inputText = Text(frame, bg='white')
inputText.place(rely=0.2, relwidth=0.49, relheight=0.8)

outputText = Text(frame, bg='white')
outputText.place(relx=0.51, rely=0.2, relwidth=0.49, relheight=0.8)

# Settings
###############################################################################
third_party = BooleanVar(value=False)
monster_parts = BooleanVar(value=False)
companion = BooleanVar(value=False)
eidolon = BooleanVar(value=False)
ancestry = BooleanVar(value=False)
replacement_mode = BooleanVar(value=False)
use_clipboard = BooleanVar(value=True)
add_gm_text = BooleanVar(value=False)
inline_rolls = BooleanVar(value=True)
add_conditions = BooleanVar(value=True)
add_actions = BooleanVar(value=True)
add_inline_checks = BooleanVar(value=True)
starfinder_mode = BooleanVar(value=False)
add_inline_templates = BooleanVar(value=True)
remove_non_ASCII = BooleanVar(value=True)
eldamon_mode = BooleanVar(value=False)
deity = BooleanVar(value=False)
###############################################################################


# Build settings menu
##############################################################################

menu = Menu(root)

settings_menu = Menu(menu)
settings_menu.add_checkbutton(
    label="Copy Output to Clipboard",
    variable=use_clipboard
)
settings_menu.add_checkbutton(
    label="Add GM Only Tags",
    variable=add_gm_text
)
settings_menu.add_checkbutton(
    label="Handle Inline rolls",
    variable=inline_rolls
)
settings_menu.add_checkbutton(
    label="Handle Starfinder 2e formatting",
    variable=starfinder_mode
)
settings_menu.add_checkbutton(
    label="Add Inline Templates",
    variable=add_inline_templates
)
settings_menu.add_checkbutton(
    label="Add Inline Checks",
    variable=add_inline_checks
)
settings_menu.add_checkbutton(
    label="Add Condition Links",
    variable=add_conditions
)
settings_menu.add_checkbutton(
    label="Handle Deity Formatting",
    variable=deity
)
settings_menu.add_checkbutton(
    label="Add Action Links",
    variable=add_actions
)
settings_menu.add_checkbutton(
    label="Remove non-ASCII characters",
    variable=remove_non_ASCII
)
settings_menu.add_checkbutton(
    label="No Wrapping <p> tags",
    variable=replacement_mode
)
settings_menu.add_checkbutton(
    label="Handle Animal Companion Blocks",
    variable=companion
)
settings_menu.add_checkbutton(
    label="Handle Eidolon Blocks",
    variable=eidolon
    )
settings_menu.add_checkbutton(
    label="Handle Ancestry Description Text",
    variable=ancestry
)
settings_menu.add_checkbutton(
    label="Handle Third Party Formatting (legacy)",
    variable=third_party
)
settings_menu.add_checkbutton(
    label="Handle Monster Part Formatting (third party)",
    variable=monster_parts
)
settings_menu.add_checkbutton(
    label="Handle Eldamon Powers (third party)",
    variable=eldamon_mode
)

menu.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menu)

##############################################################################

reformatButton = Button(
    root,
    text="Reformat Text",
    command=lambda: reformat(
        inputText.get("1.0", "end-1c"),
        third_party.get(),
        companion.get(),
        eidolon.get(),
        ancestry.get(),
        use_clipboard.get(),
        add_gm_text.get(),
        inline_rolls.get(),
        starfinder_mode.get(),
        add_conditions.get(),
        add_actions.get(),
        add_inline_checks.get(),
        add_inline_templates.get(),
        remove_non_ASCII.get(),
        replacement_mode.get(),
        monster_parts.get(),
        eldamon_mode.get(),
        deity.get()
    )
)
reformatButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.2)

resetButton = Button(root, text="Clear Input", command=lambda: clearInput())
resetButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.2)


def main():
    # reformat(
    #   input(),
    #   third_party=False,
    #   companion=False,
    #   eidolon=False,
    #   ancestry=False,
    #   use_clipboard=True,
    #   add_gm_text=False,
    #   inline_rolls=True,
    #   add_conditions=True,
    #   add_inline_checks=True,
    #   add_inline_templates=True,
    #   remove_non_ASCII=True
    # )
    root.mainloop()


if __name__ == "__main__":
    main()
