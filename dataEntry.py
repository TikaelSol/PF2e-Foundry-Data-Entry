import regex as re
import pyperclip as cl

DC = r"DC (\d+)"

ABILITY_SCORES = r"(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
SAVES = r"(Reflex|Will|Fortitude)"
SKILLS = r"(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|" \
         r"Occultism|Performance|Religion|Society|Stealth|Survival|Thievery)"

CONDITION_COMPENDIUM = r"@Compendium[pf2e.conditionitems."


def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def reformat(text):
    # Initial handling not using regex.
    string = "<p>" + text.replace("’","'")\
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
        .replace(r"“", r"\"")
    # string = string.replace("Activate", "</p><p><strong>Activate</strong>")

    string = string.replace("Maximum Duration", "</p><p><strong>Maximum Duration</strong>")\
        .replace("Onset", "</p><p><strong>Onset</strong>")\
        .replace("Saving Throw", "</p><p><strong>Saving Throw</strong>")
    string = re.sub(r"Stage (\d)", r"</p><p><strong>Stage \1</strong>", string)

    string = string.replace(" </p>", "</p>")

    string = re.sub(r"Activate \?", r"</p><p><strong>Activate</strong> <span class='pf2-icon'>1</span>", string)

    # Skills and saves
    string = re.sub(r"%s basic (\w+) save" % DC, r"<span data-pf2-check='\2' data-pf2-traits='damaging-effect' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>basic \2</span> save", string)
    string = re.sub(r"%s %s" % (DC, SAVES), r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span>", string)
    string = re.sub(r"%s %s" % (SAVES, DC), r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>", string)
    string = re.sub(r"%s \(%s\)" % (SAVES, DC), r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>", string)
    string = re.sub(r"%s save \(%s\)" % (SAVES, DC), r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>", string)

    string = re.sub(r"%s %s" % (DC, SKILLS), r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span>", string)
    string = re.sub(r"%s %s" % (SKILLS, DC), r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>", string)
    string = re.sub(r"%s \(%s\)" % (SKILLS, DC), r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>", string)

    string = re.sub(r"(\w+) Lore %s" % DC, r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2 Lore</span>", string)
    string = re.sub(r"%s (\w+) save" % DC, r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span> save", string)
    string = re.sub(r"%s flat check" % DC, r"<span data-pf2-check='flat' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='owner'>Flat Check</span>", string)

    # Catch capitalized saves
    string = re.sub("check='(%s'" % SAVES, convert_to_lower, string)
    string = re.sub(r"check='%s'" % SKILLS, convert_to_lower, string)

    # Damage rolls
    string = re.sub(r" (\d)d(\d) (rounds|minutes|hours|days)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = re.sub(r" (\d+) (\w*) damage", r" [[/r {\1}[\2] damage]]{\1 \2}", string)
    string = re.sub(r"(\d+)d(\d+)\+(\d+) (\w*) damage", r"[[/r {\1d\2 + \3}[\4]]]{\1d\2 + \3 \4 damage}", string)
    string = re.sub(r"(\d+)d(\d+) persistent (\w*) damage",
                    r"[[/r {\1d\2}[persistent,\3]]]{\1d\2} %sPersistent Damage]{Persistent \3 Damage}" % CONDITION_COMPENDIUM, string)
    string = re.sub(r"(\d+)d(\d+) (\w*) damage", r"[[/r {\1d\2}[\3]]]{\1d\2 \3 damage}", string)
    string = re.sub(r"(\d+)d(\d+) (\w+)(\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = re.sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]]{\1d\2}.", string)

    # Spell heightening handling
    string = re.sub(r"Heightened \(", r"<hr />Heightened (", string, count=1)
    string = re.sub(r"Heightened \(\+(\d+)\)", r"</p><p><strong>Heightened (+\1)</strong>", string)
    string = re.sub(r"Heightened \((\d+)(\w+)\)", r"</p><p><strong>Heightened (\1\2)</strong>", string)
    string = re.sub(r"<hr /></p><p><strong>Heightened", r"</p><hr /><p><strong>Heightened", string)

    # Removing bullet points, should replace with the actual bullet points.
    # string = re.sub(r"»", r"•", string)
    string = re.sub(r"•", "<ul><li>", string, count=1)
    string = re.sub(r"•", "</li><li>", string)

    # Add template buttons
    string = re.sub(r"(\d+)-foot (emanation|burst|cone|line)", r"@Template[type:\2|distance:\1]", string)
    # string = re.sub(r"(\d+)-foot (emanation|burst|cone|line)", r"<span data-pf2-effect-area='\2' data-pf2-distance='\1' data-pf2-traits=''>\1-foot \2</span>", string)

    # Condition handling
    string = re.sub(r"blinded", r"%sBlinded]{Blinded}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"fatigued", r"%sFatigued]{Fatigued}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"confused", r"%sConfused]{Confused}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"concealed", r"%sConcealed]{Concealed}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"dazzled", r"%sDazzled]{Dazzled}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"deafened", r"%sDeafened]{Deafened}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"invisible", r"%sInvisible]{Invisible}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"flat footed", r"%sFlat-Footed]{Flat-Footed}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"flat-footed", r"%sFlat-Footed]{Flat-Footed}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"immobilized", r"%sImmobilized]{Immobilized}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"prone", r"%sProne]{Prone}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"unconscious", r"%sUnconscious]{Unconscious}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"fascinated", r"%sFascinated]{Fascinated}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"paralyzed", r"%sParalyzed]{Paralyzed}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"hidden", r"%sHidden]{Hidden}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"quickened", r"%sQuickened]{Quickened}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"fleeing", r"%sFleeing]{Fleeing}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"restrained", r"%sRestrained]{Restrained}" % CONDITION_COMPENDIUM, string, count=1)
    string = re.sub(r"grabbed", r"%sGrabbed]{Grabbed}" % CONDITION_COMPENDIUM, string, count=1)
    
    for i in range(1, 4):
        string = re.sub(r"clumsy %s" % i, r"%sClumsy]{Clumsy %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"doomed %s" % i, r"%sDoomed]{Doomed %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"drained %s" % i, r"%sDrained]{Drained %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"enfeebled %s" % i, r"%sEnfeebled]{Enfeebled %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"slowed %s" % i, r"%sSlowed]{Slowed %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"frightened %s" % i, r"%sFrightened]{Frightened %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"sickened %s" % i, r"%sSickened]{Sickened %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"stunned %s" % i, r"%sStunned]{Stunned %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"stupefied %s" % i, r"%sStupefied]{Stupefied %s}" % (CONDITION_COMPENDIUM, i), string, count=1)
        string = re.sub(r"quickened %s" % i, r"%sQuickened]{Quickened %s}" % (CONDITION_COMPENDIUM, i), string, count=1)

    # #Comment out when not entering backgrounds.
    # string = re.sub(r"Choose two ability boosts.", r"</p><p>Choose two ability boosts.", string)
    # string = re.sub(r"%s" % ABILITY_SCORES, r"<strong>\1</strong>", string, count=2)
    # string = re.sub(r"You're trained in", r"</p><p>You're trained in", string)

    print("\n")
    print(string)
    cl.copy(string)


reformat(input())
