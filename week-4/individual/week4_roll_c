Koostan ülevaate kategooriate kaupa
SELECT
  p.category,
  COUNT(DISTINCT p.product_id) AS tooteid,
  ROUND(AVG(p.retail_price), 2) AS keskmine_hind,
  MIN(p.retail_price) AS min_hind,
  MAX(p.retail_price) AS max_hind
FROM products p
GROUP BY p.category
ORDER BY tooteid DESC;

SELECT
    p.category AS kategooria,
    SUM(s.quantity) AS "müüdud tooted",
    ROUND(AVG(s.quantity)) AS "keskmine müüdud kogus"
FROM products AS p
JOIN sales s ON s.product_id = p.product_id
GROUP BY p.category
HAVING SUM(s.quantity) > 50
ORDER BY "müüdud tooted" DESC;

SELECT
    p.category AS kategooria,
    SUM(p.retail_price) AS "kasum",
    ROUND(AVG(s.quantity)) AS "keskmine müüdud kogus"
FROM products AS p
JOIN sales s ON s.product_id = p.product_id
GROUP BY p.category
HAVING SUM(s.quantity) > 50
ORDER BY "kasum" DESC;

SELECT
    p.category AS kategooria,
    SUM(i.quantity_available) AS "saadaval tooted"
FROM inventory AS i
JOIN products AS p ON p.product_id = i.product_id
GROUP BY p.category
HAVING SUM(i.quantity_available) > 1
ORDER BY "saadaval tooted" DESC;

SELECT
  p.product_name,
  p.category,
  p.retail_price,
  ROW_NUMBER() OVER (
    PARTITION BY p.category
    ORDER BY p.retail_price DESC
  ) AS koht_kategoorias
FROM products p;


