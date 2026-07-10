# Nädal 7: Python Pandas — andmete laadimine ja puhastamine

## 👤 Minu roll
Roll A (andmete laadimine ja liitmine) + Roll B (andmete puhastamine)

## 🎯 Äriprobleem
Vaja oli minna üle CSV-põhisele andmetöötlusele pandas'e abil (mitte otse SQL/Supabase), et andmed jõuaksid tootmiskõlblikul kujul edasisse analüüsi.

## ⚙️ Lähenemine
Lugesin `sales.csv` ja `customers.csv` failid pandas'esse (`encoding="utf-8-sig"` BOM-i eemaldamiseks), liitsin need left joiniga `customer_id` põhjal, eemaldasin duplikaadid `sale_id` primaarvõtme järgi, parsisin kuupäevad (mixed formaat, dayfirst), ning tuvastasin NULL väärtused ja negatiivsed `total_price` väärtused — need raporteerisin, aga ei eemaldanud, et tulemus jääks kooskõlla Supabase allikaga.

## 🔍 Peamised Leiud
- Sales: 15 234 rida, Customers: 3 150 rida; left join säilitas kõik 15 234 müügirida
- Täisrea duplikaate 4 086, korduvaid `sale_id` väärtusi 5 116 — pärast puhastust jäi alles 10 118 unikaalset müügitehingut
- 988 real puudus `customer_id` (külalisostud), 3 462 real puudus `store_location` (online tehingud), 195 negatiivset `total_price` (tagastused)
- Kuupäevavahemik 2023-01-01 kuni 2026-12-03 — viimane kuupäev on tuleviku-kuupäev, mis kinnitab week-1 ja week-5 leidu vigastest tulevikukuupäevadest andmestikus

## 💼 Äriline soovitus
Kuna duplikaate oli üle 5000 (~1/3 algandmetest), tasub uurida ETL/ekspordi protsessi allikasüsteemis. Sama vigaste tulevikukuupäevade probleem kordub juba kolmandat nädalat (week-1, week-5, nüüd week-7) — tasuks lahendada andmeallikas üks kord, mitte parandada iga nädal uuesti igas analüüsis.

## 🛠️ Tehniline Pinurida
Python, pandas, Jupyter Notebook

## ▶️ Kuidas Käivitada

```bash
pip install pandas jupyter
jupyter notebook week7_roll_ab.ipynb
```

## 💡 Õpitu ja Väljakutsed
Õppisin kuidas laadida alla CSV faile, liita need ning teostada andmete puhastamise.

## 🤖 AI kasutamine
Kasutasin AI-d nagu eelmistel nädalatel — koodi küsimiseks ja äriliste tõlgenduste loomiseks.

## 👥 Meeskonna töö
https://docs.google.com/presentation/d/14yUo9fP38sgrFW8HtT6MgmD8u_6QZwbUqgs9Tzrsc7s/edit?slide=id.g3ede0e925b1_0_279#slide=id.g3ede0e925b1_0_279

## 📁 Failid
- `week7_roll_ab.ipynb` — minu Roll A+B (laadimine, liitmine, puhastamine)
- `week7_roll_abcd.ipynb` — tiimi ühine fail, sisaldab lisaks tiimikaaslaste RFM-analüüsi (Roll C/D)
