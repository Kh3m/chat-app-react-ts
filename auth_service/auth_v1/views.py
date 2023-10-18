from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .policy_engine import evaluate_policy


class Evaluate_request(APIView):
    """
    Evaluates a request
    """

    def post(self, request, format=None):
        method = request.data.get('method', None)
        auth_token = request.data.get('auth_token', None)
        request_path = request.data.get("request_path", None)

        for item in [method, auth_token, request_path]:
            if item is None:
                return Response({"error": f"Missing {item}"}, status=status.HTTP_400_BAD_REQUEST)

        result = evaluate_policy(auth_token, request_path, method)
        return Response({"result": result}, status=status.HTTP_200_OK)
