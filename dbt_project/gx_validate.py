import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToBeInSet,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToMatchRegex,
    ExpectTableRowCountToBeBetween,
)

# ── Step 1: Get context ──────────────────────────────────────────
context = gx.get_context()

# ── Step 2: Connect to Snowflake ─────────────────────────────────
data_source = context.data_sources.add_snowflake(
    name="snowflake_source",
    connection_string=(
        "snowflake://MuneebAhmad:muneebahmad1123!GG@br88058.me-central2.gcp"
        "/PRACTICE_DB/RAW"
        "?warehouse=COMPUTE_WH&role=ACCOUNTADMIN"
    ),
)

# ════════════════════════════════════════════════════════════════
#   CHECK 1 — NULL customer_id
# ════════════════════════════════════════════════════════════════
asset_1 = data_source.add_query_asset(
    name="null_customer_check",
    query="""
        SELECT customer_id
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_1 = asset_1.add_batch_definition_whole_table("batch_1").get_batch()
suite_1 = context.suites.add(gx.ExpectationSuite(name="suite_null_customer"))
suite_1.add_expectation(ExpectColumnValuesToNotBeNull(column="CUSTOMER_ID"))
result_1 = batch_1.validate(suite_1)


# ════════════════════════════════════════════════════════════════
#   CHECK 2 — NULL email
# ════════════════════════════════════════════════════════════════
asset_2 = data_source.add_query_asset(
    name="null_email_check",
    query="""
        SELECT customer_email
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_2 = asset_2.add_batch_definition_whole_table("batch_2").get_batch()
suite_2 = context.suites.add(gx.ExpectationSuite(name="suite_null_email"))
suite_2.add_expectation(ExpectColumnValuesToNotBeNull(column="CUSTOMER_EMAIL"))
result_2 = batch_2.validate(suite_2)


# ════════════════════════════════════════════════════════════════
#   CHECK 3 — DUPLICATE order_id
# ════════════════════════════════════════════════════════════════
asset_3 = data_source.add_query_asset(
    name="duplicate_order_check",
    query="""
        SELECT order_id
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_3 = asset_3.add_batch_definition_whole_table("batch_3").get_batch()
suite_3 = context.suites.add(gx.ExpectationSuite(name="suite_duplicate_order"))
suite_3.add_expectation(ExpectColumnValuesToBeUnique(column="ORDER_ID"))
result_3 = batch_3.validate(suite_3)


# ════════════════════════════════════════════════════════════════
#   CHECK 4 — INVALID STATUS values
# ════════════════════════════════════════════════════════════════
asset_4 = data_source.add_query_asset(
    name="invalid_status_check",
    query="""
        SELECT status
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_4 = asset_4.add_batch_definition_whole_table("batch_4").get_batch()
suite_4 = context.suites.add(gx.ExpectationSuite(name="suite_invalid_status"))
suite_4.add_expectation(ExpectColumnValuesToBeInSet(
    column="STATUS",
    value_set=["pending", "shipped", "delivered", "cancelled"]
))
result_4 = batch_4.validate(suite_4)


# ════════════════════════════════════════════════════════════════
#   CHECK 5 — NEGATIVE amount
# ════════════════════════════════════════════════════════════════
asset_5 = data_source.add_query_asset(
    name="negative_amount_check",
    query="""
        SELECT amount
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_5 = asset_5.add_batch_definition_whole_table("batch_5").get_batch()
suite_5 = context.suites.add(gx.ExpectationSuite(name="suite_negative_amount"))
suite_5.add_expectation(ExpectColumnValuesToBeBetween(
    column="AMOUNT",
    min_value=0,
    max_value=100000
))
result_5 = batch_5.validate(suite_5)


# ════════════════════════════════════════════════════════════════
#   CHECK 6 — NEGATIVE quantity
# ════════════════════════════════════════════════════════════════
asset_6 = data_source.add_query_asset(
    name="negative_quantity_check",
    query="""
        SELECT quantity
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_6 = asset_6.add_batch_definition_whole_table("batch_6").get_batch()
suite_6 = context.suites.add(gx.ExpectationSuite(name="suite_negative_quantity"))
suite_6.add_expectation(ExpectColumnValuesToBeBetween(
    column="QUANTITY",
    min_value=1,
    max_value=1000
))
result_6 = batch_6.validate(suite_6)


# ════════════════════════════════════════════════════════════════
#   CHECK 7 — INVALID email format
# ════════════════════════════════════════════════════════════════
asset_7 = data_source.add_query_asset(
    name="invalid_email_check",
    query="""
        SELECT customer_email
        FROM PRACTICE_DB.RAW.ORDERS
        WHERE customer_email IS NOT NULL   -- skip nulls, already caught above
    """,
)
batch_7 = asset_7.add_batch_definition_whole_table("batch_7").get_batch()
suite_7 = context.suites.add(gx.ExpectationSuite(name="suite_invalid_email"))
suite_7.add_expectation(ExpectColumnValuesToMatchRegex(
    column="CUSTOMER_EMAIL",
    regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
))
result_7 = batch_7.validate(suite_7)


# ════════════════════════════════════════════════════════════════
#   CHECK 8 — ROW COUNT sanity check
# ════════════════════════════════════════════════════════════════
asset_8 = data_source.add_query_asset(
    name="row_count_check",
    query="""
        SELECT *
        FROM PRACTICE_DB.RAW.ORDERS
    """,
)
batch_8 = asset_8.add_batch_definition_whole_table("batch_8").get_batch()
suite_8 = context.suites.add(gx.ExpectationSuite(name="suite_row_count"))
suite_8.add_expectation(ExpectTableRowCountToBeBetween(
    min_value=1,
    max_value=10000000
))
result_8 = batch_8.validate(suite_8)


# ════════════════════════════════════════════════════════════════
#   CHECK 9 — BUSINESS RULE: high value orders must be shipped or delivered
# ════════════════════════════════════════════════════════════════
asset_9 = data_source.add_query_asset(
    name="high_value_orders_check",
    query="""
        SELECT status
        FROM PRACTICE_DB.RAW.ORDERS
        WHERE amount > 500          -- only check expensive orders
    """,
)
batch_9 = asset_9.add_batch_definition_whole_table("batch_9").get_batch()
suite_9 = context.suites.add(gx.ExpectationSuite(name="suite_high_value_orders"))
suite_9.add_expectation(ExpectColumnValuesToBeInSet(
    column="STATUS",
    value_set=["shipped", "delivered"]
))
result_9 = batch_9.validate(suite_9)


# ════════════════════════════════════════════════════════════════
#   FINAL RESULTS SUMMARY
# ════════════════════════════════════════════════════════════════
all_results = {
    "NULL customer_id":          result_1,
    "NULL email":                result_2,
    "DUPLICATE order_id":        result_3,
    "INVALID status":            result_4,
    "NEGATIVE amount":           result_5,
    "NEGATIVE quantity":         result_6,
    "INVALID email format":      result_7,
    "ROW COUNT check":           result_8,
    "HIGH VALUE orders status":  result_9,
}

print("\n")
print("=" * 55)
print("         GREAT EXPECTATIONS — DQ REPORT")
print("=" * 55)

passed = 0
failed = 0

for check_name, result in all_results.items():
    status = "✅ PASS" if result.success else "❌ FAIL"
    if result.success:
        passed += 1
    else:
        failed += 1
    print(f"  {status}  |  {check_name}")

print("-" * 55)
print(f"  Total Checks : {len(all_results)}")
print(f"  Passed       : {passed}")
print(f"  Failed       : {failed}")
print("=" * 55)
context.open_data_docs()