import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Return the health status of the Project Atlas service."""
    response = {
        "status": "healthy",
        "service": "project-atlas",
        "version": os.environ.get("APP_VERSION", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": getattr(context, "aws_request_id", "local"),
    }

    logger.info(
        json.dumps(
            {
                "event": "health_check",
                "status": response["status"],
                "service": response["service"],
                "version": response["version"],
                "request_id": response["request_id"],
            }
        )
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response),
    }
