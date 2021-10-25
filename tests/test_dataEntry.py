from unittest import TestCase

from pf2e_data import dataEntry


class Test(TestCase):

    def test_condition_sub(self):
        test_condition = r"Blinded"
        test_string = r"something %s stuff" % test_condition.lower()

        result = dataEntry.condition_sub(test_string, test_condition)
        self.assertEquals(r"something @Compendium[pf2e.conditionitems.Blinded]{Blinded} stuff", result)
