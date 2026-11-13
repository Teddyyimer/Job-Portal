
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Job
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import Application





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

##Job application section

@login_required(login_url='login')
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    existing_application = Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if existing_application:
        messages.info(
            request,
            'You have already applied for this job.'
        )
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(
                request,
                'Your application was submitted successfully!'
            )
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(
        request,
        'jobs/apply.html',
        {'form': form, 'job': job}
    )

#my applications section

@login_required(login_url='login')
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job')

    return render(
        request,
        'jobs/my_applications.html',
        {'applications': applications}
    )
