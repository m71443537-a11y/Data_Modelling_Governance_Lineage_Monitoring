{{ config(materialized='table', schema='RAW') }}

with source as (
    select
        *
    from {{ ref('my_first_dbt_model') }}
)

select
    *
from source
