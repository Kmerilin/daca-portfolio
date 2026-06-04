-- WEEK 4 GRUPITÖÖ ROLL:B

--Kliendigruppide analüüs

-- Kasutan CTE-d, et arvutada kliendi baasandmed
WITH kliendi_kokkuvote AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS nimi,
        c.city,
        COUNT(o.sale_id) AS tellimuste_arv,
        SUM(o.total_price) AS kogukäive
    FROM customers c
    JOIN sales o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
)
-- Põhipäring, kus toimub segmenteerimine ja järjestamine
SELECT
    nimi,
    city,
    tellimuste_arv,
    kogukäive,
    -- Kasutame CASE WHEN loogikat segmentide määramiseks
    CASE
        WHEN kogukäive > 500 THEN 'VIP'       -- Piiriks 500€ tuginedes püsikliendi väärtusele
        WHEN kogukäive > 100 THEN 'Regular'   -- Piiriks 100€ (u 2-3 keskmist ostu)
        ELSE 'Uus'
    END AS segment,
    -- Aknafunktsioon: järjestab kliendid linna siseselt käibe järgi
    RANK() OVER (
        PARTITION BY city 
        ORDER BY kogukäive DESC
    ) AS koht_linnas
FROM kliendi_kokkuvote
ORDER BY kogukäive DESC;


-- Leian 10 suurima kogukäibega püsiklienti (vähemalt 2 ostu)

SELECT 
    c.first_name || ' ' || c.last_name AS klient,
    SUM(s.total_price) AS kogukäive,
    COUNT(s.sale_id) AS tellimusi
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(s.sale_id) >= 2 
ORDER BY kogukäive DESC
LIMIT 10;

-- Kliendisegmentide koondstatistika

WITH kliendi_clv AS (
    SELECT 
        c.customer_id,
        SUM(s.total_price) AS kogukäive
    FROM customers c
    INNER JOIN sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
),
segmenteeritud_baas AS (
    SELECT 
        customer_id,
        kogukäive,
        CASE 
            WHEN kogukäive > 500 THEN 'VIP'
            WHEN kogukäive > 100 THEN 'Regular'
            ELSE 'Uus'
        END AS segment
    FROM kliendi_clv
)
SELECT 
    segment,
    COUNT(customer_id) AS klientide_arv,
    ROUND(AVG(kogukäive), 2) AS keskmine_segmenti_käive
FROM segmenteeritud_baas
GROUP BY segment
ORDER BY keskmine_segmenti_käive DESC;

--UrbanStyle'i analüüs tuvastas 1722 VIP-klienti, 714 Regular-klienti ning 115 Uut klienti, kusjuures VIP-segment on kõige suurem ja asub peamiselt Tallinnas (678 inimest). Anna peaks Kristile raporteerima, et meie lojaalsusprogramm on erakordselt tugev, kuna suurim osa käibest tuleb pikaajalistelt VIP-klientidelt. Soovitusena tuleks Tallinna VIP-idele suunata eksklusiivne kampaania, samas kui Regular-kliente tuleks kõnetada ''Kuld kliendiks'' pakkumisega. 

--ROLL D: Turunduskampaaniate ROI

--Turunduskanalite koondandmed

SELECT 
    w.source AS turunduskanal, 
    COUNT(DISTINCT c.customer_id) AS kliente, 
    COUNT(DISTINCT o.sale_id) AS tellimusi, 
    SUM(o.total_price) AS kogumüük, 
    ROUND(AVG(o.total_price), 2) AS keskmine_tellimus
FROM sales o 
JOIN customers c ON o.customer_id = c.customer_id 
LEFT JOIN web_logs w ON c.customer_id = w.customer_id 
GROUP BY w.source 
ORDER BY kogumüük DESC;

--Kanali efektiivsus

WITH kanali_myyk AS (
    SELECT w.source, SUM(o.total_price) AS kogukaive, COUNT(o.sale_id) AS tellimuste_arv
    FROM sales o
    JOIN web_logs w ON o.customer_id = w.customer_id
    GROUP BY w.source
),
kanali_kliendid AS (
    SELECT w.source, COUNT(DISTINCT o.customer_id) AS kliendi_arv
    FROM sales o
    JOIN web_logs w ON o.customer_id = w.customer_id
    GROUP BY w.source
)
SELECT 
    km.source AS kanal,
    km.kogukaive,
    kk.kliendi_arv,
    ROUND(km.kogukaive / kk.kliendi_arv, 2) AS myyk_per_klient
FROM kanali_myyk km
JOIN kanali_kliendid kk ON km.source = kk.source
WHERE km.tellimuste_arv > 50 -- Valitud piir: kanalid, kus on vähemalt 50 tellimust
ORDER BY myyk_per_klient DESC;

-- 1. SAMM: Puhastan ja ühtlustan kanalite nimed CTE-s
WITH puhastatud_andmed AS (
    SELECT 
        s.total_price,
        s.customer_id,
        CASE 
            WHEN LOWER(w.source) LIKE '%google%' AND (LOWER(w.source) LIKE '%organic%' OR w.source = 'google') 
                THEN 'Google Organic'
            WHEN LOWER(w.source) = 'google_ads' THEN 'Google Ads'
            
            -- Koondame kõik Facebooki variatsioonid (FB, fb_ads jne)
            WHEN LOWER(w.source) LIKE '%facebook%' OR LOWER(w.source) LIKE 'fb%' 
                THEN 'Facebook Ads'
            
            -- Koondame Instagrami variatsioonid (IG, ig_ads jne)
            WHEN LOWER(w.source) LIKE '%instagram%' OR LOWER(w.source) LIKE 'ig%' 
                THEN 'Instagram Ads'
            
            ELSE INITCAP(TRIM(w.source))
        END AS puhas_kanal
    FROM sales s
    INNER JOIN web_logs w ON s.customer_id = w.customer_id 
) 

SELECT 
    puhas_kanal AS turunduskanal,
    SUM(total_price) AS kogumüük,
    COUNT(DISTINCT customer_id) AS kliente,
    ROUND(SUM(total_price) / COUNT(DISTINCT customer_id), 2) AS myyk_per_klient
FROM puhastatud_andmed 
GROUP BY puhas_kanal
ORDER BY myyk_per_klient DESC;