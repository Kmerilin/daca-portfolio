-- WEEK3 

--ROLL: A Müügi ja klientide ühendamine- INNER JOIN abil


--Millised kliendid on ostnud ning kui palju?

SELECT
c.first_name,       
c.last_name,        
c.email,        
c.city,        
s.sale_id,        
s.sale_date,        
s.total_price    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
LIMIT 20; 


-- Leian 10 TOP klienti kogumüügi järgi 
SELECT 
    c.first_name || ' ' || c.last_name AS klient, 
    c.city, 
    COUNT(DISTINCT s.invoice_id) AS ostude_arv, 
    SUM(s.total_price) AS kogumüük
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY kogumüük DESC
LIMIT 10; 

-- Analüüsin müüki linnade kaupa

SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    SUM(s.total_price) AS kogumüük
FROM sales s
INNER JOIN customers c 
    ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY kogumüük DESC;

 -- Müük lojaalsustasemete kaupa    
 SELECT        c.loyalty_tier,        
 COUNT(DISTINCT c.customer_id) AS kliente,        SUM(s.total_price) AS kogumüük    
 FROM sales s    
 INNER JOIN customers c ON s.customer_id = c.customer_id    
 GROUP BY c.loyalty_tier    
 ORDER BY kogumüük DESC;   


--Leian kliendid, kelle kogumüük on üle keskmise

SELECT       
c.first_name || ' ' || 
c.last_name AS klient,       
SUM(s.total_price) AS kogumüük   
FROM sales s   
INNER JOIN customers c ON s.customer_id = c.customer_id   
GROUP BY c.customer_id, c.first_name, c.last_name HAVING SUM(s.total_price) > (       
    SELECT AVG(kliendi_müük)       
    FROM (           
        SELECT SUM(total_price) AS kliendi_müük           
        FROM sales           
        GROUP BY customer_id       ) AS keskmised   )   
        ORDER BY kogumüük DESC;   


--ROLL D: Müügikanalid + kliendid


-- Vaata, millised müügikanalid on olemas    

SELECT DISTINCT channel 
FROM sales 
ORDER BY channel;

-- Olemas on 2 müügikanalit: online ja pood


-- Milline kanal toob enim müüke? 

   SELECT  s.channel AS müügikanal, 
   COUNT(DISTINCT s.customer_id) AS kliente,        
   COUNT(s.sale_id) AS oste,        
   SUM(s.total_price) AS kogumüük    
   FROM sales s    
   GROUP BY s.channel    
   ORDER BY kogumüük DESC; 

 --Enim toob müüke füüsiline pood (1 902 430.30)


-- Millistest linnadest kliendid milliseid kanaleid kasutavad?   

SELECT s.channel AS müügikanal,        
c.city AS linn,        
COUNT(DISTINCT c.customer_id) AS kliente,        
SUM(s.total_price) AS kogumüük    
FROM sales s    INNER JOIN customers c ON s.customer_id = c.customer_id    
GROUP BY s.channel, c.city    
ORDER BY müügikanal, kogumüük DESC;

-- füüsilised poed on peamine müügikanal kõikides linnades
--suuremates linnades on aktiivne nii füüsilises poes kui ka online ostlemine
--online poe osakaal on suurem kõrgema elanikkonnaga piirkondades
--väiksemates linnades eelistavad kliendid rohkem traditsioonilist poes ostmist


--Millised tooted müüvad millises kanalis?    
SELECT s.channel AS müügikanal, 
p.category AS tootekategooria, 
COUNT(DISTINCT c.customer_id) AS kliente, 
COUNT(s.sale_id) AS oste, SUM(s.total_price) AS kogumüük, 
ROUND(AVG(s.total_price), 2) AS keskmine_ost    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
INNER JOIN products p ON s.product_id = p.product_id    
GROUP BY s.channel, p.category    
ORDER BY müügikanal, kogumüük DESC;  

--kõike populaarsemad kategooriad on meeste-ja naisteriided ning jalanõud, mille kogumüük ning keskmine ostu summa on kõige kõrgemad just füüsilises poes
--lasteriiete puhul on keskmine ostu summa väiksem ning eelistatakse ostlemiseks poodi
--aksessuaare ostetakse poole rohkem samuti füüsilisest poest
--kuigi jalanõusidd ostetakse pigem füüsilisest poest, siis kõige kõrgem keskmine ost on just online poes jalanõude kategoorias
--kokkuvõtlikult tehakse online poes üldiselt kokku vähem oste kui füüsilistes poodides 


-- Leian kõige efektiivsema müügikanali müük per klient läbi 
 SELECT        
 s.channel AS müügikanal, 
 COUNT(DISTINCT s.customer_id) AS kliente,        
 SUM(s.total_price) AS kogumüük,        
 ROUND(SUM(s.total_price) / COUNT(DISTINCT s.customer_id), 2) AS müük_per_klient    
 FROM sales s    
 GROUP BY s.channel    
 ORDER BY müük_per_klient DESC; 

 --Kõige efektiivsem on füüsiline pood
 
