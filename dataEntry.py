from regex import sub
from pyperclip import copy
from tkinter import Tk, Frame, Canvas, Text, Button, END, BooleanVar, Menu

from constants import *


def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def action_sub(string, action):
    return sub(r"\b" + action + r"\b", r"@Compendium[pf2e.actionspf2e.%s]{%s}" % (action, action), string, count=1)


def condition_sub(string, condition):
    return sub(condition.lower(), r"%s%s]{%s}" % (CONDITION_COMPENDIUM, condition, condition), string, count=1)


def condition_sub_with_stage(string, condition, stage):
    return sub(r"%s %s" % (condition.lower(), stage),
                  r"%s%s]{%s %s}" % (CONDITION_COMPENDIUM, condition, condition, stage),
                  string, count=1)


def equipment_sub(string, equipment):
    return sub(equipment, r"@Compendium[pf2e.equipment-srd.%s]{%s}" % (equipment, equipment), string, count=1)


def feat_sub(string, feat):
    return sub(feat, r"@Compendium[pf2e.feats-srd.%s]{%s}" % (feat, feat), string, count=1)


def spell_sub(string, spell):
    return sub(spell, r"<em>@Compendium[pf2e.spells-srd.%s]{%s}</em>" % (spell, spell), string, count=1)


def handle_actions(string):
    for action in ACTIONS:
        string = action_sub(string, action)
    return string


def handle_conditions(string):
    for condition in CONDITIONS:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = sub(r"flat footed", r"%sFlat-Footed]{Flat-Footed}" % CONDITION_COMPENDIUM, string, count=1)

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
    string = sub(r"\[free-action\]", r"<span class=\"pf2-icon\">F</span>", string)
    string = sub(r"\[reaction\]", r"<span class=\"pf2-icon\">R</span>", string)
    string = sub(r"\[one-action\]", r"<span class=\"pf2-icon\">1</span>", string)
    string = sub(r"\[two-actions\]", r"<span class=\"pf2-icon\">2</span>", string)
    string = sub(r"\[three-actions\]", r"<span class=\"pf2-icon\">3</span>", string)
    return string


def handle_damage_rolls(string):
    string = sub(r" (\d)d(\d) (rounds|minutes|hours|days)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = sub(r" (\d+) (\w*) damage", r" [[/r {\1}[\2]]]{\1 \2 Damage}", string)
    string = sub(r"(\d+)d(\d+)\+(\d+) (\w*) damage", r"[[/r {\1d\2 + \3}[\4]]]{\1d\2 + \3 \4 damage}", string)
    string = sub(r"(\d+)d(\d+) persistent (\w*) damage",
                    r"[[/r {\1d\2}[persistent,\3]]]{\1d\2} %sPersistent Damage]{Persistent \3 Damage}"
                    % CONDITION_COMPENDIUM, string)
    string = sub(r"(\d+)d(\d+) (\w*) damage", r"[[/r {\1d\2}[\3]]]{\1d\2 \3 damage}", string)
    string = sub(r"(\d+)d(\d+) (\w+)(\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]]{\1d\2}.", string)
    return string


def handle_spell_heightening(string):
    string = sub(r"Heightened \(", r"<hr />Heightened (", string, count=1)
    string = sub(r"Heightened \(\+(\d+)\)", r"</p><p><strong>Heightened (+\1)</strong>", string)
    string = sub(r"Heightened \((\d+)(\w+)\)", r"</p><p><strong>Heightened (\1\2)</strong>", string)
    string = sub(r"<hr /></p><p><strong>Heightened", r"</p><hr /><p><strong>Heightened", string)
    return string


def handle_bullet_lists(string):
    # Removing bullet points, should replace with the actual bullet points.
    string = sub(r"•", "<ul><li>", string, count=1)
    string = sub(r"•", "</li><li>", string)
    return string

def handle_templates(string):
    # Add template buttons
    string = sub(r"(\d+)-foot (emanation|burst|cone|line)", r"@Template[type:\2|distance:\1]", string)
    # string = sub(r"(\d+)-foot (emanation|burst|cone|line)", r"<span data-pf2-effect-area='\2' data-pf2-distance='\1' data-pf2-traits=''>\1-foot \2</span>", string)
    return string

def handle_third_party(string):
    # Handling for 3rd party formatting.
    string = sub(r"» (Critical Success|Success|Failure|Critical Failure)", r"</p><p><strong>\1</strong>", string)
    string = sub(r"»", r"•", string)
    return string

def handle_background(string):
    string = sub(r"Choose two ability boosts.", r"</p><p>Choose two ability boosts.", string)
    string = sub(r"%s" % ABILITY_SCORES, r"<strong>\1</strong>", string, count=2)
    string = sub(r"You're trained in", r"</p><p>You're trained in", string)
    string = sub(r"You gain the (.*) skill feat",r"You gain the @Compendium[pf2e.feats-srd.\1]{\1} skill feat",string)
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
    string = sub(r"%s basic (\w+) save" % DC, r"@Check[type:\2|dc:\1|basic:true]", string)
    string = sub(r"%s %s" % (DC, SAVES), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s save \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)

    string = sub(r"%s %s" % (DC, SKILLS), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SKILLS, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SKILLS, DC), r"@Check[type:\1|dc:\2", string)

    string = sub(r"(\w+) Lore %s" % DC, r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s (\w+) save" % DC, r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s flat check" % DC, r"@Check[type:flat|dc:\1]", string)

    # Catch capitalized saves
    string = sub(r"type:%s" % SAVES, convert_to_lower, string)
    string = sub(r"type:%s" % SKILLS, convert_to_lower, string)
    
    return string

