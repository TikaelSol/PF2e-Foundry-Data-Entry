DC = r"DC (\d+)"

ABILITY_SCORES = r"(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
SAVES = r"(Reflex|Will|Fortitude)"
SKILLS = r"(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|" \
         r"Occultism|Performance|Religion|Society|Stealth|Survival|Thievery)"

CONDITION_COMPENDIUM = r"@Compendium[pf2e.conditionitems."

CONDITIONS = ["Blinded", "Fatigued", "Confused", "Concealed", "Dazzled", "Deafened", "Invisible",
              "Flat-Footed", "Immobilized", "Prone", "Unconscious", "Fascinated", "Paralyzed",
              "Hidden", "Quickened", "Fleeing", "Restrained", "Grabbed"]
NUMBERED_CONDITIONS = ["Clumsy", "Doomed", "Drained", "Enfeebled", "Slowed", "Frightened", "Sickened",
                       "Stunned", "Stupefied", "Quickened"]

ACTIONS = ["Avoid Notice", "Balance", "Burrow", "Cast a Spell", "Climb", "Coerce", "Crawl",
           "Create a Diversion", "Demoralize", "Disable Device", "Disarm", "Earn Income", "Escape", "Feint",
           "Force Open", "Grab an Edge", "Grapple", "High Jump", "Leap", "Liberating Step", "Long Jump",
           "Make an Impression", "Mount", "Perform", "Search", "Seek", "Sense Motive", "Shove", "Sneak",
           "Steal", "Sustain a Spell", "Take Cover", "Track", "Treat Disease", "Treat Poison", "Treat Wounds",
           "Trip", "Tumble Through"]