import pyperclip as cl
from unittest import TestCase

from pf2e_data import dataEntry


class Test(TestCase):

    def test_action_sub(self):
        test_action = r"Seek"
        test_string = r"you Seek for creatures; and when you Seek for"

        result = dataEntry.action_sub(test_string, test_action)
        self.assertEqual(r"you @Compendium[pf2e.actionspf2e.Seek]{Seek} for creatures; and when you Seek for", result)

    def test_action_full_word_sub(self):
        test_action = r"Steal"
        test_string = r"you Steal things; and when you Steal things you don't use Stealth"

        result = dataEntry.action_sub(test_string, test_action)
        self.assertEqual(r"you @Compendium[pf2e.actionspf2e.Steal]{Steal} things; and when you Steal things you don't use Stealth", result)

    def test_condition_sub(self):
        test_condition = r"Blinded"
        test_string = r"something blinded stuff"

        result = dataEntry.condition_sub(test_string, test_condition)
        self.assertEqual(r"something @Compendium[pf2e.conditionitems.Blinded]{Blinded} stuff", result)

    def test_equipment_sub(self):
        test_condition = r"Handwraps of Mighty Blows"
        test_string = r"the Handwraps of Mighty Blows does stuff and... Handwraps of Mighty Blows"

        result = dataEntry.equipment_sub(test_string, test_condition)
        self.assertEqual(r"the @Compendium[pf2e.equipment-srd.Handwraps of Mighty Blows]{Handwraps of Mighty Blows} " 
                         r"does stuff and... Handwraps of Mighty Blows", result)

    def test_feat_sub(self):
        test_feat = r"Canny Acumen"
        test_string = r"Canny Acumen is cool... and so is Canny Acumen"

        result = dataEntry.feat_sub(test_string, test_feat)
        self.assertEqual(
            r"@Compendium[pf2e.feats-srd.Canny Acumen]{Canny Acumen} is cool... and so is Canny Acumen", result)

    def test_spell_sub(self):
        test_spell = r"Plane Shift"
        test_string = r"Plane Shift is cool... and so is Plane Shift"

        result = dataEntry.spell_sub(test_string, test_spell)
        self.assertEqual(
            r"<em>@Compendium[pf2e.spells-srd.Plane Shift]{Plane Shift}</em> is cool... and so is Plane Shift", result)

    def test_handle_actions(self):
        test_string = r"You observe and assess your surroundings with great speed. " \
                      r"You Recall Knowledge, Seek, or Sense Motive."
        expected = r"You observe and assess your surroundings with great speed. " \
                   r"You Recall Knowledge, @Compendium[pf2e.actionspf2e.Seek]{Seek}, or " \
                   r"@Compendium[pf2e.actionspf2e.Sense Motive]{Sense Motive}."

        result = dataEntry.handle_actions(test_string)
        self.assertEqual(expected, result)

    def test_handle_conditions(self):
        test_string = r"The target is blinded for 1 round and dazzled for 10 minutes. " \
                      r"Its invisibility is negated for 10 minutes."
        expected = r"The target is @Compendium[pf2e.conditionitems.Blinded]{Blinded} for 1 round and " \
                   r"@Compendium[pf2e.conditionitems.Dazzled]{Dazzled} for 10 minutes. " \
                   r"Its invisibility is negated for 10 minutes."

        result = dataEntry.handle_conditions(test_string)
        self.assertEqual(expected, result)

    def test_handle_conditions_flat_footed(self):
        test_string = r"The target takes double damage and is flat footed and immobilized."
        expected = r"The target takes double damage and is @Compendium[pf2e.conditionitems.Flat-Footed]{Flat-Footed} " \
                   r"and @Compendium[pf2e.conditionitems.Immobilized]{Immobilized}."

        result = dataEntry.handle_conditions(test_string)
        self.assertEqual(expected, result)

    def test_handle_conditions_numbered(self):
        test_string = r"Foes within the area are frightened 1. They can't reduce their frightened value below 1 " \
                      r"while they remain in the area."
        # Also testing that only the first "frightened" gets replaced.
        expected = r"Foes within the area are @Compendium[pf2e.conditionitems.Frightened]{Frightened 1}. They " \
                   r"can't reduce their frightened value below 1 while they remain in the area."

        result = dataEntry.handle_conditions(test_string)
        self.assertEqual(expected, result)

    def test_handle_equipment(self):
        test_string = r"the Handwraps of Mighty Blows does stuff and... Handwraps of Mighty Blows"

        result = dataEntry.handle_equipment(test_string)
        self.assertEqual(r"the @Compendium[pf2e.equipment-srd.Handwraps of Mighty Blows]{Handwraps of Mighty Blows} "
                         r"does stuff and... Handwraps of Mighty Blows", result)

    def test_handle_feats(self):
        test_string = r"Canny Acumen is cool... and so is Canny Acumen"

        result = dataEntry.handle_feats(test_string)
        self.assertEqual(
            r"@Compendium[pf2e.feats-srd.Canny Acumen]{Canny Acumen} is cool... and so is Canny Acumen", result)

    def test_handle_spells(self):
        test_string = r"Plane Shift is cool... and so is Plane Shift"

        result = dataEntry.handle_spells(test_string)
        self.assertEqual(
            r"<em>@Compendium[pf2e.spells-srd.Plane Shift]{Plane Shift}</em> is cool... and so is Plane Shift", result)

    def test_handle_activation_actions(self):
        param_list = [("free-action", "F"), ("reaction", "R"),
                      ("one-action", "1"), ("two-actions", "2"), ("three-actions", "3")]
        for p1, p2 in param_list:
            with self.subTest():
                test_string = r"Activate [%s] envision;" % p1

                result = dataEntry.handle_activation_actions(test_string)
                self.assertEqual(r"Activate <span class=\"pf2-icon\">%s</span> envision;" % p2, result)

    def test_reformat_general_feat(self):
        test_string = r"Cost the Price of the chosen item " \
                      r"Requirements You haven't used this ability since the last time you were able to purchase goods. " \
                      r"You regularly create convoluted plans and contingencies, using your resources to enact them. You take 1 minute to " \
                      r"remove your backpack, then "
        expected = r"<p><strong>Cost</strong> the Price of the chosen item " \
                   r"<p><strong>Requirements</strong> You haven't used this ability since the last time you were able to purchase goods. " \
                   r"You regularly create convoluted plans and contingencies, using your resources to enact them. You take 1 minute to " \
                   r"remove your backpack, then...</p>"

        result = dataEntry.reformat(test_string)
        self.assertEqual(expected, result)

    def test_reformat_skill_feat(self):
        test_string = "Frequency once per day;\nAccess You are a member of the\nArclords of Nex.\n" \
                      "You open an incandescent third eye\nupon your forehead. The eye can remain\nopen for 1 minute" \
                      ", and you can close it\nbefore then with a single action with the\nconcentrate trait. It can " \
                      "remain open for\n2 minutes if you’re a master in Arcana,\nor 5 minutes if you’re legendary. " \
                      "While\nthe eye is open, you gain the following\nbenefits: you gain the effects of the\ndetect " \
                      "magic arcane innate spell from\nyour Arcane Sense at the start of each\nof your turns without " \
                      "needing to cast\nthe spell; you gain darkvision; you gain\na +2 status bonus to Perception " \
                      "checks\nto Seek undetected and hidden creatures\nand to your Perception DC against Hide\nand " \
                      "Sneak. After your third eye closes,\nyou are dazzled for an amount of time\nequal to how long " \
                      "you had it open."
        expected = r"<p><strong>Frequency</strong> once per day; " \
                   r"<p><strong>Access</strong> You are a member of the Arclords of Nex. " \
                   r"You open an incandescent third eye upon your forehead. The eye can remain open for 1 minute, " \
                   r"and you can close it before then with a single action with the concentrate trait. It can remain " \
                   r"open for 2 minutes if you're a master in Arcana, or 5 minutes if you're legendary. While the " \
                   r"eye is open, you gain the following benefits: you gain the effects of the detect magic arcane " \
                   r"innate spell from your Arcane Sense at the start of each of your turns without needing to " \
                   r"cast the spell; you gain darkvision; you gain a +2 status bonus to Perception checks to " \
                   r"@Compendium[pf2e.actionspf2e.Seek]{Seek} undetected and @Compendium[pf2e.conditionitems.Hidden]{Hidden} " \
                   r"creatures and to your Perception DC against Hide and @Compendium[pf2e.actionspf2e.Sneak]{Sneak}." \
                   r" After your third eye closes, you are @Compendium[pf2e.conditionitems.Dazzled]{Dazzled} for an " \
                   r"amount of time equal to how long you had it open.</p>"

        result = dataEntry.reformat(test_string)
        self.assertEqual(expected, result)

    def test_reformat_worn_item(self):
        test_string = "Thousands of small, reflective, mirrored glass shards have\nbeen carefully stitched down " \
                      "this long silk duster.\nActivate [one-action] Interact; Requirements The mirror robe was " \
                      "last\nactivated to draw attention toward you, or you haven’t\nused the mirror robe today; " \
                      "Effect The mirror robe Creates\na Diversion for you with a +9 Deception modifier.\n" \
                      "Activate [one-action] Interact (visual); Requirements The mirror robe\nwas last activated to " \
                      "divert attention away from you\nand you are hidden or undetected by at least one foe;\n" \
                      "Effect You draw attention toward yourself. Choose one\nfoe to which you were hidden or " \
                      "undetected. You reveal\nyourself to all, becoming observed. The foe you chose\ndiverts its " \
                      "attention to you, becoming flat-footed to your\nallies until the beginning of your next turn. " \
                      "If you are\ninvisible or otherwise can’t become observed, you can’t\nuse this activation."
        expected = r"<p>Thousands of small, reflective, mirrored glass shards have been carefully stitched down this " \
                   r"long silk duster. Activate <span class=\"pf2-icon\">1</span> Interact; <p>" \
                   r"<strong>Requirements</strong> The mirror robe was last activated to draw attention toward you, " \
                   r"or you haven't used the mirror robe today;</p><p><strong>Effect</strong> The mirror robe " \
                   r"Creates a Diversion for you with a +9 Deception modifier. " \
                   r"Activate <span class=\"pf2-icon\">1</span> Interact (visual); " \
                   r"<p><strong>Requirements</strong> The mirror robe was last activated to divert attention away " \
                   r"from you and you are @Compendium[pf2e.conditionitems.Hidden]{Hidden} or undetected by at least " \
                   r"one foe;</p><p><strong>Effect</strong> You draw attention toward yourself. Choose one foe to " \
                   r"which you were hidden or undetected. You reveal yourself to all, becoming observed. The foe you " \
                   r"chose diverts its attention to you, becoming @Compendium[pf2e.conditionitems.Flat-Footed]{Flat-Footed} " \
                   r"to your allies until the beginning of your next turn. If you are " \
                   r"@Compendium[pf2e.conditionitems.Invisible]{Invisible} or otherwise can't become observed, you " \
                   r"can't use this activation.</p>"

        result = dataEntry.reformat(test_string)
        self.assertEqual(expected, result)

    def test_reformat_spell_gale_blast(self):
        test_string = "Cast [two-actions] somatic, verbal\nSaving Throw Fortitude\nWind flows from your outstretched " \
                      "hands and whirls\naround you in a 5-foot emanation. Each creature in the\narea takes " \
                      "bludgeoning damage equal to your spellcasting\nability modifier, with a Fortitude save.\n" \
                      "Critical Success The creature is unaffected.\nSuccess The creature takes half damage.\n" \
                      "Failure The creature takes full damage and is pushed 5 feet\naway from you.\nCritical Failure " \
                      "The creature takes double damage and is\npushed 10 feet away from you.\nHeightened (+2) The " \
                      "damage increases by 1d6."
        expected = r"<p>Cast <span class=\"pf2-icon\">2</span> somatic, verbal</p><p><strong>Saving Throw</strong> " \
                   r"Fortitude Wind flows from your outstretched hands and whirls around you in a " \
                   r"@Template[type:emanation|distance:5]. Each creature in the area takes bludgeoning damage equal " \
                   r"to your spellcasting ability modifier, with a Fortitude save.</p><hr /><p>" \
                   r"<strong>Critical Success</strong> The creature is unaffected.</p><p><strong>Success</strong> " \
                   r"The creature takes half damage.</p><p><strong>Failure</strong> The creature takes full damage " \
                   r"and is pushed 5 feet away from you.</p><p><strong>Critical Failure</strong> The creature takes " \
                   r"double damage and is pushed 10 feet away from you. </p><hr /><p><strong>Heightened (+2)</strong> " \
                   r"The damage increases by 1d6.</p>"

        result = dataEntry.reformat(test_string)
        self.assertEqual(expected, result)

    def test_reformat_spell_shocking_grasp(self):
        test_string = "Cast [two-actions] somatic, verbal\nRange touch; Targets 1 creature\nYou shroud your hands " \
                      "in a crackling field of lightning. Make\na melee spell attack roll. On a hit, the target " \
                      "takes 2d12\nelectricity damage. If the target is wearing metal armor or\nis made of metal, " \
                      "you gain a +1 circumstance bonus to your\nattack roll with shocking grasp, and the target " \
                      "also takes 1d4\npersistent electricity damage on a hit. On a critical hit, double\nthe " \
                      "initial damage, but not the persistent damage.\nHeightened (+1) The damage increases by 1d12, " \
                      "and the\npersistent electricity damage increases by 1."
        expected = r"<p>Cast <span class=\"pf2-icon\">2</span> somatic, verbal Range touch; Targets 1 creature " \
                   r"You shroud your hands in a crackling field of lightning. Make a melee spell attack roll. On a " \
                   r"hit, the target takes [[/r {2d12}[electricity]]]{2d12 electricity damage}. If the target is " \
                   r"wearing metal armor or is made of metal, you gain a +1 circumstance bonus to your attack roll " \
                   r"with shocking grasp, and the target also takes [[/r {1d4}[persistent,electricity]]]{1d4} " \
                   r"@Compendium[pf2e.conditionitems.Persistent Damage]{Persistent electricity Damage} on a hit. On " \
                   r"a critical hit, double the initial damage, but not the persistent damage. </p><hr />" \
                   r"<p><strong>Heightened (+1)</strong> The damage increases by 1d12, and the persistent " \
                   r"electricity damage increases by 1.</p>"

        result = dataEntry.reformat(test_string)
        self.assertEqual(expected, result)
