import os
import logging
from time import time, strftime

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


def redirect_view(request):
    response = redirect('/admin/')
    return response


class ResumeHit(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1]
        else:
            ip = request.META.get('REMOTE_ADDR')
        file_name = "resume.log"
        logger = logging.getLogger(__name__)
        logger.setLevel(level='INFO')
        if not logger.handlers:
            handler = logging.FileHandler(
                os.path.join(os.path.dirname(
                    os.path.abspath(__file__)), '../log', file_name)
            )
            formatter = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.info(ip)

        return HttpResponse(ip)
