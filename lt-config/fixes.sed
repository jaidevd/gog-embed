# SPACE_BEFORE_PARENTHESIS
s/\([^[:space:]]\)(/\1 (/g
s/\s\+(/ (/g
# SECOND_LARGEST_HYPHEN
s/\bsecond highest\b/second-highest/g
# Un-escape ampersand
s/&amp;/\&/g
# Determiners for proper nouns
s/\bBahamas\b/the Bahamas/g
s/\bCaribbean\b/the Caribbean/g
s/\bCayman Islands\b/the Cayman Islands/g
s/\bCentral African Republic\b/the Central African Republic/g
s/\bChannel Islands\b/the Channel Islands/g
s/\bComoros\b/the Comoros/g
s/\bCzech Republic\b/the Czech Republic/g
s/\bDominican Republic\b/the Dominican Republic/g
s/\bGambia\b/the Gambia/g
s/\bIsle of Man\b/the Isle of Man/g
s/\bMaldives\b/the Maldives/g
s/\bMarshall Islands\b/the Marshall Islands/g
s/\bMiddle East\b/the Middle East/g
s/\bNetherlands\b/the Netherlands/g
s/\bPhilippines\b/the Philippines/g
s/\bSolomon Islands\b/the Solomon Islands/g
s/\bTurks and Caicos Islands\b/the Turks and Caicos Islands/g
s/\bUnited Arab Emirates\b/the United Arab Emirates/g
s/\bUnited Kingdom\b/the United Kingdom/g
s/\bUnited States\b/the United States/g
s/\bVirgin Islands\b/the Virgin Islands/g
s/\bthe the\b/the/g
# Other, better ways of writing names of countries
s/\bYemen, Rep\./Yemen/g
s/\bEgypt, Arab Rep\./Egypt/g
# Repeated whitespace
s/\s\+/ /g
# Diacritics
s/Sao Tome and Principe/São Tomé and Príncipe/g
# Repeating words
s/\btotal Total\b/total/g
s/\bTotal total\b/Total/g
s/\btotal total\b/total/g
s/\bTotal Total\b/Total/g
s/\bin in\b/in/g
# Other missing determiners
s/\b\(in|of\) Least developed\b/\1 the least developed/g
s/\bin largest city\b/in the largest city/g
s/\b\(in|of\) Labor Market\b/\1 the labor market/g
s/\bin poorest qunitile\b/in the poorest qunitile/g
# Words spelt with hyphens
s/\bself employed\b/self-employed/g
s/\bwell developed\b/well-developed/g
# Words spelt as one
s/\bmoney lenders\b/moneylenders/g
s/\btax payers\b/taxpayers/g
# Incorrect formatting
s/\bTwenty-\s\+foot Equivalent\b/Twenty-foot Equivalent/g
