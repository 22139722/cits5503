from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.text import mark_safe
from iam import iam
from pprint import pprint, pformat
import pytz


tz = pytz.timezone(settings.TIME_ZONE)


def active_users_list(request, json=False):
    users = iam.get_active_users_list(path_prefix='/')
    if json:
        return JsonResponse(users)
    else:
        return render(request, 'iam/partials/users_list.html', dict(users=users['Users'], title='Active /'))


def inactive_users_list(request, json=False):
    users = iam.get_inactive_users_list(path_prefix='/CITS5503')
    if json:
        return JsonResponse(users)
    else:
        return render(request, 'iam/partials/users_list.html', dict(users=users['Users'], title='Inactive /CITS5503'))


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


def user(request, username, json=False):
    user = iam.get_user(username)
    if json:
        return JsonResponse(user)
    else:
        return render(request, 'iam/user.html', dict(iam_user=user))


def update_user_path(request, username, new_path):
    if request.method == 'POST':
        iam.update_user_path(username, '/{}/'.format(new_path))
        messages.success(request, 'User path updated to {}'.format(new_path))
    return redirect('iam:user', username)

