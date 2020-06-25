import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import EstimateSession
from django.shortcuts import render


def estimate_view(request):
    return render(request, "index.html")


def chat_view(request):
    return render(request, "chat.html")


def session_view(request, code):
    print("session_view code: ", code)
    code_display = "Session code: " + str(code)
    return render(request, "session.html", {'data': code_display.upper()})


@api_view(['POST'])
def enter_session(request):
    """
    """
    if request.method == 'POST':
        code = request.data.get("code", None)
        session = EstimateSession.objects.filter(code=code).first()
        session_return = None
        if session:
            session_return = {
                'id': session.id,
                'name': session.name,
                'code':
                    session.code,
                'date_created': session.date_created,
            }

        return Response(session_return, status=status.HTTP_200_OK)
