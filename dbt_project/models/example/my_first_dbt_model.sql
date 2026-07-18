{{ config(materialized='table', schema='RAW') }}

with source_data as (

    select
        *
    from {{ source('RAW', 'ORDERS') }}

)

select *
from source_data