def ancestry_format(string):
    string = sub(r"YOU MIGHT...",r"</p><h2>You Might...</h2>", string)
    string = sub(r"OTHERS PROBABLY...",r"</ul><h2>Others Probably...</h2><ul>", string)
    string = sub(r"PHYSICAL DESCRIPTION",r"</ul><h2>Physical Description</h2><p>", string)
    string = sub(r"SOCIETY",r"</p><h2>Society</h2><p>", string)
    string = sub(r"ALIGNMENT AND RELIGION",r"</p><h2>Alignment and religion</h2><p>", string)
    string = sub(r"NAMES",r"</p><h2>Names</h2><p>", string)
    string = sub(r"S ample N ameS",r"</p><h3>Sample Names</h3><p>", string)
    
    return string

def reformat(text, third_party = False, companion = False, eidolon = False, ancestry = False, use_clipboard=True, add_gm_text = True, inline_rolls = True, add_conditions = True, add_inline_checks = True, add_inline_templates = True, remove_non_ASCII = True):
    # Initial handling not using regex.
    string = "<p>" + text.replace("Trigger", "<p><strong>Trigger</strong>")\
        .replace("Requirements", "<p><strong>Requirements</strong>")\
        .replace("\nCritical Success", "</p><hr /><p><strong>Critical Success</strong>")\
        .replace("\nSuccess", "</p><p><strong>Success</strong>")\
        .replace("\nFailure", "</p><p><strong>Failure</strong>")\
        .replace("\nCritical Failure", "</p><p><strong>Critical Failure</strong>")\
        .replace("\nSpecial", "</p><p><strong>Special</strong>")\
        .replace("\n", " ")\
        .replace("Frequency", "<p><strong>Frequency</strong>")\
        .replace("Effect", "</p><p><strong>Effect</strong>")\
        .replace("Cost", "<strong>Cost</strong>") + "</p>"
    string = string.replace("<p><p>", "<p>")\
        .replace(r"”", r"\"")\
        .replace(r"“", r"\"")\
        .replace("Maximum Duration", "</p><p><strong>Maximum Duration</strong>")\
        .replace("Onset", "</p><p><strong>Onset</strong>")\
        .replace("Saving Throw", "</p><p><strong>Saving Throw</strong>")
        
    if remove_non_ASCII:
        string = string.replace("–", "-").replace("’", "'")
    
    string = sub(r"Stage (\d)", r"</p><p><strong>Stage \1</strong>", string)

    string = sub("Access", "<p><strong>Access</strong>", string, count=1)
    string = sub(r"Activate \?", r"</p><p><strong>Activate</strong> <span class='pf2-icon'>1</span>", string)

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
        string = handle_conditions(string)

    if inline_rolls:
        string = handle_damage_rolls(string)
    
    if add_inline_templates:
        string = handle_templates(string)
    
    string = handle_spell_heightening(string)
    string = handle_bullet_lists(string)
    
    string = handle_actions(string)
    
    string = handle_equipment(string)
    string = handle_feats(string)
    string = handle_spells(string)
    
    string = handle_activation_actions(string)
    string = handle_aura(string)
    

    if "Choose two ability boosts" in string:
        string = handle_background(string)
        
    string = string.replace("<p></p>","").replace("<p><p>","<p>")
    string = string.replace(" <p>","</p><p>")
    string = string.replace(" </p>", "</p>")
    string = string.replace(";</p>","</p>")
    
            
    if add_gm_text:
        string = string.replace("<p><strong>Trigger</strong>", "<p data-visibility='gm'><strong>Trigger</strong>")
        string = string.replace("<p><strong>Requirements</strong>", "<p data-visibility='gm'><strong>Requirements</strong>")
        string = string.replace("<p><strong>Frequency</strong>", "<p data-visibility='gm'><strong>Frequency</strong>")

    print("\n")
    print(string)

    if use_clipboard:
        copy(string)

    return string
    # outputText.delete("1.0", END)
    # outputText.insert(END, string)
    
