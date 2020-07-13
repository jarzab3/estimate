import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import EstimateSession
from django.shortcuts import render


def index_view(request):
    return render(request, "index.html")


def estimate_view(request, room_name, name):
    return render(request, 'room.html', {
        'room_name': room_name,
        'name': name
    })


def session_view(request, code):
    print("session_view code: ", code)
    code_display = "Session code: " + str(code)
    return render(request, "session.html", {'data': code_display.upper()})


@api_view(['POST'])
def validate_session_code(request):
    """
    Check if code is ok.
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


@api_view(['POST'])
def validate_session_code_and_password(request):
    """
    """
    if request.method == 'POST':
        code = request.data.get("code", None)
        password = request.data.get("password", None)

        print("code  ", code, "password:  ", password)

        session = EstimateSession.objects.filter(code=code).first()
        print(session.session_password)

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
