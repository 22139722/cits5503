from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ec2 import ec2


def instances_list(request, json=False):
    instances = ec2.get_instances()
    if json:
        return JsonResponse(dict(instances=instances))
    else:
        return render(request, 'ec2/instances_list.html', dict(instances=instances))


def old_instances_list(request, json=False):
    instances = ec2.get_old_instances()
    summary_only = request.GET.get('summary_only', False)
    if json:
        return JsonResponse(dict(instances=instances))
    else:
        return render(request, 'ec2/partials/instances_list.html', dict(instances=instances, title='Old Instances (> 12 hours)', summary_only=summary_only))


def young_instances_list(request, json=False):
    instances = ec2.get_young_instances()
    summary_only = request.GET.get('summary_only', False)
    if json:
        return JsonResponse(dict(instances=instances))
    else:
        return render(request, 'ec2/partials/instances_list.html', dict(instances=instances, title='Young Instances (<= 12 hours)', summary_only=summary_only))


def terminate_instances(request):
    
    instances = ec2.get_instances_for_termination()

    if request.method == 'POST':
        ec2.terminate_instances()
        messages.success(request, '{} instances terminated'.format(len(instances)))
        response = redirect('ec2:instances_list')
    else:
        response = render(request, 'ec2/terminate_instances.html', dict(instances=instances))

    return response
