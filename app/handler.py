import json
import os
from datetime import datetime, timezone


def lambda_handler(event, context):
    """Return the health status of the Project Atlas service."""
    response = {
        "status": "healthy",
        "service": "project-atlas",
        "version": os.getenv("APP_VERSION", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": getattr(context, "aws_request_id", "local"),
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response),
    }
