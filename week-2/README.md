# Nädal 2: SQL Cleaning -- Urbanstyle andmete uurimine

## Äriprobleem

Selle nädala fookuses oli UrbanStyle’i andmete puhastamine, kus pidime kõrvaldama kriitilised vead nagu üle 5000 duplikaatse müügirea, puuduvad kliendiandmed (NULL-väärtused) ja ebakorrektsed tuleviku kuupäevad.

## Lähenemine
Minu ülesanne oli toote-ja müügiandmete puhastamine ja ristvalideerimine ROLL B. Kasutasin oma töös GROUP BY + HAVING ja ROW_NUMBER(),IS NULL, COALESCE() ja NULLIF(, CAST, TRIM(), UPPER()/LOWER() ja kuupäevafunktsioon.

## Peamised Leiud

- Kogumüük kõige kõrgem Tallinnas (1 062 52)
- Hõbeda tasemel kliente (560)
- 1024 klienti ei ole üheski lojaalsusprogrammi tasemes
- 2 müügikanalit: online (1 006 747) ja pood (1 902 430)
- Online poe osakaal on suurem kõrgema elanikkonnaga piirkondades 
- Enim müüki toovad sisse füüsilised poed, mis on kõigis linnades peamine müügikanal

## Tehniline Pinurida
SQL

## Ekraanipildid


## Õpitu ja Väljakutsed
Õppisin sellel nädalal andmete puhastamist ja ristvalideerimist. 

## AI kasutamine
AI kasutus tööprotsessis: Kasutasin sel nädalal AI-d (NotebookLM), et kiiresti leida ja mõista spetsiifilisi SQL-i funktsioone. AI aitas mul ka SQL päringuid õigeks muuta ja genereerida kontrollpäringuid, mis tagasid, et muudatused test-tabelites olid korrektsed.

## Meeskonna töö
https://docs.google.com/presentation/d/1aXbHz_prwYMUp1iP37YYKQh6YgeExWUGKPCPc3-hlUU/edit?slide=id.g3e1805e3309_1_0#slide=id.g3e1805e3309_1_0 

## Failid
- week2_customers_crossvalidation_cleaning.sql -- minu SQL päringud
- week2_results_screenshot.png -- tulemuste pilt 
