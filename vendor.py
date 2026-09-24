"""
Bulk-create vendors via the add-vendor API, sourcing payload data from two
exported spreadsheets:

  1. VENDOR_FILE   - vendor_id, vendor_name, gst_number, agreement_pdf_url,
                      is_active, is_messaging_active, is_lm, is_fm,
                      vendor_address, rate
  2. CHARGE_FILE   - Vendor ID, Vendor Charge Percent, Vendor Charge Fuel Percent

The two are joined on vendor_id. By default this is a DRY RUN: it prints the
request that would be sent for each vendor without calling the API. Pass
--execute to actually send the requests.

Usage:
    python3 add_vendors.py                # dry run, prints payloads
    python3 add_vendors.py --execute       # actually calls the API
    python3 add_vendors.py --execute --only 45,59   # limit to specific vendor_ids
"""

import argparse
import json
import math
import sys

import pandas as pd
import requests

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Vendor/add-vendor"
NODE_ID = "346"

VENDOR_FILE = "/Users/sachinverma/Downloads/query_result_2026-07-31T07_57_50.268050802Z.xlsx"
CHARGE_FILE = "/Users/sachinverma/Downloads/query_result_2026-07-31T08_01_18.530524598Z.xlsx"


def clean_str(value, default=""):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return str(value).strip()


def clean_bool(value, default=False):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return bool(value)


def clean_rate(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return {}
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}
    return value


def build_payloads():
    vendors = pd.read_excel(VENDOR_FILE)
    charges = pd.read_excel(CHARGE_FILE)

    charges = charges.rename(
        columns={
            "Vendor ID": "vendor_id",
            "Vendor Charge Percent": "vendor_charge_percent",
            "Vendor Charge Fuel Percent": "vendor_charge_fuel_percent",
        }
    )[["vendor_id", "vendor_charge_percent", "vendor_charge_fuel_percent"]]

    merged = vendors.merge(charges, on="vendor_id", how="left", validate="one_to_one")

    missing = merged[merged["vendor_charge_percent"].isna()]
    if not missing.empty:
        print(
            f"WARNING: {len(missing)} vendor(s) have no charge-percent match: "
            f"{missing['vendor_id'].tolist()}",
            file=sys.stderr,
        )

    payloads = []
    for _, row in merged.iterrows():
        payload = {
            "vendorName": clean_str(row["vendor_name"]),
            "gstNumber": clean_str(row["gst_number"]),
            "agreementPdfUrl": clean_str(row.get("agreement_pdf_url")),
            "vendorChargePercent": row["vendor_charge_percent"]
            if not pd.isna(row["vendor_charge_percent"])
            else 0,
            "vendorChargeFuelPercent": row["vendor_charge_fuel_percent"]
            if not pd.isna(row["vendor_charge_fuel_percent"])
            else 0,
            "isActive": clean_bool(row["is_active"], default=True),
            "isLm": clean_bool(row["is_lm"]),
            "isFm": clean_bool(row["is_fm"]),
            "vendorAddress": clean_str(row.get("vendor_address")),
            "rate": clean_rate(row.get("rate")),
            "isMessagingActive": clean_bool(row["is_messaging_active"], default=True),
            "createdBy": None,
        }
        payloads.append((row["vendor_id"], payload))

    return payloads


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually send requests to the API instead of just printing them.",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Comma-separated vendor_id list to restrict to (matches the source vendor_id column).",
    )
    args = parser.parse_args()

    only_ids = None
    if args.only:
        only_ids = {int(x.strip()) for x in args.only.split(",")}

    payloads = build_payloads()

    headers = {"node_id": NODE_ID, "Content-Type": "application/json"}

    for vendor_id, payload in payloads:
        if only_ids is not None and vendor_id not in only_ids:
            continue

        print(f"\n--- vendor_id={vendor_id} ({payload['vendorName']}) ---")
        print(json.dumps(payload, indent=2, default=str))

        if args.execute:
            resp = requests.post(API_URL, headers=headers, json=payload)
            print(f"-> HTTP {resp.status_code}: {resp.text}")
        else:
            print("(dry run - not sent, use --execute to send)")


if __name__ == "__main__":
    main()