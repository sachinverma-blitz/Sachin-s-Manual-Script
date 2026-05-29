import os
from datetime import datetime, timezone

import pandas as pd
import requests

# =====================
# CONFIGURATION
# =====================

METABASE_URL = "https://metabase.blitznow.in"
API_KEY = os.environ.get(
    "METABASE_API_KEY",
    "API-mb_sspK9uNcxNA0zQePG403tMbEw/afgld7LEM4NtpOU2A=",
)
DATABASE_ID = 9  # Simplee Analytics

# Date range (UTC) — update these before each run
START_DATE = "2026-04-29 00:00:00.000 +00:00"
END_DATE = "2026-05-28 00:00:00.000 +00:00"

# Optional: fetch a saved Metabase card instead of running SQL below
# Example: CARD_ID = 6355
CARD_ID = None

TICKET_QUERY = """
SELECT
  "application_db"."ticket"."id" AS "id",
  "application_db"."ticket"."ticket_id" AS "ticket_id",
  "application_db"."ticket"."priority" AS "priority",
  "application_db"."ticket"."status" AS "status",
  "application_db"."ticket"."created_time" AS "created_time",
  "application_db"."ticket"."update_time" AS "update_time",
  "application_db"."ticket"."agent" AS "agent",
  "application_db"."ticket"."org_id" AS "org_id",
  "application_db"."ticket"."due_by" AS "due_by",
  "application_db"."ticket"."ticket_agent_id" AS "ticket_agent_id",
  "application_db"."ticket"."ticket_type_id" AS "ticket_type_id",
  "application_db"."ticket"."created_by" AS "created_by",
  "application_db"."ticket"."cc_email_list" AS "cc_email_list",
  "application_db"."ticket"."updated_by" AS "updated_by",
  "Support Conversation"."id" AS "Support Conversation__id",
  "Support Conversation"."customer_id" AS "Support Conversation__customer_id",
  "Support Conversation"."status" AS "Support Conversation__status",
  "Support Conversation"."start_time" AS "Support Conversation__start_time",
  "Support Conversation"."end_time" AS "Support Conversation__end_time",
  "Support Conversation"."total_messages" AS "Support Conversation__total_messages",
  "Support Conversation"."last_interaction" AS "Support Conversation__last_interaction",
  "Support Conversation"."conversation_notes" AS "Support Conversation__conversation_notes",
  "Support Conversation"."customer_metadata" AS "Support Conversation__customer_metadata",
  "Support Conversation"."average_response_time_ms" AS "Support Conversation__average_response_time_ms",
  "Support Conversation"."created_at" AS "Support Conversation__created_at",
  "Support Conversation"."updated_at" AS "Support Conversation__updated_at",
  "Support Conversation"."ticket_id" AS "Support Conversation__ticket_id",
  "Support Conversation"."last_interaction_by" AS "Support Conversation__last_interaction_by",
  "Support Message"."id" AS "Support Message__id",
  "Support Message"."sender_type" AS "Support Message__sender_type",
  "Support Message"."message_type" AS "Support Message__message_type",
  "Support Message"."attachments" AS "Support Message__attachments",
  "Support Message"."read_at" AS "Support Message__read_at",
  "Support Message"."client_message_id" AS "Support Message__client_message_id",
  "Support Message"."metadata" AS "Support Message__metadata",
  "Support Message"."created_at" AS "Support Message__created_at",
  "Support Message"."updated_at" AS "Support Message__updated_at",
  "Support Message"."body" AS "Support Message__body",
  "Support Message"."conversation_id" AS "Support Message__conversation_id",
  ("Ticket Type"."data" #>> array [ 'checkCod' ] :: text [ ]) :: boolean AS "Ticket Type__data → checkCod",
  (
    "Ticket Type"."data" #>> array [ 'closing_status' ] :: text [ ]
  ) :: text AS "Ticket Type__data → closing_status",
  (
    "Ticket Type"."data" #>> array [ 'excluded_status' ] :: text [ ]
  ) :: text AS "Ticket Type__data → excluded_status",
  (
    "Ticket Type"."data" #>> array [ 'isAllowedForOnDemand' ] :: text [ ]
  ) :: boolean AS "Ticket Type__data → isAllowedForOnDemand",
  (
    "Ticket Type"."data" #>> array [ 'isAllowedForSdd' ] :: text [ ]
  ) :: boolean AS "Ticket Type__data → isAllowedForSdd",
  ("Ticket Type"."data" #>> array [ 'isPickup' ] :: text [ ]) :: boolean AS "Ticket Type__data → isPickup",
  ("Ticket Type"."data" #>> array [ 'isReturn' ] :: text [ ]) :: boolean AS "Ticket Type__data → isReturn",
  (
    "Ticket Type"."data" #>> array [ 'opening_status' ] :: text [ ]
  ) :: text AS "Ticket Type__data → opening_status",
  (
    "Ticket Type"."data" #>> array [ 'showOnClientPanel' ] :: text [ ]
  ) :: boolean AS "Ticket Type__data → showOnClientPanel",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'en' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → en",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'hi' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → hi",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'kn' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → kn",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'mr' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → mr",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'ta' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → ta",
  (
    "Ticket Type"."data" #>> array [ 'subtype_i18n',
    'te' ] :: text [ ]
  ) :: text AS "Ticket Type__data → subtype_i18n → te",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'en' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → en",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'hi' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → hi",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'kn' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → kn",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'mr' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → mr",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'ta' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → ta",
  (
    "Ticket Type"."data" #>> array [ 'type_i18n',
    'te' ] :: text [ ]
  ) :: text AS "Ticket Type__data → type_i18n → te",
  "Ticket Type"."id" AS "Ticket Type__id",
  "Ticket Type"."type" AS "Ticket Type__type",
  "Ticket Type"."subtype" AS "Ticket Type__subtype",
  "Ticket Type"."event" AS "Ticket Type__event",
  "Ticket Type"."ticket_group_id" AS "Ticket Type__ticket_group_id",
  "Ticket Type"."data" AS "Ticket Type__data",
  "Ticket Type"."action" AS "Ticket Type__action"
FROM
  "application_db"."ticket"
  LEFT JOIN (
    SELECT
      "application_db"."support_conversation"."id" AS "id",
      "application_db"."support_conversation"."customer_id" AS "customer_id",
      "application_db"."support_conversation"."status" AS "status",
      "application_db"."support_conversation"."start_time" AS "start_time",
      "application_db"."support_conversation"."end_time" AS "end_time",
      "application_db"."support_conversation"."total_messages" AS "total_messages",
      "application_db"."support_conversation"."last_interaction" AS "last_interaction",
      "application_db"."support_conversation"."conversation_notes" AS "conversation_notes",
      "application_db"."support_conversation"."customer_metadata" AS "customer_metadata",
      "application_db"."support_conversation"."average_response_time_ms" AS "average_response_time_ms",
      "application_db"."support_conversation"."created_at" AS "created_at",
      "application_db"."support_conversation"."updated_at" AS "updated_at",
      "application_db"."support_conversation"."ticket_id" AS "ticket_id",
      "application_db"."support_conversation"."last_interaction_by" AS "last_interaction_by"
    FROM
      "application_db"."support_conversation"
  ) AS "Support Conversation" ON "application_db"."ticket"."id" = "Support Conversation"."ticket_id"
  LEFT JOIN (
    SELECT
      "application_db"."support_message"."id" AS "id",
      "application_db"."support_message"."sender_type" AS "sender_type",
      "application_db"."support_message"."message_type" AS "message_type",
      "application_db"."support_message"."attachments" AS "attachments",
      "application_db"."support_message"."read_at" AS "read_at",
      "application_db"."support_message"."client_message_id" AS "client_message_id",
      "application_db"."support_message"."metadata" AS "metadata",
      "application_db"."support_message"."created_at" AS "created_at",
      "application_db"."support_message"."updated_at" AS "updated_at",
      "application_db"."support_message"."body" AS "body",
      "application_db"."support_message"."conversation_id" AS "conversation_id"
    FROM
      "application_db"."support_message"
  ) AS "Support Message" ON "Support Conversation"."id" = "Support Message"."conversation_id"
  LEFT JOIN (
    SELECT
      (
        "application_db"."ticket_type"."data" #>> array [ 'checkCod' ] :: text [ ]
      ) :: boolean AS "data → checkCod",
      (
        "application_db"."ticket_type"."data" #>> array [ 'closing_status' ] :: text [ ]
      ) :: text AS "data → closing_status",
      (
        "application_db"."ticket_type"."data" #>> array [ 'excluded_status' ] :: text [ ]
      ) :: text AS "data → excluded_status",
      (
        "application_db"."ticket_type"."data" #>> array [ 'isAllowedForOnDemand' ] :: text [ ]
      ) :: boolean AS "data → isAllowedForOnDemand",
      (
        "application_db"."ticket_type"."data" #>> array [ 'isAllowedForSdd' ] :: text [ ]
      ) :: boolean AS "data → isAllowedForSdd",
      (
        "application_db"."ticket_type"."data" #>> array [ 'isPickup' ] :: text [ ]
      ) :: boolean AS "data → isPickup",
      (
        "application_db"."ticket_type"."data" #>> array [ 'isReturn' ] :: text [ ]
      ) :: boolean AS "data → isReturn",
      (
        "application_db"."ticket_type"."data" #>> array [ 'opening_status' ] :: text [ ]
      ) :: text AS "data → opening_status",
      (
        "application_db"."ticket_type"."data" #>> array [ 'showOnClientPanel' ] :: text [ ]
      ) :: boolean AS "data → showOnClientPanel",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'en' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → en",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'hi' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → hi",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'kn' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → kn",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'mr' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → mr",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'ta' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → ta",
      (
        "application_db"."ticket_type"."data" #>> array [ 'subtype_i18n',
        'te' ] :: text [ ]
      ) :: text AS "data → subtype_i18n → te",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'en' ] :: text [ ]
      ) :: text AS "data → type_i18n → en",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'hi' ] :: text [ ]
      ) :: text AS "data → type_i18n → hi",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'kn' ] :: text [ ]
      ) :: text AS "data → type_i18n → kn",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'mr' ] :: text [ ]
      ) :: text AS "data → type_i18n → mr",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'ta' ] :: text [ ]
      ) :: text AS "data → type_i18n → ta",
      (
        "application_db"."ticket_type"."data" #>> array [ 'type_i18n',
        'te' ] :: text [ ]
      ) :: text AS "data → type_i18n → te",
      "application_db"."ticket_type"."id" AS "id",
      "application_db"."ticket_type"."type" AS "type",
      "application_db"."ticket_type"."subtype" AS "subtype",
      "application_db"."ticket_type"."event" AS "event",
      "application_db"."ticket_type"."ticket_group_id" AS "ticket_group_id",
      "application_db"."ticket_type"."data" AS "data",
      "application_db"."ticket_type"."action" AS "action"
    FROM
      "application_db"."ticket_type"
  ) AS "Ticket Type" ON "application_db"."ticket"."ticket_type_id" = "Ticket Type"."id"
WHERE
  ("application_db"."ticket"."org_id" = 'rider')
  AND (
    "application_db"."ticket"."created_time" >= CAST(
      CAST((NOW() + INTERVAL '-30 day') AS date) AS timestamptz
    )
  )
  AND (
    "application_db"."ticket"."created_time" < CAST(CAST(NOW() AS date) AS timestamptz)
  )
ORDER BY
  "application_db"."ticket"."created_time" DESC
LIMIT
  1048575
"""


def normalize_api_key(api_key: str) -> str:
    if api_key.startswith("API-"):
        return api_key[len("API-") :]
    return api_key


def fetch_from_card(card_id: int, api_key: str) -> list[dict]:
    url = f"{METABASE_URL}/api/card/{card_id}/query/json"
    headers = {"x-api-key": normalize_api_key(api_key)}

    response = requests.post(url, headers=headers, timeout=120)
    response.raise_for_status()
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
    response.raise_for_status()
    return response.json()


def build_output_filename() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%S.%fZ")
    return f"query_result_{timestamp}.xlsx"


def main() -> None:
    if CARD_ID:
        print(f"Fetching Metabase card {CARD_ID}...")
        data = fetch_from_card(CARD_ID, API_KEY)
    else:
        sql = TICKET_QUERY.format(start_date=START_DATE, end_date=END_DATE)
        print(
            f"Fetching tickets from {START_DATE} to {END_DATE} "
            f"(database {DATABASE_ID})..."
        )
        data = fetch_from_sql(sql, DATABASE_ID, API_KEY)

    if not isinstance(data, list):
        raise ValueError(f"Unexpected Metabase response type: {type(data)}")

    output_file = build_output_filename()
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

    print(f"Fetched {len(df)} rows")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()