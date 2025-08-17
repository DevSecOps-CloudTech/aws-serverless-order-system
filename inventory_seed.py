#!/usr/bin/env python3
"""
Seed DynamoDB InventoryTable with example SKUs.

Usage:
  export AWS_REGION=us-east-1
  export INVENTORY_TABLE=ComposerDemo-dev-inventory
  # Option A: use built-in sample list
  python inventory_seed.py

  # Option B: load from a JSON file (list with sku/available/name/price)
  python inventory_seed.py --file sku_seed_list.json
"""
import os
import json
import argparse
import boto3
from botocore.exceptions import ClientError


def load_items(path: str | None):
    if not path:
        # fallback example items
        return [
            {"sku": "ABC123", "available": 100, "name": "Blue T-Shirt (M)", "price": 19.99},
            {"sku": "ABC124", "available": 50,  "name": "Blue T-Shirt (L)", "price": 19.99},
            {"sku": "XYZ789", "available": 200, "name": "Coffee Mug", "price": 9.99},
            {"sku": "LMN456", "available": 30,  "name": "Wireless Mouse", "price": 24.99},
            {"sku": "BKL321", "available": 75,  "name": "Notebook (A5)", "price": 4.99}
        ]
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to JSON list of items to seed")
    args = parser.parse_args()

    region = os.environ.get("AWS_REGION", "us-east-1")
    table_name = os.environ.get("INVENTORY_TABLE")
    if not table_name:
        raise SystemExit("Set INVENTORY_TABLE environment variable to your DynamoDB table name.")

    items = load_items(args.file)
    ddb = boto3.resource("dynamodb", region_name=region)
    table = ddb.Table(table_name)

    # Upsert by partition key 'sku'
    with table.batch_writer(overwrite_by_pkeys=["sku"]) as batch:
        for it in items:
            # minimal validation
            if "sku" not in it or "available" not in it:
                print(f"Skipping invalid item: {it}")
                continue
            batch.put_item(Item=it)
            print(f"Upserted SKU {it['sku']} (available={it['available']})")

    print("Done.")


if __name__ == "__main__":
    main()
