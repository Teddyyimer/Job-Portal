
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Job


def home(request):
    query = request.GET.get('q', '').strip()

    jobs = Job.objects.order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query)
            | Q(company__icontains=query)
            | Q(location__icontains=query)
        )

    context = {
        'jobs': jobs,
        'query': query,
    }

    return render(request, 'jobs/home.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job},
    )
