
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Job
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm




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
## user registration section

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'jobs/register.html', {'form': form})
