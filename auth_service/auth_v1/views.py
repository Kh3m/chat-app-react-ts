from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.openapi import AutoSchema

import logging
from .policy_engine import evaluate_policy

# import consumers to run consumers
from .events import consumers

logger = logging.getLogger("auth_v1")


class Evaluate_request(APIView):
    """
    Evaluates a request
    """
    schema = AutoSchema()

    def post(self, request, format=None):
        data = {
            "method": request.data.get('method', None),
            "service": request.data.get('service', None),
            "auth_token": request.data.get('auth_token', None),
            "req_path": request.data.get("request_path", None)
        }

        for item_name, item in data.items():
            if not item:
                return Response({"error": f"Missing {item_name}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = evaluate_policy(**data)
            return Response({"result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({
                "Error": "Failed to evaluate request",
                "detail": e
            })
            return Response({"error": "Failed to evaluate request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
