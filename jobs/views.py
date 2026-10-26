from django.shortcuts import render
from .models import Job


def home(request):
    jobs = Job.objects.order_by('-created_at')

    return render(
        request,
        'jobs/home.html',
        {'jobs': jobs},
    )