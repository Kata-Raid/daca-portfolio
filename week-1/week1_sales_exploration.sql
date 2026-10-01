-- Millised kanalid, asukohad ja makseviisid on?
SELECT channel, store_location, payment_method
FROM sales
LIMIT 10;
-- pood, online kanalid, asukohad Tallinn, Tartu ja Pärnu, makseviisid kaart, sularaha, järelmaks
-- Unikaalsed müügikanalid
SELECT DISTINCT channel FROM sales;
-- Online ja pood
-- Unikaalsed kaupluste asukohad
SELECT DISTINCT store_location FROM sales;
--Tallinn, Pärnu ja Tartu
-- Unikaalsed makseviisid
SELECT DISTINCT payment_method FROM sales
--Järelmaks, kaart ja sularaha
--Online müük
SELECT*FROM sales
WHERE channel='online'
ORDER BY total_price desc
LIMIT 15;
--Tehingud ilma kaupluse asukohata
SELECT COUNT(*) AS puuduv_asukoht
FROM sales
WHERE store_location IS NULL;
--5204
--kui suur osa müügist toimub veebis vs poodides?
SELECT COUNT(*) AS puuduv_asukoht
FROM sales
WHERE store_location IN('Tartu', 'Tallinn', 'Pärnu');
--poes toimub kohapeal müüke 10 030, seega üle poolte müükide toimuvad onlineis