import regex as re
import pyperclip as cl

from constants import *


def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def action_sub(string, action):
    return re.sub(r"\b" + action + r"\b", r"@Compendium[pf2e.actionspf2e.%s]{%s}" % (action, action), string, count=1)


def condition_sub(string, condition):
    return re.sub(condition.lower(), r"%s%s]{%s}" % (CONDITION_COMPENDIUM, condition, condition), string, count=1)


def condition_sub_with_stage(string, condition, stage):
    return re.sub(r"%s %s" % (condition.lower(), stage),
                  r"%s%s]{%s %s}" % (CONDITION_COMPENDIUM, condition, condition, stage),
                  string, count=1)


def equipment_sub(string, equipment):
    return re.sub(equipment, r"@Compendium[pf2e.equipment-srd.%s]{%s}" % (equipment, equipment), string, count=1)


def feat_sub(string, feat):
    return re.sub(feat, r"@Compendium[pf2e.feats-srd.%s]{%s}" % (feat, feat), string, count=1)


def spell_sub(string, spell):
    return re.sub(spell, r"<em>@Compendium[pf2e.spells-srd.%s]{%s}</em>" % (spell, spell), string, count=1)


def handle_actions(string):
    for action in ACTIONS:
        string = action_sub(string, action)
    return string


def handle_conditions(string):
    for condition in CONDITIONS:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = re.sub(r"flat footed", r"%sFlat-Footed]{Flat-Footed}" % CONDITION_COMPENDIUM, string, count=1)

    for condition in NUMBERED_CONDITIONS:
        for i in range(1, 4):
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
    string = re.sub(r"\[free-action\]", r"<span class=\"pf2-icon\">F</span>", string)
    string = re.sub(r"\[reaction\]", r"<span class=\"pf2-icon\">R</span>", string)
    string = re.sub(r"\[one-action\]", r"<span class=\"pf2-icon\">1</span>", string)
    string = re.sub(r"\[two-actions\]", r"<span class=\"pf2-icon\">2</span>", string)
    string = re.sub(r"\[three-actions\]", r"<span class=\"pf2-icon\">3</span>", string)
    return string