# def clearInput():
#     inputText.delete("1.0", END)

# Height = 700
# Width = 800

# root = Tk()



# root.title("PF2e on Foundry VTT Data Entry v 2.1")

# canvas = Canvas(root, height = Height, width = Width)
# canvas.pack()

# frame = Frame(root, bg = '#80c0ff')
# frame.place(relwidth = 1, relheight = 1)

# inputText = Text(frame, bg = 'white')
# inputText.place(rely = 0.2, relwidth = 0.49, relheight = 0.8)

# outputText = Text(frame, bg = 'white')
# outputText.place(relx = 0.51, rely = 0.2, relwidth = 0.49, relheight = 0.8)

## Settings
###############################################################################
# third_party = BooleanVar()
# companion = BooleanVar()
# eidolon = BooleanVar()
# ancestry = BooleanVar()
# use_clipboard = BooleanVar(value = True)
# add_gm_text = BooleanVar(value = True)
# inline_rolls = BooleanVar(value = True)
# add_conditions = BooleanVar(value = True)
# add_inline_checks = BooleanVar(value = True)
# add_inline_templates = BooleanVar(value = True)
# remove_non_ASCII = BooleanVar(value = True)

# handleThirdParty = Checkbutton(text = "Support Third Party", variable = third_party)
# handleThirdParty.place(relx = 0.3, rely= 0)

# handleCompanion = Checkbutton(text = "Animal Companion", variable = companion)
# handleCompanion.place(relx = 0.3, rely= 0.05)

# handleEidolon = Checkbutton(text = "Eidolon", variable = eidolon)
# handleEidolon.place(relx = 0.3, rely= 0.1)

# handleAncestry = Checkbutton(text = "Ancestry", variable = ancestry)
# handleAncestry.place(relx = 0.5, rely= 0.0)

# useClipboard = Checkbutton(text = "Copy Output to Clipboard", variable = use_clipboard)
# useClipboard.place(relx = 0.5, rely= 0.05)
###############################################################################


## Build settings menu
###############################################################################

# menu = Menu(root)

# settings_menu = Menu(menu)
# settings_menu.add_checkbutton(label = "Copy Output to Clipboard", variable = use_clipboard)
# settings_menu.add_checkbutton(label = "Add GM Only Tags", variable = add_gm_text)
# settings_menu.add_checkbutton(label = "Handle Inline rolls", variable = inline_rolls)
# settings_menu.add_checkbutton(label = "Add Inline Templates", variable = add_inline_templates)
# settings_menu.add_checkbutton(label = "Add Inline Checks", variable = add_inline_checks)
# settings_menu.add_checkbutton(label = "Add Condition Links", variable = add_conditions)
# settings_menu.add_checkbutton(label = "Remove non-ASCII characters", variable = remove_non_ASCII)
# settings_menu.add_checkbutton(label = "Handle Animal Companion Blocks", variable = companion)
# settings_menu.add_checkbutton(label = "Handle Eidolon Blocks", variable = eidolon)
# settings_menu.add_checkbutton(label = "Handle Ancestry Description Text", variable = ancestry)
# settings_menu.add_checkbutton(label = "Handle Third Party Formatting", variable = third_party)

# menu.add_cascade(label = "Settings", menu = settings_menu)
# root.config(menu = menu)


# ###############################################################################

# reformatButton = Button(root, text="Reformat Text", command = lambda: reformat(inputText.get("1.0", "end-1c"), third_party.get(), companion.get(), eidolon.get(), ancestry.get(), use_clipboard.get(), add_gm_text.get(), inline_rolls.get(), add_conditions.get(), add_inline_checks.get(), add_inline_templates.get(), remove_non_ASCII.get()))
# reformatButton.place(relx = 0.75, rely= 0, relwidth = 0.25, relheight = 0.2)

# resetButton = Button(root, text="Clear Input", command = lambda: clearInput())
# resetButton.place(relx = 0, rely= 0, relwidth = 0.25, relheight = 0.2)


def main():
    reformat(input(), third_party = False, companion = False, eidolon = False, ancestry = False, use_clipboard=True, add_gm_text = True, inline_rolls = True, add_conditions = True, add_inline_checks = True, add_inline_templates = True, remove_non_ASCII = True)
    # root.mainloop()


if __name__ == "__main__":
    main()