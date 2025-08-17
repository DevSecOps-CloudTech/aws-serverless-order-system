# shipping_handler.py
import os
import json
import uuid
import boto3
from datetime import datetime, timezone

DDB = boto3.resource("dynamodb")
ORDERS_TABLE = DDB.Table(os.environ.get("ORDERS_TABLE", ""))

def handler(event, context):
    """
    Input from Step Functions (output of Inventory step):
    { "orderId": "...", "items": [...], "payment": {...}, "reservation": {...} }
    """
    order_id = event.get("orderId")
    if not order_id:
        raise ValueError("orderId is required")

    tracking_number = f"TRK-{uuid.uuid4().hex[:12].upper()}"
    shipped_at = datetime.now(timezone.utc).isoformat()

    if ORDERS_TABLE.name:
        ORDERS_TABLE.update_item(
            Key={"orderId": order_id},
            UpdateExpression="SET #s=:sh, trackingNumber=:t, updatedAt=:ts",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":sh": "SHIPPED", ":t": tracking_number, ":ts": shipped_at},
        )

    return {
        "orderId": order_id,
        "shipment": {"status": "CREATED", "trackingNumber": tracking_number, "shippedAt": shipped_at}
    }
