FIRST = r"1"
string = re.sub(r"clumsy %s" % FIRST, r"@Compendium[pf2e.conditionitems.Clumsy]{Clumsy %s}" % FIRST, string, count=1)
    string = re.sub(r"doomed %s" % FIRST, r"@Compendium[pf2e.conditionitems.Doomed]{Doomed %s}" % FIRST, string, count=1)
    string = re.sub(r"drained %s" % FIRST, r"@Compendium[pf2e.conditionitems.Drained]{Drained %s}" % FIRST, string, count=1)
    string = re.sub(r"enfeebled %s" % FIRST, r"@Compendium[pf2e.conditionitems.Enfeebled]{Enfeebled %s}" % FIRST, string, count=1)
    string = re.sub(r"slowed %s" % FIRST, r"@Compendium[pf2e.conditionitems.Slowed]{Slowed %s}" % FIRST, string, count=1)
    string = re.sub(r"frightened %s" % FIRST, r"@Compendium[pf2e.conditionitems.Frightened]{Frightened %s}" % FIRST, string, count=1)
    string = re.sub(r"sickened %s" % FIRST, r"@Compendium[pf2e.conditionitems.Sickened]{Sickened %s}" % FIRST, string, count=1)
    string = re.sub(r"stunned %s" % FIRST, r"@Compendium[pf2e.conditionitems.Stunned]{Stunned %s}" % FIRST, string, count=1)
    string = re.sub(r"stupefied %s" % FIRST, r"@Compendium[pf2e.conditionitems.Stupefied]{Stupefied %s}" % FIRST, string, count=1)
    string = re.sub(r"quickened %s" % FIRST, r"@Compendium[pf2e.conditionitems.Quickened]{Quickened %s}" % FIRST, string, count=1)