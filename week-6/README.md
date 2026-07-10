# Nädal 6: Andmelugu — Tartu kaupluse langustrend

## 👤 Minu roll
Roll B, Track B — andmelugu (data storytelling)

## 🎯 Äriprobleem
Tartu on UrbanStyle'i teine kauplus käibe poolest, kuid andmed näitasid langustrendi. Investor vajas vastust: kas Tartu on probleem või võimalus, ja mida konkreetselt ette võtta.

## ⚙️ Lähenemine
Ehitasin Streamlit dashboard'i, mis filtreerib andmed ainult Tartu kaupluse kohta ja võrdleb neid Tallinna kuukeskmisega (benchmark). Struktureerisin loo Knaflic'i "Storytelling with Data" põhimõtte järgi: Ülesseade → Konflikt → Soovitus. Taaskasutasin Nädal 5 andmekihti (`data_loader.py`), et vältida topelttööd.

## 🔍 Peamised Leiud
- Tartu kuukeskmine käive jääb selgelt Tallinna omale alla — dashboard arvutab reaalajas täpse protsentuaalse vahe
- Käive langes järsult pärast tippkuud, mitte hooajaliselt kõikudes — see viitab struktuursele, mitte ajutisele probleemile
- Koodis on välja toodud kaks võimalikku põhjust: uue konkurendi avanemine Tartu kesklinnas ja online-kanali eelistus (online-müük ei kajastu poe käibes)
- Analüüsist eemaldati kuud, kus käive jäi alla 5000€ — vältimaks moonutust andmestiku hõredast sabast

## 💼 Äriline soovitus
Koodis endas juba sõnastatud: Tartu kaupluse audit (asukoht, teenindus, laoseis), tootevaliku kohandamine kohalikule nõudlusele, ja kohaliku turunduskampaania käivitamine. Kuna langus on kiire ja püsiv, mitte hooajaline, vajab see kohest tegutsemist, mitte jälgimist järgmise kvartalini.

## 🛠️ Tehniline Pinurida
Python, Streamlit, Plotly, pandas, Supabase (taaskasutatud Nädal 5 andmekiht)


## ▶️ Kuidas Käivitada

```bash
cd week-6
pip install streamlit pandas plotly supabase python-dotenv
streamlit run tartu_dashboard.py
```
Avaneb aadressil http://localhost:8501

## 💡 Õpitu ja Väljakutsed
Lõin Tartu kaupluse Streamlit dashboard'i ja andmeloo. Kujundasin KPI-kaardid ja visualiseeringud, arvutasin võrdlusmõõdikuid. Analüüsisin müügi-, toote- ja kliendiandmeid ning koostasin juhtkonnale peamised ärilised järeldused ja soovitused.

## 🤖 AI kasutamine
Kasutasin ChatGPT-d, et aidata kujundada dashboard'i ülesehitust, kirjutada Python/Streamlit koodi ning sõnastada ärilisi järeldusi ja juhtkonnale mõeldud soovitusi.

## 👥 Meeskonna töö
https://docs.google.com/presentation/d/1z4LPNL1jmZUq7Cw4m29Y-bjUWCAC24PDErt_MBjGw-E/edit

## 📁 Failid
- `tartu_dashboard.py` — Tartu dashboard ja andmelugu
- `charts_tartu.py` — graafikute abifunktsioonid





