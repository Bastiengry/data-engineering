-- mart_top_stores.sql
SELECT 
    store, 
    SUM(total_revenue) AS grand_total
FROM {{ ref('stg_sales') }}  -- <--- dbt comprend que stg_sales doit être exécuté AVANT ce modèle
GROUP BY store