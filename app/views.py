import json
import logging
from django.template import RequestContext
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404, HttpResponseServerError

from app.models import EstimateSession
from django.shortcuts import render

log = logging.getLogger(__name__)


def index_view(request):
    return render(request, "index.html")


def estimate_view(request, room_name, name):
    session = None
    if request.method == 'POST':
        user = None
        try:
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
        except KeyError:
            log.info("Malformed data!")

        session_return = None
        if user is not None and user.is_active:
            session = EstimateSession.objects.filter(session_admin_user_id=user).first()

            # print(session)

            if session:
                session_return = {
                    'id': session.id,
                    'room_name': room_name,
                    'code': session.code,
                    'date_created': session.date_created,
                    'name': name,
                    'session_name': session.name,
                }
            login(request, user)
            # Set Session Expiry to 0 if user clicks "Remember Me"
            if not request.POST.get('rem', None):
                request.session.set_expiry(0)
            return render(request, 'room.html', session_return)

    try:
        session = EstimateSession.objects.filter(code=room_name).first()
        session_name = session.name
    except Exception:
        session_name = ""

    return render(request, 'room.html', {
        'room_name': room_name,
        'session_name': session_name,
        'name': name,
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


# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def validate_session_code_and_password(request):
    """
    """
    # content = {
    #     'user': str(request.user),  # `django.contrib.auth.User` instance.
    #     'auth': str(request.auth),  # None
    # }
    if request.method == 'POST':
        user = None
        try:
            print(request.POST.get('password'))
            # print(request.POST)
            # json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
            # username = json_data['username']
            # password = json_data['password']
            # code = json_data['code']
            # user = authenticate(request, username=username, password=password)
        except KeyError:
            HttpResponseServerError("Malformed data!")

        session_return = None

        if user is not None and user.is_active:

            # password = request.data.get("password", None)
            session = EstimateSession.objects.filter(session_admin_user_id=user).first()

            print(session)

            if session:
                session_return = {
                    'id': session.id,
                    'name': session.name,
                    'code':
                        session.code,
                    'date_created': session.date_created,
                }

            login(request, user)
            # Set Session Expiry to 0 if user clicks "Remember Me"
            if not request.POST.get('rem', None):
                request.session.set_expiry(0)
        else:
            Response(session_return, status=status.HTTP_403_FORBIDDEN)
            # session_return = {"error": "There was an error logging you in. Please Try again"}
        # return HttpResponse(session_return)
        return render(request, "room.html", {'data': session_return})
        # return Response(session_return, status=status.HTTP_200_OK, template_name='session.html')
        # else:
        # return Response(session_return, status=status.HTTP_403_FORBIDDEN)
