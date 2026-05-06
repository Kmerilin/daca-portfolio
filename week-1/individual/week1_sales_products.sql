-- ALAÜLESANDE KAART A: Müügiandmed
-- Nädal: 1          Meeskond: Operatsions         Roll: A


-- Kontrollin kui palju müügitehinguid tabelis on 
SELECT COUNT(*) AS ridade_arv
FROM sales;
-- Sales tabelis on 15234 müügitehingut

-- Millised veerud tabelis on?
SELECT * 
FROM sales
LIMIT 10;
-- Tabelis on veerud nagu id, sale_id, invoice_id, sale_date, customer_id, product_id, quantity, unit_price, total_price, channel, store_location ja payment_method.

-- vaatan tallinna kaupluse tehinguid, ostu tehingu lähima kuupäeva järgi, näita ainult 15tk
SELECT *
FROM sales
WHERE store_location = 'Tallinn'
ORDER BY sale_date DESC
LIMIT 15;
-- Kuvati ainult Tallinna müügid. Andmed olid sorteeritud kuupäeva järgi. Andmetes esines erinevaid makseviise, nagu kaart, sularaha ja järelmaks. Mõnel real puudus customer_id väärtus (NULL)

-- 10 suurimat tehingut kahanevas järjekorras 
SELECT *
FROM sales
ORDER BY total_price DESC
LIMIT 10;
-- Päring näitas 10 suurimat müügitehingut, mis olid sorteeritud total_price järgi kahanevalt.
Suurim tehing oli 2170.40€. Enamik suurtest tehingutest sisaldas 5 ühikut toodet. Müügid toimusid nii poes kui ka veebis ning makseviisideks olid kaart ja järelmaks. Invoive_id sisaldab dduplikaate, customer_id NULL ja ka store_location.

-- Päring näitab 10 väikseimat tehingut, kasvavas järjestikus
SELECT *
FROM sales
ORDER BY total_price ASC
LIMIT 10;
-- Kuvati 10 väikseimat tehingut, mis olid järjestatud total_price järgi kasvavalt. Kõik väikseimad väärtused olid negatiivsed, mis viitab võimalikele tagastustele või parandustele. Mõned tehingud toimusid veebis ja mõned poes. Esines ka null väärtusega store_location (online tehingutel).

-- Mitu rida, kus kliendi info on puudu?
SELECT COUNT(*) - COUNT(customer_id) AS puuduv_klient
FROM sales;
--Tulemuseks selgus, et 1487 rida ei sisalda kliendi ID-d. See viitab sellele, et osad müügitehingud ei ole seotud konkreetse kliendiga või kliendi info puudub andmestikus.

-- Kokkuvõte
-- Sales tabelis on kokku 15 234 müügitehingut. Tabelis on veerud nagu id, sale_id, invoice_id, sale_date, customer_id, product_id, quantity, unit_price, total_price, channel, store_location ja payment_method. Üllatav oli see, et osad tehingud olid negatiivse summaga, mis viitab tõenäoliselt tagastustele või korrigeeritud müükidele. Samuti esines puuduvaid andmeid customer_id veerus, kus 1487 rida ei sisaldanud kliendi infot. Andmestikus oli ka mõningaid nullväärtusi store_location veerus (nt online tehingute puhul).


-- Mitu toodet on kokku?
SELECT COUNT(*) AS toodete_arv
FROM products; 
-- Tooteid on kokku 362

-- Vaata toodete tabeli esimesi ridu
SELECT *
FROM products
LIMIT 10;
--Tabelis on info toodete nime, kategooria, hinna ja tootja kohta, eco sertifikaadi ja retail hinna kohta.

-- Kõik unikaalsed tootekategooriad
SELECT DISTINCT category
FROM products;
--Tootekategooriaid on viis: jalanõud, meeste_riided, naiste_riided, laste_riided ja aksessuaarid. See näitab, et UrbanStyle müüb nii rõivaid kui ka jalanõusid ja aksessuaare. Toodete valik on jaotatud erinevate sihtrühmade vahel (mehed, naised ja lapsed).

-- 10 kalleimat toodet
SELECT product_name, category, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 10;
--Kuvati 10 kalleimat toodet sorteerituna retail_price järgi. Kalleimad tooted olid üle 300€.Enamik kalleid tooteid kuulus meeste_riided ja naiste_riided kategooriasse.

-- 10 odavaimat toodet
SELECT product_name, category, retail_price
FROM products
ORDER BY retail_price ASC
LIMIT 10;

--Kuvati 10 odavaimat toodet sorteerituna retail_price järgi kasvavalt. Odavaim toode maksis 13.53€ ja kalleim sellest valikust 24.54€. Enamik odavamaid tooteid kuulus aksessuaaride kategooriasse. Samuti esines laste_riided kategooria madalama hinnaga toodete seas.

-- Kõik naiste riided
SELECT *
FROM products
WHERE category = 'naiste_riided'
ORDER BY retail_price DESC;
--Valiti kategooria naiste_riided ja kuvati kõik selle kategooria tooted. Tooted olid sorteeritud retail_price järgi kahanevalt, seega kõige kallimad tooted olid nimekirja alguses. Naiste_riiete kategoorias oli väga lai hinnavahemik – ligikaudu 30€ kuni üle 350€.Selles kategoorias esines erinevaid tooteid, näiteks jakid, kleidid, püksid ja pluusid. Enamik tooteid oli keskmise kuni kõrgema hinnatasemega, mis viitab rõivakategooria suuremale väärtusele.

-- Puuduvad hinnad
SELECT COUNT(*) - COUNT(retail_price) AS puuduvad_hinnad
FROM products;
-- Tulemus näitas, et puuduvaid hindu ei esine (0 rida). See tähendab, et kõikidel toodetel on müügihind olemas ning andmed on selles osas täielikud.

-- Puuduvad kategooriad
SELECT COUNT(*) - COUNT(category) AS puuduvad_kategooriad
FROM products;
--Kontrolliti puuduvaid väärtusi category veerus. Tulemus näitas, et puuduvaid kategooriaid ei esine (0 rida). See tähendab, et kõikidel toodetel on kategooria määratud ning andmestik on selles osas täielik.

--Kokkuvõte Products tabelis on kokku 50 toodet (valimi põhjal). Tooted jagunevad viide kategooriasse: jalanõusid, meeste_riided, naiste_riided, laste_riided ja aksessuaarid.Toodete hinnad varieeruvad ligikaudu 13.53€ kuni üle 350€, kus odavaimad tooted on peamiselt aksessuaarid ning kallimad pigem naiste- ja meeste rõivad (nt jakid ja ülerõivad).Puuduvaid andmeid ei esinenud ei hindade (retail_price) ega kategooriate (category) veerus (mõlemal juhul tulemus 0). See näitab, et andmestik on täielik ja sobib hästi analüüsimiseks.

