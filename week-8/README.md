# Nädal 8: Python API — automatiseeritud ETL pipeline

## 👤 Minu roll
Roll C (visualiseerimine ja salvestamine) + Roll D (automatiseerimisskript / pipeline)

## 🎯 Äriprobleem
Käsitsi analüüs iga nädal on aeganõudev ja veaohtlik. Vaja oli automatiseeritud pipeline'i, mis tõmbab, puhastab, visualiseerib ja ekspordib müügiandmed ühe käsuga.

## ⚙️ Lähenemine
Ehitasin `visualize_export.py` (Roll C), mis loob Plotly joondiagrammi nädalasest tulust ja KPI-indicator kaardid (kogukäive, unikaalsed kliendid, keskmine tellimus) ning ekspordib need CSV+HTML failidena ajatempliga. Ehitasin `pipeline.py` (Roll D), mis ühendab kõik neli rolli (extract → transform → visualize → export) üheks skriptiks koos logimise ja selge veakäsitlusega.

## 🔍 Peamised Leiud
- Pipeline logib iga sammu (INFO tase, ajatempliga), mis lihtsustab tootmises silumist
- Väljundfailid saavad ajatempliga nime (`results_YYYYMMDD.csv`), et vältida ülekirjutamist
- Kui extract-samm ei tagasta andmeid, viskab pipeline selge `ValueError`-i koos juhisega ("kontrolli .env ühendust ja kuupäevi") — parem kui hiljem segane crash
- Diagrammifunktsioonid on try/except'is ja tagastavad tühja `Figure`-i vea korral, mitte ei lase kogu pipeline'il katki minna

## 💼 Äriline soovitus
Pipeline logib ja käitleb vigu juba korralikult — loomulik järgmine samm on see ajastada (nt cron või Airflow) ja lisada teavitus (Slack/e-mail) ebaõnnestumise korral. Praegu nõuab see ikka käsitsi käivitamist ja logide jälgimist, mis kaotab osa automatiseerimise kasust.

## 🛠️ Tehniline Pinurida
Python, pandas, Plotly (express, graph_objects), logging

## 📸 Ekraanipildid
- [`weekly_revenue.html`](./weekly_revenue.html) — nädalase tulu joondiagramm
- [`kpi_summary.html`](./kpi_summary.html) — KPI-kaardid

## ▶️ Kuidas Käivitada

```bash
pip install pandas plotly
python pipeline.py
```
Tulemused salvestuvad `output/` kausta.

## 💡 Õpitu ja Väljakutsed
Õppisin, kuidas ehitada mitmeastmelist ETL pipeline'i (extract → transform → visualize → export) ja panna erinevad moodulid omavahel korrektselt suhtlema. Väljakutseks oli veakäsitluse ja logimise korralik ülesehitamine, et pipeline annaks selge veateate, mitte segase crashi, kui mõni samm ebaõnnestub.

## 🤖 AI kasutamine
Kasutasin ChatGPT-d, et aidata struktureerida pipeline'i loogikat (try/except veakäsitlus, logimise formaat), lahendada Plotly indicator-kaartide paigutuse (domain row/column) vigu, ning kontrollida koodi üldist loogikat.

## 👥 Meeskonna töö
https://docs.google.com/presentation/d/1kJtM9jM5cdKQg91xikcIb1fakwzNAihSeg23QVzBWsg/edit

## 📁 Failid
- `pipeline.py` — minu Roll D, terve pipeline
- `visualize_export.py` — minu Roll C, graafikud ja eksport
- `kpi_summary.html` — eksporditud KPI diagramm
- `weekly_revenue.html` — eksporditud nädalatulu diagramm
