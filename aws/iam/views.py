from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.text import mark_safe
from iam import iam
from pprint import pprint, pformat
import pytz


tz = pytz.timezone(settings.TIME_ZONE)


def active_users_list(request, json=False):
    users = iam.get_active_users_list()
    if json:
        return JsonResponse(users)
    else:
        return render(request, 'iam/partials/users_list.html', dict(users=users['Users'], title='Active'))


def inactive_users_list(request, json=False):
    users = iam.get_inactive_users_list()
    if json:
        return JsonResponse(users)
    else:
        return render(request, 'iam/partials/users_list.html', dict(users=users['Users'], title='Inactive'))


def users_list(request, json=False):
    users = iam.get_users_list()
    if json:
        return JsonResponse(users)
    else:
        return render(request, 'iam/users_list.html', dict(users=users['Users']))


def delete_inactive_users(request):
    users = iam.get_inactive_users_list()
    if request.method == 'POST':
        if users:
            response = iam.delete_inactive_users()
            messages.success(request, 'Inactive users deleted')
            messages.success(request, '{}'.format(mark_safe(str(response).replace('\n', '<br/>'))))
        else:
            messages.error(request, 'No inactive users to delete')
        response = render(request, 'iam/delete_users.html', dict(users=users['Users']))
    else:
        response = render(request, 'iam/delete_users.html', dict(users=users['Users']))
    return response
