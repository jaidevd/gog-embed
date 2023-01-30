s/resorces/resources/g
s/USable/usable/g
s/rdb//g
s/belgium/Belgium/g
s/R\&amp/R\&/g
s/r\&\;d/R\&D/g
s/R\&\;D/R\&D/g
s/s\&\;p/S\&P/g
s/imf/IMF/g
s/hiv/HIV/g
s/sweden/Sweden/g
s/Undisbursed//g
s/r\&amp/r\&/g
s/iceland/Iceland/g
s/italy/Italy/g
s/emissisons/emissions/g
s/ireland/Ireland/g
s/uk/UK/g
s/USed/used/g
s/enforece/enforce/g
s/USers/users/g
s/centeral/central/g
s/spain/Spain/g
s/eu/EU/g
s/australia/Australia/g
s/\&amp/\&/g
s/USe/use/g
s/Techinal/Technical/g
s/donars/donors/g
s/subsciptions/subscriptions/g
s/norway/Norway/g
s/conusmption/consumption/g
s/recevied/received/g
s/germany/Germany/g
s/commerical/commercial/g
s/USing/Using/g
s/france/France/g
s/servies/services/g
s/finland/Finland/g
s/Maunufacturing/Manufacturing/g
s/switzerland/Switzerland/g
s/Periodicty/Periodicity/g
s/canada/Canada/g
s/austria/Austria/g
s/onduty/on-duty/g
s/&#39;/\'/g
s/matural/natural/g
s/chiildren/children/g
s/poland/Poland/g
s/hospiatls/hospitals/g
s/luxembourg/Luxembourg/g
s/commercal/commercial/g
s/Mauriti the US/Mauritius/g
s/sanitaion/sanitation/g
s/curriences/currencies/g
s/Inverstment/Investment/g
s/denmark/Denmark/g
s/greece/Greece/g
s/\bPrive\b/Price/g
s/\bari treatment\b/ARI treatment/g
s/\bcpia rating\b/CPIA rating/g
s/\bdalay\b/delay/g
s/\bdac donors\b/DAC donors/g
s/\disimbursed\b/disbursed/g
s/\bmoney investmented/money invested/g
s/\blargent city/largest city/g
s/portugal/Portugal/g
s/\bprive\b/price/g
s/\bunderweighted\b/underweight/g
s/\bdod\b/DoD/g
s/\bgdp\b/GDP/g
s/\bghg\b/GHG/g
s/\bgni\b/GNI/g
s/\bhfc\b/HFC/g
s/\bibrd\b/IBRD/g
s/\bict\b/ICT/g
s/\bida\b/IDA/g
s/\blpi\b/LPI/g
s/\bnonOECD\b/non-OECD/g
s/\bnonconcessional\b/non-concessional/g
s/\boda\b/ODA/g
s/\bpfc\b/PFC/g
s/\bppg\b/PPG/g
s/\bppp\b/PPP/g
s/\bundp\b/UNDP/g
s/\bunhcr\b/UNHCR/g
s/\bunpbf\b/UNPBF/g
s/\bunrwa\b/UNRWA/g
s/\bwfp\b/WFP/g
s/\bunta\b/UNTA/g
s/\blitre\b/liter/g
s/\bunaids\b/UNAIDS/g
# This don't work
s/Cote d\'Ivoire/Côte d\'Ivoire/g 
s/Curacao/Curaçao/g
# THE_SUPERLATIVE
s/\bpoorest\b/the poorest/g
s/\blargest\b/the largest/g
s/\bthe the poorest\b/the poorest/g
s/\bthe the largest\b/the largest/g
# One word
s/\bmoney lenders\b/moneylenders/g
s/\btax payers\b/taxpayers/g
s/\bpeace keepers\b/peacekeepers/g
s/\bwage workers\b/wageworkers/g
# whitespace parenthesis
s/mm )/mm)/g
# repeat words
s/"\bThe the\b/"The/g
s/\btotal total\b/total/g
s/\bthe the\b/the/g
s/\baverage Average\b/average/g
s/\bexpenses Expenses\b/expenses/g
s/\bproduction Production\b/production/g
s/\brate Rate\b/rate/g
s/\bsavings Savings\b/savings/g
s/\bbranche\b/branches/gI
# Hyphenated
s/\bNon renewable\b/Non-renewable/g
s/\bnon concessional\b/non-concessional/g
s/\bnon residents\b/non-residents/g
s/\bself employed\b/self-employed/g
s/\bwell developed\b/well-developed/g
# Apostrophe
s/\bfemales population\b/female population/g
s/\bmales population\b/male population/g
# Determiner
s/\bIn Isle of Man\b/In the Isle of Man/g
s/\bIn Turks and Caicos Islands\b/In the Turks and Caicos Islands/g
s/\bin Isle of Man\b/in the Isle of Man/g
s/\bin Turks and Caicos Islands\b/in the Turks and Caicos Islands/g
s/\bof Isle of Man\b/of the Isle of Man/g
s/\bof Turks and Caicos Islands\b/of the Turks and Caicos Islands/g
# Misc
s/\bus\$/USD/g
s/\bUS\$/USD/g
s/\baverage per year\b/average annual/g
s/\bTwenty-\ foot Equivalent\b/Twenty-foot\ Equivalent/g
s/\bNumber of enrolments of both sexes\b/number of enrolments of both sexes/g
s/\bEgypt, Arab Rep\.\+/Egypt/g
s/\bYemen, Rep\.\+/Yemen/g
s/(\ 0 = weak/(0 = weak/g
# These are the result of bad regexes - still leaving out here for completeness for now:
s/\bfrom\s\+across\b/from across/g
s/\bfrom\s\+and\b/from and/g
s/\bfrom\s\+differ\b/from differ/g
s/\bfrom\s\+does\b/from does/g
s/\bfrom\s\+in\b/from in/g
s/\bfrom\s\+is\b/from is/g
s/\bfrom\s\+per\b/from per/g
s/\bfrom\s\+taken\b/from taken/g
s/\bfrom\s\+was\b/from was/g
# GPES
s/\bMiddle\ East\b/the\ Middle East/g
s/\bBahamas\b/the Bahamas/g
s/\bCayman Islands\b/the Cayman Islands/g
s/\bCentral African Republic\b/the Central African Republic/g
s/\bCongo\b/the Congo/g
s/\bCzech Republic\b/the Czech Republic/g
s/\bDominican Republic\b/the Dominican Republic/g
s/\bGambia\b/the Gambia/g
s/\bNetherlands\b/the Netherlands/g
s/\bPhilippines\b/the Philippines/g
s/\bSlovak Republic\b/the Slovak Republic/g
s/\bSolomon Islands\b/the Solomon Islands/g
s/\bUS\b/the US/g
s/\bUnited Arab Emirates\b/the United Arab Emirates/g
s/\bUnited Kingdom\b/the United Kingdom/g
s/\bUnited States\b/the United States/g
s/\bVirgin Islands\b/the Virgin Islands/g
s/\bWest Bank\b/the West Bank/g
s/\bCaribbean\b/the Caribbean/g
s/\bComoros\b/the Comoros/g
s/\bMaldives\b/the Maldives/g
s/\bMarshall Islands\b/the Marshall Islands/g
s/\bChannel Islands\b/the Channel Islands/g
s/\bthe the\b/the/Ig
