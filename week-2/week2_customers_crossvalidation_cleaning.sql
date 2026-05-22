-- ANDMETE PUHASTAMINE MEESKOND: OPERATIONS |  NÄDAL: 2



--Loo test koopia 
CREATE TABLE customers_test AS SELECT * FROM customers; 
--koopia loodud


-- customers tabelist ridade arv 
SELECT COUNT(*) AS ridade_arv FROM customers_test;
-- Kirjuta üles: 3150 rida


--Leia duplikaatsed e-mailid
SELECT email, COUNT(*) AS koopiate_arv
FROM customers_test
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC;
--Kirjuta üles: 380 duplikaatset e-maili.

--Leia puuduvad nimed
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR first_name = '') AS null_eesnimi,
    COUNT(*) FILTER (WHERE last_name IS NULL OR last_name = '') AS null_perenimi
FROM customers_test;
Kirjuta üles: 0 NULL eesnime, 0 NULL perenime.

--Kontrollin linnade nimekujusid — kas on ebajärjekindlusi?
SELECT city, COUNT(*) AS arv
FROM customers_test
GROUP BY city
ORDER BY city;
--Kirjutan üles: Haapsalu;haapsalu; HAAPSALU;  erinevat nimekuju samale linnale. 

--Kontrollin kontaktandmeid — puuduvad telefoninumbrid ja e-mailid
SELECT
    COUNT(*) FILTER (WHERE phone IS NULL OR phone = '') AS null_telefon,
    COUNT(*) FILTER (WHERE email IS NULL OR email = '') AS null_email
FROM customers_test;
--Kirjutan üles:0 NULL telefon, 380 NULL email.

-- Asenda NULL nimed
UPDATE customers_test
SET first_name = 'Tundmatu'
WHERE first_name IS NULL OR first_name = '';

-- Ühtlusta linnanimed INITCAP + TRIM abil
UPDATE customers_test
SET city = INITCAP(TRIM(city))
WHERE city != INITCAP(TRIM(city));

-- Standardiseeri e-mailid väiketähtedeks
UPDATE customers_test
SET email = LOWER(TRIM(email))
WHERE email != LOWER(TRIM(email));

-- Kontrolli tulemust
SELECT city, COUNT(*) AS arv
FROM customers_test
GROUP BY city ORDER BY city;

-- Näide: standardiseeri telefoninumbrid
SELECT phone,
    CASE
        WHEN phone LIKE '+372%' THEN phone
        WHEN phone LIKE '372%' THEN '+' || phone
        WHEN LENGTH(phone) = 7 THEN '+372' || phone
        ELSE phone
    END AS standardne_telefon
FROM customers_test
WHERE phone IS NOT NULL
LIMIT 10;


--Ristvalideerimine ja kvaliteedikontroll

-- Orbid müügid — kas on customer_id, mida pole customers tabelis?
SELECT COUNT(*) AS orb_klient
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL AND s.customer_id IS NOT NULL;
--Kirjutan üles: 0 müüki viitab olematule kliendile.

-- Orbid müügid — kas on product_id, mida pole products tabelis?
SELECT COUNT(*) AS orb_toode
FROM sales s
LEFT JOIN products p ON s.product_id = p.product_id
WHERE p.product_id IS NULL AND s.product_id IS NOT NULL;
--Kirjutan üles: 0 müüki viitab olematule tootele.

-- Kontrollin hindade kooskõla — kas müügihind ja tootehind klapivad?
SELECT 
    s.sale_id, 
    s.total_price, 
    p.retail_price AS tootehind, 
    s.quantity,
    s.total_price - (p.retail_price * s.quantity) AS erinevus
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE ABS(s.total_price - (p.retail_price * s.quantity)) > 1
--Kirjutan üles: 20 müüki ei klapi hind tootehinnaga

-- Kontrollin, kas on kliente, kes pole kunagi ostnud
SELECT COUNT(*) AS vaimkliendid
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL;
--Kirjutan üles: 592 klienti pole kunagi ostnud.

--Kontrolli, kas on tooteid, mida pole kunagi müüdud
SELECT COUNT(*) AS vaimtooted
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.product_id IS NULL;
--Kirjutan üles: 12 toodet pole kunagi müüdud.

-- Millistel toodetel on suurimad hinnaerinevused?
SELECT 
    p.product_name, 
    p.category, 
    p.retail_price AS list_hind,
    AVG(s.total_price / NULLIF(s.quantity, 0)) AS kesk_muugihind,
    p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0)) AS erinevus
FROM products p
JOIN sales s 
    ON p.product_id = s.product_id
GROUP BY 
    p.product_id, 
    p.product_name, 
    p.category, 
    p.retail_price
HAVING ABS(p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0))) > 5
ORDER BY ABS(p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0))) DESC
LIMIT 10;
--Suurimad hinnaerinevused on: Praktiline viskoosne jakk, Vintage nahkne tossud, Minimalistlik kašmiir bleiser, Klassikaline puust nahkvöö