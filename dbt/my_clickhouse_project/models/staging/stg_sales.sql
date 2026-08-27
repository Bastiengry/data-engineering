{{ config(
    materialized='table',
    engine='MergeTree()',
    order_by='(store, product_id)'
) }}

SELECT 
    store,
    product_id,
    total_quantity,
    total_revenue,
    now() AS transformed_at
FROM datamart.sales_summary