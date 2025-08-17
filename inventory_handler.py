# inventory_handler.py
import os
import json
import boto3

DDB = boto3.resource("dynamodb")
INVENTORY_TABLE = DDB.Table(os.environ["INVENTORY_TABLE"])

def handler(event, context):
    """
    Input from Step Functions (output of Payments step), includes items:
    {
      "orderId": "...",
      "items": [{"sku":"ABC123","qty":2}, {"sku":"XYZ","qty":1}],
      "payment": {...}
    }
    """
    order_id = event.get("orderId")
    items = event.get("items") or []

    if not order_id or not items:
        raise ValueError("orderId and items are required")

    # Try to reserve each item atomically
    for it in items:
        sku = it["sku"]
        qty = int(it["qty"])
        # Expect an attribute "available" in the item. Create seed data up front.
        resp = INVENTORY_TABLE.update_item(
            Key={"sku": sku},
            UpdateExpression="SET available = available - :q",
            ConditionExpression="available >= :q",
            ExpressionAttributeValues={":q": qty},
            ReturnValues="UPDATED_NEW"
        )

    return {
        "orderId": order_id,
        "reservation": {"status": "RESERVED", "items": items},
        **({"payment": event.get("payment")} if "payment" in event else {}),
    }