def handle_damage_rolls(string):
    string = re.sub(r" (\d)d(\d) (rounds|minutes|hours|days)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = re.sub(r" (\d+) (\w*) damage", r" [[/r {\1}[\2]]]{\1 \2 Damage}", string)
    string = re.sub(r"(\d+)d(\d+)\+(\d+) (\w*) damage", r"[[/r {\1d\2 + \3}[\4]]]{\1d\2 + \3 \4 damage}", string)
    string = re.sub(r"(\d+)d(\d+) persistent (\w*) damage",
                    r"[[/r {\1d\2}[persistent,\3]]]{\1d\2} %sPersistent Damage]{Persistent \3 Damage}"
                    % CONDITION_COMPENDIUM, string)
    string = re.sub(r"(\d+)d(\d+) (\w*) damage", r"[[/r {\1d\2}[\3]]]{\1d\2 \3 damage}", string)
    string = re.sub(r"(\d+)d(\d+) (\w+)(\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = re.sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]]{\1d\2}.", string)
    return string


def handle_spell_heightening(string):
    string = re.sub(r"Heightened \(", r"<hr />Heightened (", string, count=1)
    string = re.sub(r"Heightened \(\+(\d+)\)", r"</p><p><strong>Heightened (+\1)</strong>", string)
    string = re.sub(r"Heightened \((\d+)(\w+)\)", r"</p><p><strong>Heightened (\1\2)</strong>", string)
    string = re.sub(r"<hr /></p><p><strong>Heightened", r"</p><hr /><p><strong>Heightened", string)
    return string


def handle_bullet_lists(string):
    # Removing bullet points, should replace with the actual bullet points.
    string = re.sub(r"•", "<ul><li>", string, count=1)
    string = re.sub(r"•", "</li><li>", string)
    return string

def handle_templates(string):
    # Add template buttons
    string = re.sub(r"(\d+)-foot (emanation|burst|cone|line)", r"@Template[type:\2|distance:\1]", string)
    # string = re.sub(r"(\d+)-foot (emanation|burst|cone|line)", r"<span data-pf2-effect-area='\2' data-pf2-distance='\1' data-pf2-traits=''>\1-foot \2</span>", string)
    return string

def handle_third_party(string):
    # Handling for 3rd party formatting.
    string = re.sub(r"» (Critical Success|Success|Failure|Critical Failure)", r"</p><p><strong>\1</strong>", string)
    string = re.sub(r"»", r"•", string)
    return string

def handle_background(string):
    string = re.sub(r"Choose two ability boosts.", r"</p><p>Choose two ability boosts.", string)
    string = re.sub(r"%s" % ABILITY_SCORES, r"<strong>\1</strong>", string, count=2)
    string = re.sub(r"You're trained in", r"</p><p>You're trained in", string)
    string = re.sub(r"You gain the (.*) skill feat",r"You gain the @Compendium[pf2e.feats-srd.\1]{\1} skill feat",string)
    return string

def handle_aura(string):
    string = re.sub(r"<p>(\d+) feet.",r"<p>@Template[type:emanation|distance:\1] @Compendium[pf2e.bestiary-ability-glossary-srd.Aura]{Aura}</p><p>", string)
    return string

def companion_format(string):
    string = re.sub(r"Size (Tiny|Small|Medium|Large)", r"<p><strong>Size</strong> \1</p>", string)
    string = re.sub(r"Melee \? (\w+)(,|;) Damage (\d+)d(\d+) (\w+)", r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1, <strong>Damage</strong> \3d\4 \5</p>", string)
    string = re.sub(r"Melee \? (\w+) \(([^\)]+)\)(,|;) Damage (\d+)d(\d+) (\w+)", r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1 (\2), <strong>Damage</strong> \4d\5 \6</p>", string)
    string = re.sub(r"Str ", r"<p><strong>Str</strong> ", string)
    string = re.sub(r"(Dex|Con|Int|Wis|Cha) ", r"<strong>\1</strong> ", string)
    string = re.sub(r"Hit Points (\d+)", r"</p><p><strong>Hit Points</strong> \1</p>", string)
    string = re.sub(r"(Skill|Senses|Speed|Support Benefit|Advanced Maneuver)", r"</p><p><strong>\1</strong>", string)
    
    return string

def eidolon_format(string):
    string = re.sub(r"(Tradition|Traits|Alignment|Home Plane|Size|Suggested Attacks|Skills|Senses|Language|Speed|Eidolon Abilities)", r"</p><p><strong>\1</strong>", string)
    string = re.sub(r"(\w+) (\w+) Str (\d+), Dex (\d+), Con (\d+), Int (\d+), Wis (\d+), Cha (\d+); \+(\d+) AC \(\+(\d+) Dex cap\)", r"</p><p><strong>\1 \2</strong> Str \3, Dex \4, Con \5, Int \6, Wis \7, Cha \8; +\9 AC (+\10 Dex cap)", string)
    
    return string

def handle_inlines_checks(string):
    
    # Skills and saves
    string = re.sub(r"%s basic (\w+) save" % DC, r"@Check[type:\2|dc:\1|basic:true]", string)
    string = re.sub(r"%s %s" % (DC, SAVES), r"@Check[type:\2|dc:\1]", string)
    string = re.sub(r"%s %s" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = re.sub(r"%s \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = re.sub(r"%s save \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)

    string = re.sub(r"%s %s" % (DC, SKILLS), r"@Check[type:\2|dc:\1]", string)
    string = re.sub(r"%s %s" % (SKILLS, DC), r"@Check[type:\1|dc:\2]", string)
    string = re.sub(r"%s \(%s\)" % (SKILLS, DC), r"@Check[type:\1|dc:\2", string)

    string = re.sub(r"(\w+) Lore %s" % DC, r"@Check[type:\2|dc:\1]", string)
    string = re.sub(r"%s (\w+) save" % DC, r"@Check[type:\2|dc:\1]", string)
    string = re.sub(r"%s flat check" % DC, r"@Check[type:flat|dc:\1]", string)

    # Catch capitalized saves
    string = re.sub(r"type:%s" % SAVES, convert_to_lower, string)
    string = re.sub(r"type:%s" % SKILLS, convert_to_lower, string)
    
    return string

def reformat(text, use_clipboard=False):
    # Initial handling not using regex.
    string = "<p>" + text.replace("’", "'")\
        .replace("Trigger", "<p><strong>Trigger</strong>")\
        .replace("Requirements", "<p><strong>Requirements</strong>")\
        .replace("\nCritical Success", "</p><hr /><p><strong>Critical Success</strong>")\
        .replace("\nSuccess", "</p><p><strong>Success</strong>")\
        .replace("\nFailure", "</p><p><strong>Failure</strong>")\
        .replace("\nCritical Failure", "</p><p><strong>Critical Failure</strong>")\
        .replace("\nSpecial", "</p><p><strong>Special</strong>")\
        .replace("\n", " ")\
        .replace("Frequency", "<p><strong>Frequency</strong>")\
        .replace("Effect", "</p><p><strong>Effect</strong>")\
        .replace("—", "-")\
        .replace("Cost", "<strong>Cost</strong>") + "</p>"
    string = string.replace("<p><p>", "<p>")\
        .replace("–", "-")\
        .replace(r"”", r"\"")\
        .replace(r"“", r"\"")\
        .replace("Maximum Duration", "</p><p><strong>Maximum Duration</strong>")\
        .replace("Onset", "</p><p><strong>Onset</strong>")\
        .replace("Saving Throw", "</p><p><strong>Saving Throw</strong>")
    string = re.sub(r"Stage (\d)", r"</p><p><strong>Stage \1</strong>", string)
    string = string.replace(";</p>","</p>")
    string = string.replace(" <p>","</p><p>")
    string = string.replace(" </p>", "</p>")

    string = re.sub("Access", "<p><strong>Access</strong>", string, count=1)
    string = re.sub(r"Activate \?", r"</p><p><strong>Activate</strong> <span class='pf2-icon'>1</span>", string)

    # Uncomment for third party formatting
    # string = handle_third_party(string)
    
    # Uncomment for handling animal companion blocks
    # string = companion_format(string)
    
    # Uncomment for handling eidolon blocks
    # string = eidolon_format(string)
    
    string = handle_inlines_checks(string)

    string = handle_damage_rolls(string)
    string = handle_spell_heightening(string)
    string = handle_bullet_lists(string)
    string = handle_templates(string)
    
    string = handle_actions(string)
    string = handle_conditions(string)
    string = handle_equipment(string)
    string = handle_feats(string)
    string = handle_spells(string)
    string = handle_activation_actions(string)
    string = handle_aura(string)

    if "Choose two ability boosts" in string:
        string = handle_background(string)
        
    string = string.replace("<p></p>","").replace("<p><p>","<p>")

    print("\n")
    print(string)
    if use_clipboard:
        cl.copy(string)

    return string


def main():
    reformat(input(), use_clipboard=True)


if __name__ == "__main__":
    main()
