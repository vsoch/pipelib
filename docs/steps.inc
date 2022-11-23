========= ========================= ========================= ===========================================================================
type      name                      module                    description
========= ========================= ========================= ===========================================================================
filter    HasMaxLength              HasMaxLength              Keep items (return true) given a maximum length
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
filter    HasMinLength              HasMinLength              Keep items (return true) given a minimum length
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
filter    HasAllLetters             HasAllLetters             Keep items with all letters (no numbers or special characters)
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
filter    HasAllLowerLettersNumbers HasAllLowerLettersNumbers Keep the string if it's the string is only lowercase letters and numbers.
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
filter    HasPatterns               HasPatterns               Determine if items match a pattern of interest.
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
filter    CleanCommit               CleanCommit               Given a container tag that has -- and _ separating some commit and version,
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
transform SplitAndJoinN             SplitAndJoinN             Split a string by one delimiter, join by another.
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
transform ToLowercase               ToLowercase               Convert the item to all lowercase.
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
transform ToString                  ToString                  Convert the item to a string (typically from a wrapper)
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
container ContainerTagSort          ContainerTagSort          Parse container tag versions and return a filtered and sorted set.
--------- ------------------------- ------------------------- ---------------------------------------------------------------------------
sort      BasicSort                 BasicSort                 Sort the list of items
========= ========================= ========================= ===========================================================================
