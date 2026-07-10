# Nädal 4: Agregatsioonid — kliendisegmentatsioon ja turunduskanalite ROI

## 👤 Minu roll
Roll B (kliendigruppide analüüs / segmentatsioon) + Roll D (turunduskampaaniate ROI)

## 🎯 Äriprobleem
UrbanStyle vajas ülevaadet, millised kliendid toovad enim väärtust (segmentatsioon) ja millised turunduskanalid õigustavad oma kulu — ilma selleta kulub turunduseelarve laiali ilma sihita.

## ⚙️ Lähenemine
Kasutasin CTE-sid kliendi kokkuvõtte arvutamiseks, CASE WHEN loogikat segmenteerimiseks (VIP/Regular/Uus), RANK() OVER (PARTITION BY city) aknafunktsiooni linnasisese pingerea jaoks, ning LEFT JOIN web_logs tabeliga turunduskanalite ROI analüüsiks. Kanalinimed (google_ads, fb, ig jne) tuli CASE WHEN + LIKE loogikaga esmalt puhastada ja ühtlustada.

## 🔍 Peamised Leiud
- 1 722 VIP-klienti (kogukäive >500€), 714 Regular-klienti (>100€), 115 Uut klienti
- VIP on suurim segment ja asub valdavalt Tallinnas (678 inimest)
- Turunduskanalite nimed olid ebaühtlased (nt "fb", "facebook", "ig_ads") ja vajasid standardiseerimist enne analüüsi
- Kanali efektiivsuse (müük per klient) analüüsi kaasati ainult kanalid, kus vähemalt 50 tellimust

## 💼 Äriline soovitus
Kuna lojaalsusprogrammi suurim käive tuleb pikaajalistelt VIP-klientidelt, tuleks Tallinna VIP-idele suunata eksklusiivne kampaania, samas Regular-kliente kõnetada "Kuld kliendiks" pakkumisega, et liigutada neid VIP-segmenti.

## 🛠️ Tehniline Pinurida
SQL (PostgreSQL/Supabase) — CTE, window functions (RANK), CASE WHEN, LEFT JOIN

## 📸 Ekraanipildid


## ▶️ Kuidas Käivitada
SQL päringud käivitatavad otse andmebaasi konsoolis (fail: `week-4_roll_b_aggregation.sql`)

## 💡 Õpitu ja Väljakutsed
Kirjutasin SQL päringud müügi- ja kliendiandmete analüüsimiseks. Kasutasin agregatsioonifunktsioone (SUM, COUNT, AVG, GROUP BY), analüüsisin müügitrende kuude lõikes ning koostasin peamised järeldused ja ärilised soovitused.

## 🤖 AI kasutamine
Kasutasin ChatGPT-d, et kontrollida SQL päringute loogikat, aidata leida vigade põhjuseid ning sõnastada ärilised järeldused ja soovitused.

## 👥 Meeskonna töö
https://docs.google.com/presentation/d/1cFoeW5i1hSBeOK26qFkYzEMcqnNt3PfFbszMdjDYEzw/edit

## 📁 Failid
- `week-4_roll_b_aggregation.sql` — minu SQL päringud
