# Nädal 3: SQL JOINS — kliendid, müügikanalid ja kategooriad

## 👤 Minu roll
Roll A (klientide ja müügi ühendamine INNER JOIN abil) + Roll D (müügikanalid + kliendid)

## 🎯 Äriprobleem
Vaja oli ühendada müügi- ja kliendiandmed, et näha, kes reaalselt ostab, milline müügikanal (pood vs online) on efektiivsem ja kuidas tootekategooriad kanalite lõikes erinevad.

## ⚙️ Lähenemine
Kasutasin INNER JOIN-e sales, customers ja products tabelite vahel, GROUP BY agregatsioone (COUNT, SUM, AVG), ja subquery + HAVING klauslit, et leida keskmisest suurema kogumüügiga kliendid.

## 🔍 Peamised Leiud
- Füüsiline pood on peamine müügikanal kõigis linnades, kogumüük 1 902 430.30€
- Online-kanali osakaal on suurem kõrgema elanikkonnaga linnades; väiksemates linnades eelistatakse poodi
- Meeste/naiste riided ja jalanõud on populaarseimad kategooriad — kõrgeim kogumüük ja keskmine ostusumma just füüsilises poes
- Erandiks on jalanõud: kuigi rohkem oste tehakse poes, on keskmine ostusumma just online-kanalis kõrgeim
- Müük-per-klient mõõdikus on füüsiline pood kõige efektiivsem kanal

## 💼 Äriline soovitus
Kuna jalanõude kategoorias on online-kanali keskmine ostusumma kõrgeim, tasub kõrgema elanikkonnaga linnades suunata online-turundust just jalanõudele — see kasvataks online-kanali keskmist ostukorvi, mitte ainult käivet.

## 🛠️ Tehniline Pinurida
SQL (PostgreSQL/Supabase) — INNER JOIN, GROUP BY, subquery/HAVING

## 📸 Ekraanipildid


## ▶️ Kuidas Käivitada
SQL päringud käivitatavad otse andmebaasi konsoolis (fail: `week3_roll_a_myyk_kliendid_turundus.sql`)

## 💡 Õpitu ja Väljakutsed
Õppisin kuidas kasutada LEFT JOIN-i ja NULL-kontrolli, analüüsisin kliendi geograafilist asukohta ning koostasin raporti.

## 🤖 AI kasutamine
Kasutasin ChatGPT-d, et kontrollida SQL JOIN päringute loogikat, aidata lahendada vigu ning sõnastada ärilised järeldused ja soovitused.

## 👥 Meeskonna töö
https://docs.google.com/presentation/d/1oSZyKl0YB271pfwPAe21IILeEIEnSs-osVSvAM5A2L0/edit?slide=id.g3e1805e3309_1_0#slide=id.g3e1805e3309_1_0

## 📁 Failid
- `week3_roll_a_myyk_kliendid_turundus.sql` — minu SQL päringud
