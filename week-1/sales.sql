SELECT COUNT(*) AS ridade_arv FROM sales; -- tahan teada kui mitu rida on sales tabelis

SELECT total_price FROM sales ORDER BY total_price DESC LIMIT 10 -- tahan teada saada mis on 10 kõige suuremat tehingut

SELECT total_price FROM sales ORDER BY total_price ASC LIMIT 10; -- tahan teada saada mis on 10 kõige väiksemat tehingut

SELECT AVG(total_price) AS avg_order_value
FROM sales; -- keskmine tellimuse summa