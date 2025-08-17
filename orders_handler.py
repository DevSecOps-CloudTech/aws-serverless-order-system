# orders_handler.py
import os
import json
import uuid
import boto3
from datetime import datetime, timezone

DDB = boto3.resource("dynamodb")
EVB = boto3.client("events")
SFN = boto3.client("stepfunctions")

ORDERS_TABLE = DDB.Table(os.environ["ORDERS_TABLE"])
EVENTBUS_NAME = os.environ["EVENTBUS_NAME"]
ORDER_WORKFLOW_ARN = os.environ["ORDER_WORKFLOW_ARN"]


def _response(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, context):
    """
    Expects API Gateway HTTP API v2 event.
    Body JSON example:
    {
      "items": [{"sku":"ABC123","qty":2,"price":19.99}],
      "amount": 39.98,
      "clientToken": "optional-idempotency-key"
    }
    """
    try:
        body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")
        payload = json.loads(body)
    except Exception:
        return _response(400, {"message": "Invalid JSON body"})

    items = payload.get("items") or []
    amount = payload.get("amount")
    client_token = payload.get("clientToken")

    if not items or amount is None:
        return _response(400, {"message": "items[] and amount are required"})

    # Identify the caller (from Cognito JWT via HTTP API authorizer)
    claims = (event.get("requestContext", {})
                    .get("authorizer", {})
                    .get("jwt", {})
                    .get("claims", {}))
    user_id = claims.get("sub", "anonymous")

    # Basic idempotency: reuse orderId if clientToken was seen before.
    # (In production you’d persist clientToken→orderId mapping.)
    order_id = str(uuid.uuid4())

    now = datetime.now(timezone.utc).isoformat()
    order_item = {
        "orderId": order_id,
        "userId": user_id,
        "status": "CREATED",
        "amount": amount,
        "items": items,
        "createdAt": now,
        "updatedAt": now,
    }

    # 1) Write order
    ORDERS_TABLE.put_item(
        Item=order_item,
        ConditionExpression="attribute_not_exists(orderId)"  # prevents overwrite
    )

    # 2) Emit domain event
    EVB.put_events(
        Entries=[{
            "Source": "app.orders",
            "DetailType": "OrderCreated",
            "Detail": json.dumps({"orderId": order_id, "userId": user_id, "amount": amount}),
            "EventBusName": EVENTBUS_NAME,
        }]
    )

    # 3) Orchestrate downstream steps
    SFN.start_execution(
        stateMachineArn=ORDER_WORKFLOW_ARN,
        input=json.dumps({"orderId": order_id, "userId": user_id, "amount": amount, "items": items})
    )

    return _response(201, {"orderId": order_id, "status": "CREATED"})
