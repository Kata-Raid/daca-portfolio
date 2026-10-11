--Samm 1. Loo test koopia
CREATE TABLE sales_test as
SELECT*FROM sales;
-- Taga unikaalne rea-tunnus dedup'i jaoks (lisab `id` AINULT siis, kui see puudub).
-- NB: `CREATE TABLE ... AS SELECT` ei pärandata alati `id`-d — see rida teeb Sammu 3 töökindlaks.
ALTER TABLE sales_test ADD COLUMN IF NOT EXISTS id SERIAL;
-- Kontrolli ridade arvu
SELECT COUNT(*) AS ridade_arv FROM sales_test;
--10118 rida
--Samm 2. Leia duplikaadid
SELECT invoice_id, COUNT(*) AS koopiate_arv
FROM sales_test
GROUP BY invoice_id
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC;
--Samm 3. Loe kokku duplikaatsete ridade arv:
SELECT COUNT(*) AS duplikaat_read
FROM sales_test
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sales_test
    GROUP BY invoice_id
);
--null
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
    COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price
FROM sales_test;
--null_customer_id 988, sale_date 0_total_price 0
--Samm 5. Kontrolli kuupäevade formaati — kas on tuleviku kuupäevi?
SELECT COUNT(*) AS tuleviku_kuupaevad
FROM sales_test
WHERE sale_date > CURRENT_DATE
   OR sale_date < DATE '2020-01-01';   -- UrbanStyle.ltd asutati 2020
--null
--kokku probleeme 1, customer_id on 988 tehingul puudu
