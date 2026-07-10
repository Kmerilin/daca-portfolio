# Nädal 1: SQL Basics — UrbanStyle'i andmete uurimine

## 👤 Minu roll
Andmete esmane uurimine (sales ja products tabelid)

## 🎯 Äriprobleem
UrbanStyle vajas ülevaadet oma müügi- ja tooteandmetest enne sügavamat analüüsi — kas andmed on usaldusväärsed ja milliseid auke/anomaaliaid need sisaldavad.

## ⚙️ Lähenemine
Uurisin sales ja products tabeleid SQL päringutega: COUNT, ORDER BY, DISTINCT, LIMIT ja NULL-kontroll (COUNT(*) - COUNT(veerg)).

## 🔍 Peamised Leiud
- Sales tabelis 15 234 tehingut, 1 487 real (~9.8%) puudub customer_id
- Suurim üksiktehing 2170.40€; väikseimad tehingud negatiivsed (viitab tagastustele/korrigeerimistele)
- Products tabelis 362 toodet, 5 kategoorias (jalanõud, meeste/naiste/laste riided, aksessuaarid)
- Tootehinnad 13.53€–350€+ vahemikus, hindades ja kategooriates puuduvaid väärtusi ei esinenud
- store_location sisaldas NULL väärtusi mõne online-tehingu puhul

## 💼 Äriline soovitus
Enne edasist analüüsi tuleb puuduvad customer_id väärtused (9.8% ridadest) juurutada — kliendisidumata müüki ei saa segmenteerida ega lojaalsusprogrammi arvestada. Samuti tuleb kindlaks teha, kas negatiivsed total_price väärtused on tagastused või andmevead — see mõjutab otseselt käibenumbrite täpsust.

## 🛠️ Tehniline Pinurida
SQL (PostgreSQL/Supabase)

## 📸 Ekraanipildid


## ▶️ Kuidas Käivitada
SQL päringud käivitatavad otse andmebaasi konsoolis (fail: `week1_sales_products_exploration.sql`)


## 👥 Meeskonna töö
https://docs.google.com/document/d/1iUIhHFb633tp-EM_9FFwXHfRahRdlWpFiM4qXpgY6Do/edit?tab=t.0

## 📁 Failid
- `week1_sales_products_exploration.sql` — minu SQL päringud
