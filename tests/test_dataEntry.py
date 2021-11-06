from unittest import TestCase

from pf2e_data import dataEntry


class Test(TestCase):

    def test_action_sub(self):
        test_action = r"Seek"
        test_string = r"you Seek for creatures; and when you Seek for"

        result = dataEntry.action_sub(test_string, test_action)
        self.assertEqual(r"you @Compendium[pf2e.actionspf2e.Seek]{Seek} for creatures; and when you Seek for", result)

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

