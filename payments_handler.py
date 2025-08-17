# payments_handler.py
import os
import json
import boto3
from datetime import datetime, timezone

DDB = boto3.resource("dynamodb")
ORDERS_TABLE = DDB.Table(os.environ.get("ORDERS_TABLE", ""))  # optional use

def handler(event, context):
    """
    Invoked by Step Functions with input like:
    { "orderId": "...", "userId": "...", "amount": 39.98, "items": [...] }
    """
    order_id = event.get("orderId")
    amount = event.get("amount")

    if not order_id or amount is None:
        raise ValueError("orderId and amount are required")

    # ---- Simulate payment call (ALWAYS success in this stub) ----
    payment_id = f"pay_{order_id}"
    paid_at = datetime.now(timezone.utc).isoformat()

    # Optional: update order status (allowed by policy in the template)
    if ORDERS_TABLE.name:
        ORDERS_TABLE.update_item(
            Key={"orderId": order_id},
            UpdateExpression="SET #s = :paid, paymentId=:pid, updatedAt=:ts",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":paid": "PAID", ":pid": payment_id, ":ts": paid_at},
        )

    return {
        "payment": {"status": "SUCCEEDED", "paymentId": payment_id, "paidAt": paid_at},
        "orderId": order_id,
        "amount": amount,
    }
