import os
from datetime import datetime, timezone

import pandas as pd
import requests
from requests import Response

# =====================
# CONFIGURATION
# =====================

METABASE_URL = "https://metabase.blitznow.in"
API_KEY = os.environ.get("METABASE_API_KEY", "").strip()
DATABASE_ID = 9  # Simplee Analytics

# Date range (UTC) — update these before each run
START_DATE = "2026-05-07 00:00:00.000 +00:00"
END_DATE = "2026-06-15 00:00:00.000 +00:00"

# Optional: fetch a saved Metabase card instead of running SQL below
# Example: CARD_ID = 6355
CARD_ID = None

TICKET_QUERY = """
WITH date_range AS (
  SELECT
    CAST('{start_date}' AS timestamptz) AS start_at,
    CAST('{end_date}' AS timestamptz) AS end_at
),
quick_hub_nodes AS (
  SELECT
    node_id,
    node_name,
    team_names,
    city_name,
    node_type
  FROM
    "application_db"."node"
  WHERE
    city_name = 'Mumbai'
    AND node_type = 'quick_hub'
)
SELECT
  e.id AS "id",
  e.created_at AS "created_at",
  e.amount AS "amount",
  e.entity_id AS "entity_id",
  e.entity_type AS "entity_type",
  e.entry_type AS "entry_type",
  e.remarks AS "remarks",
  e.unique_payment_id AS "unique_payment_id",
  e.reference_id AS "reference_id",
  e.created_by AS "created_by",
  e.closing_balance AS "closing_balance",
  e.payment_at AS "payment_at",
  n.node_id AS "Node - Entity__node_id",
  n.node_name AS "Node - Entity__node_name",
  n.team_names AS "Node - Entity__team_names",
  n.city_name AS "Node - Entity__city_name",
  n.node_type AS "Node - Entity__node_type"
FROM
  "application_db"."entries" e
  INNER JOIN quick_hub_nodes n ON e.entity_id = n.node_id
  CROSS JOIN date_range dr
WHERE
  (e.remarks <> 'UPI Deposit' OR e.remarks IS NULL)
  AND (e.entry_type <> 'Deposit' OR e.entry_type IS NULL)
  AND e.created_at >= dr.start_at
  AND e.created_at < dr.end_at + interval '1 day'
ORDER BY
  e.created_at DESC
LIMIT
  1048575;
"""


def normalize_api_key(api_key: str) -> str:
    if api_key.startswith("API-"):
        return api_key[len("API-") :]
    return api_key


def require_api_key() -> str:
    if API_KEY:
        return API_KEY
    raise ValueError(
        "METABASE_API_KEY is not set. Export a valid Metabase API key before "
        "running this script, for example: export METABASE_API_KEY='API-mb_...'"
    )


def fetch_from_card(card_id: int, api_key: str) -> list[dict]:
    url = f"{METABASE_URL}/api/card/{card_id}/query/json"
    headers = {"x-api-key": normalize_api_key(api_key)}

    response = requests.post(url, headers=headers, timeout=120)
    raise_for_status_with_details(response)
    return response.json()


def fetch_from_sql(
    sql: str,
    database_id: int,
    api_key: str,
) -> list[dict]:
    url = f"{METABASE_URL}/api/dataset/json"
    headers = {
        "x-api-key": normalize_api_key(api_key),
        "Content-Type": "application/json",
    }
    payload = {
        "query": {
            "database": database_id,
            "type": "native",
            "native": {"query": sql},
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=300)
    raise_for_status_with_details(response)
    return response.json()


def raise_for_status_with_details(response: Response) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text.strip()
        if detail:
            raise requests.HTTPError(
                f"{exc}; Metabase response: {detail[:2000]}",
                response=response,
            ) from exc
        raise


def build_output_filename() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%S.%fZ")
    return f"query_result_{timestamp}.xlsx"


def main() -> None:
    if CARD_ID:
        print(f"Fetching Metabase card {CARD_ID}...")
        data = fetch_from_card(CARD_ID, require_api_key())
    else:
        sql = TICKET_QUERY.format(start_date=START_DATE, end_date=END_DATE)
        print(
            f"Fetching entries from {START_DATE} to {END_DATE} "
            f"(database {DATABASE_ID})..."
        )
        data = fetch_from_sql(sql, DATABASE_ID, require_api_key())

    if not isinstance(data, list):
        raise ValueError(f"Unexpected Metabase response type: {type(data)}")

    output_file = build_output_filename()
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

    print(f"Fetched {len(df)} rows")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
