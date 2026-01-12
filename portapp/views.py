import uuid
from django.shortcuts import render,redirect,get_object_or_404
from .forms import DocumentsForm, LoginForm, UserForm, CompanyForm, ContractForm, Loginformcheck,UserProfileForm,JobForm,TenderForm, InterviewForm, AgreementUploadForm, WorkStatusReportForm, ImportForm
from .models import CompanyNotification, Documents, Login, user_register, company_register, contract_register,job,job_apply,Interview,News,Ship,Export,Complaint,Notification,Tender,TenderApplication,ExportProduct, Payment,ShipLocation,ProductStatus,Chat,WorkStatusReport,Alerts, Import
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
import re
def admin(request):
    return render(request,'admin.html')

def user(request):
    return render(request,'user.html')

def company(request):
    return render(request,'company.html')

def contract(request):
    return render(request,'contract.html')

def user_login(request):
    return render(request,'login_user.html')
def create_job(request):
    return render(request,'job.html')
def view_jobs(request):
    return render(request,'view_jobs.html')
def edit_job(request):
    return render(request,'edit_job.html')
def delete_job(request):
    return render(request,'delete_job.html')
def user_job_view(request):
    return render(request,'user_view_jobs.html')
def user_job_apply(request):
    return render(request,'apply_job.html')
def job_applications(request):
    return render(request,'job_applications.html')
def accept_application(request):
    return render(request,'accept_application.html')
def reject_application(request):
    return render(request,'reject_application.html')
def job_status(request):
    return render(request,'job_status.html')
def manage_interviews(request):
    return render(request,'manage_interviews.html')

def register_user(request):
    errors = []
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = LoginForm(request.POST)

        # Password length check
        if len(request.POST.get('password', '')) < 6:
            errors.append("Password must be at least 6 characters.")

        if form1.is_valid() and form2.is_valid() and not errors:

            flag = form2.save(commit=False)
            flag.user_type = 'user'
            flag.save()

            flag1 = form1.save(commit=False)
            flag1.login = flag
            flag1.save()

            return redirect('register_user')

    else:
        form1 = UserForm()
        form2 = LoginForm()

    return render(request, 'user_register.html', {'form1': form1, 'form2': form2, 'errors': errors})
def register_company(request):
    if request.method == 'POST':
        form1 = CompanyForm(request.POST, request.FILES)
        form2 = LoginForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            login_instance = form2.save(commit=False)
            login_instance.user_type = 'company'
            login_instance.save()

            company_instance = form1.save(commit=False)
            company_instance.login = login_instance  # Ensure ForeignKey is set
            company_instance.save()

            return redirect('register_company')

    else:
        form1 = CompanyForm()
        form2 = LoginForm()

    return render(request, 'company_register.html', {'form1': form1, 'form2': form2})
def register_contract(request):
    if request.method == 'POST':
        form1 = ContractForm(request.POST)
        form2 = LoginForm(request.POST)

        if form1.is_valid() and form2.is_valid():

            flag = form2.save(commit=False)
            flag.user_type = 'contract'
            flag.save()

            flag1 = form1.save(commit=False)
            flag1.login = flag
            flag1.save()

            return redirect('register_contract')

    else:
        form1 = ContractForm()
        form2 = LoginForm()

    return render(request, 'contract_register.html', {'form1': form1, 'form2': form2})
def user_login(request):
    if request.method == 'POST':
        form = Loginformcheck(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Login.objects.get(email=email)
                if user.password == password:
                    # Set status to active on successful login
                    user.status = 1
                    user.save()
                    # Clear all session keys before setting new ones
                    request.session.flush()
                    if user.user_type == 'user':
                        request.session['user_id'] = user.id
                        return redirect('user')
                    elif user.user_type == 'company':
                        request.session['company_id'] = user.id
                        return redirect('company')
                    elif user.user_type == 'contract':
                        request.session['contract_id'] = user.id
                        return redirect('contract')
                    elif user.user_type == 'admin':
                        request.session['user_type'] = 'admin'
                        request.session['admin_id'] = user.id
                        return redirect('admin')
                    else:
                        messages.error(request, "Unknown user type.")
                else:
                    messages.error(request, "Invalid password.")
            except Login.DoesNotExist:
                messages.error(request, "Invalid email.")
    else:
        form = Loginformcheck()
    
    return render(request, 'login_user.html', {'form': form})
import re

import re
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def update_user_profile(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    user_id = request.session.get('user_id')
    user_profile = get_object_or_404(user_register, login_id=user_id)
    login_obj = user_profile.login
    profile_message = None

    if request.method == 'POST':
        name = request.POST.get('username')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        # Update basic fields
        user_profile.name = name
        user_profile.address = address
        user_profile.contact = contact
        user_profile.save()

        # Update email
        if email and email != login_obj.email:
            login_obj.email = email

        # Password update logic
        if current_password:
            if current_password == login_obj.password:
                if new_password:
                    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
                    if not re.match(password_regex, new_password):
                        profile_message = "New password must be at least 8 characters and include uppercase, lowercase, a number, and a special character."
                        return render(request, 'update_user_profile.html', {
                            'user_profile': user_profile,
                            'login_obj': login_obj,
                            'profile_message': profile_message,
                        })
                    else:
                        login_obj.password = new_password
                        profile_message = "Password updated successfully."
            else:
                profile_message = "Current password is incorrect."
                return render(request, 'update_user_profile.html', {
                    'user_profile': user_profile,
                    'login_obj': login_obj,
                    'profile_message': profile_message,
                })

        login_obj.save()
        profile_message = "Profile updated successfully."
        return render(request, 'update_user_profile.html', {
            'user_profile': user_profile,
            'login_obj': login_obj,
            'profile_message': profile_message,
        })

    return render(request, 'update_user_profile.html', {
        'user_profile': user_profile,
        'login_obj': login_obj,
        'profile_message': profile_message,
    })
def update_company_profile(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('user_login')

    company_profile = get_object_or_404(company_register, login_id=company_id)
    login_obj = company_profile.login
    profile_message = None

    if request.method == 'POST':
        # Get all fields from the form
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        registration_number = request.POST.get('registration_number')
        gst_number = request.POST.get('gst_number')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        # Update company_register fields
        company_profile.company_name = company_name
        company_profile.address = address
        company_profile.contact = contact
        company_profile.registration_number = registration_number
        company_profile.gst_number = gst_number
        company_profile.save()

        # Update email if changed
        if email and email != login_obj.email:
            login_obj.email = email

        # Password update logic (optional)
        if current_password or new_password:
            if not current_password or not new_password:
                profile_message = "To change your password, fill both current and new password fields."
                return render(request, 'update_company_profile.html', {
                    'company_profile': company_profile,
                    'login_obj': login_obj,
                    'profile_message': profile_message,
                })
            if current_password == login_obj.password:
                password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
                if not re.match(password_regex, new_password):
                    profile_message = "New password must be at least 8 characters and include uppercase, lowercase, a number, and a special character."
                    return render(request, 'update_company_profile.html', {
                        'company_profile': company_profile,
                        'login_obj': login_obj,
                        'profile_message': profile_message,
                    })
                login_obj.password = new_password
                profile_message = "Password updated successfully."
            else:
                profile_message = "Current password is incorrect."
                return render(request, 'update_company_profile.html', {
                    'company_profile': company_profile,
                    'login_obj': login_obj,
                    'profile_message': profile_message,
                })

        login_obj.save()
        profile_message = "Company profile updated successfully."
        # Show the message on the same page (do not redirect)
        return render(request, 'update_company_profile.html', {
            'company_profile': company_profile,
            'login_obj': login_obj,
            'profile_message': profile_message,
        })

    return render(request, 'update_company_profile.html', {
        'company_profile': company_profile,
        'login_obj': login_obj,
        'profile_message': profile_message,
    })
def update_contract_profile(request):
    contract_id = request.session.get('contract_id')
    if not contract_id:
        return redirect('contract_login')

    contract_profile = get_object_or_404(contract_register, login_id=contract_id)
    login_obj = contract_profile.login
    profile_message = None

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract_profile)
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if form.is_valid():
            form.save()

            # Update email if changed
            if email and email != login_obj.email:
                login_obj.email = email

            # Password update logic (optional)
            if current_password or new_password:
                if not current_password or not new_password:
                    profile_message = "To change your password, fill both current and new password fields."
                    return render(request, 'update_contract_profile.html', {
                        'form': form,
                        'contract_profile': contract_profile,
                        'login_obj': login_obj,
                        'profile_message': profile_message,
                    })
                if current_password == login_obj.password:
                    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
                    if not re.match(password_regex, new_password):
                        profile_message = "New password must be at least 8 characters and include uppercase, lowercase, a number, and a special character."
                        return render(request, 'update_contract_profile.html', {
                            'form': form,
                            'contract_profile': contract_profile,
                            'login_obj': login_obj,
                            'profile_message': profile_message,
                        })
                    login_obj.password = new_password
                    profile_message = "Password updated successfully."
                else:
                    profile_message = "Current password is incorrect."
                    return render(request, 'update_contract_profile.html', {
                        'form': form,
                        'contract_profile': contract_profile,
                        'login_obj': login_obj,
                        'profile_message': profile_message,
                    })

            login_obj.save()
            profile_message = "Contract profile updated successfully."
            # Show the message on the same page (do not redirect)
            return render(request, 'update_contract_profile.html', {
                'form': form,
                'contract_profile': contract_profile,
                'login_obj': login_obj,
                'profile_message': profile_message,
            })
        else:
            profile_message = "Please correct the errors below."
    else:
        form = ContractForm(instance=contract_profile)

    return render(request, 'update_contract_profile.html', {
        'form': form,
        'contract_profile': contract_profile,
        'login_obj': login_obj,
        'profile_message': profile_message,
    })
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job created successfully.")
            return redirect('create_job')  # Redirect to the same page or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm()

    return render(request, 'create_job.html', {'form': form})
def view_jobs(request):
    jobs = job.objects.all()  # Fetch all jobs from the database
    return render(request, 'view_jobs.html', {'jobs': jobs})  # Render the template with the job list
def edit_job(request, job_id):
    job_instance = get_object_or_404(job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('view_jobs')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm(instance=job_instance)

    return render(request, 'edit_job.html', {'form': form})
def delete_job(request, job_id):
    job_instance = get_object_or_404(job, id=job_id)
    if request.method == 'POST':
        job_instance.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('view_jobs')
    return render(request, 'confirm_delete.html', {'job': job_instance})

def view_jobs_user(request):
    jobs = job.objects.all()  # Fetch all jobs from the database
    return render(request, 'user_view_jobs.html', {'jobs': jobs})
# Example: user_view_jobs view
def user_view_jobs(request):
    user_id = request.session.get('user_id')
    user_instance = get_object_or_404(user_register, login_id=user_id)
    jobs = job.objects.all()
    applied_jobs = job_apply.objects.filter(user=user_instance).values_list('job_id', flat=True)
    return render(request, 'user_view_jobs.html', {
        'jobs': jobs,
        'applied_job_ids': list(applied_jobs),
    })
def user_job_apply(request, job_id):
    job_instance = get_object_or_404(job, id=job_id)
    user_id = request.session.get('user_id')
    user_instance = get_object_or_404(user_register, login_id=user_id)

    already_applied = job_apply.objects.filter(user=user_instance, job_id=job_instance).exists()

    if request.method == 'POST' and not already_applied:
        cv = request.FILES.get('cv')
        if not cv:
            return render(request, 'apply_job.html', {
                'job': job_instance,
                'already_applied': already_applied,
                'success': False,
                'error': "Please upload your CV."
            })
        job_apply.objects.create(
    user=user_instance,
    job_id=job_instance,
    cv=cv,
    login_id=user_instance.login  # or whatever field links to the Login model
)
        # Show success message only for this job
        return render(request, 'apply_job.html', {
            'job': job_instance,
            'already_applied': True,
            'success': True
        })

    return render(request, 'apply_job.html', {
        'job': job_instance,
        'already_applied': already_applied,
        'success': False
    })
def job_applications(request):
    applications = job_apply.objects.all()  # Fetch all job applications
    return render(request, 'job_applications.html', {'applications': applications})
def accept_application(request, application_id):
    application = get_object_or_404(job_apply, id=application_id)
    if request.method == 'POST':
        application.status = 1  # Set status to 'Accepted'
        application.save()
        messages.success(request, "Application accepted successfully.")
    return redirect('job_applications')

def reject_application(request, application_id):
    application = get_object_or_404(job_apply, id=application_id)
    if request.method == 'POST':
        application.status = 2  # Set status to 'Rejected'
        application.save()
        messages.success(request, "Application rejected successfully.")
    return redirect('job_applications')
def job_status(request):
    user_id = request.session.get('user_id')  # Assuming user_id is stored in the session
    if not user_id:
        messages.error(request, "You must be logged in to view your job status.")
        return redirect('user_login')

    # Fetch the logged-in user's applications and prefetch related interviews
    user_instance = get_object_or_404(user_register, login_id=user_id)
    applications = job_apply.objects.filter(user=user_instance).prefetch_related('interview_list')  # Prefetch interviews

    return render(request, 'job_status.html', {
        'applications': applications,
    })
def manage_interviews(request):
    # Fetch all interviews
    interviews = Interview.objects.all()

    return render(request, 'manage_interviews.html', {'interviews': interviews})

def create_interview(request):
    jobs = job.objects.all()
    selected_job_id = request.GET.get('job_id') or request.POST.get('job_id')
    applications = []
    if selected_job_id:
        applications = job_apply.objects.filter(job_id=selected_job_id, status=1)  # Only accepted

    if request.method == 'POST' and 'application_id' in request.POST:
        application_id = request.POST.get('application_id')
        interview_date = request.POST.get('interview_date')
        interview_time = request.POST.get('interview_time')
        description = request.POST.get('description')

        job_application = get_object_or_404(job_apply, id=application_id, status=1)
        Interview.objects.create(
            job_application=job_application,
            interview_date=interview_date,
            interview_time=interview_time,
            description=description,
        )
        messages.success(request, "Interview created successfully.", extra_tags='profile')
        return redirect('manage_interviews')

    return render(request, 'create_interview.html', {
        'jobs': jobs,
        'applications': applications,
        'selected_job_id': selected_job_id,
    })
def videocall_interview(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview_completed = False
    if request.method == 'POST' and request.user.is_staff:
        interview.interview_status = 'Completed'
        interview.save()
        interview_completed = True
    elif interview.interview_status == 'Completed':
        interview_completed = True
    return render(request, 'video_call.html', {'var': interview, 'interview_completed': interview_completed})
    
@csrf_exempt
def complete_interview(request, id):
    interview = get_object_or_404(Interview, id=id)
    if request.method == 'POST':
        interview.interview_status = 'Completed'
        interview.save()
    return redirect('view_interviews')
def view_interviews(request):
    # Fetch all interviews
    interviews = Interview.objects.all()
    return render(request, 'view_interviews.html', {'interviews': interviews})

def interview_details(request, job_id):
    user_id = request.session.get('user_id')  # or use request.user if using Django auth
    if not user_id:
        messages.error(request, "You must be logged in to view your interviews.")
        return redirect('user_login')

    job_instance = get_object_or_404(job, id=job_id)
    user_instance = get_object_or_404(user_register, login_id=user_id)
    # Only interviews for this job and this user
    interviews = Interview.objects.filter(
        job_application__job_id=job_instance,
        job_application__user=user_instance
    )

    return render(request, 'interview_details.html', {
        'job': job_instance,
        'interviews': interviews,
    })
@csrf_exempt
def save_appointment_url(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            if url:
                interview = get_object_or_404(Interview, pk=pk)
                interview.interview_link = url
                interview.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'message': 'No URL provided'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def news_page(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            News.objects.create(content=content)
        return redirect('news_page')

    # Fetch all news to display
    news_list = News.objects.all().order_by('-current_date')
    return render(request, 'news_page.html', {'news_list': news_list})
def news_user_page(request):
    # Fetch all news in descending order of the current date
    news_list = News.objects.all().order_by('-current_date')
    return render(request, 'news_user_page.html', {'news_list': news_list})
def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            news.content = content
            news.save()
            return redirect('news_page')

    return render(request, 'edit_news.html', {'news': news})
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('news_page')
def update_hiring_status(request, application_id):
    # Fetch the job application by ID
    application = get_object_or_404(job_apply, id=application_id)
    # Update the appointment_status to 1 (Hired)
    application.appointment_status = 1  # Ensure this field exists in the model
    application.save()
    return redirect('job_applications')  # Redirect back to the job applications page
def appointment_letter(request, application_id):
    # Fetch the job application by ID
    application = get_object_or_404(job_apply, id=application_id)
    return render(request, 'appointment_letter.html', {'application': application})
def upload_appointment_letter(request, application_id):
    application = get_object_or_404(job_apply, id=application_id)

    if request.method == 'POST':
        if 'appointment_letter' in request.FILES:
            application.appointment_letter = request.FILES['appointment_letter']
            application.save()
            messages.success(request, "Appointment letter uploaded successfully.")
            return redirect('job_applications')
        else:
            messages.error(request, "Please upload a valid file.")

    return render(request, 'upload_appointment_letter.html', {'application': application})

def add_ship(request):
    ship = None
    if request.method == 'POST':
        ship_name = request.POST.get('ship_name')
        ship_category = request.POST.get('ship_category')
        ship_type = request.POST.get('ship_type')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        ship_description = request.POST.get('ship_description')
        ship_details = request.POST.get('ship_details')
        departure_date = request.POST.get('departure_date')
        imo_number = request.POST.get('imo_number')
        mmsi_number = request.POST.get('mmsi_number')
        flag_state = request.POST.get('flag_state')

        company_login = request.session.get('company_id')
        if not company_login:
            messages.error(request, "You must be logged in as a company to add a ship.")
            return redirect('user_login')

        login_instance = Login.objects.get(id=company_login)

        ship = Ship.objects.create(
            login=login_instance,
            ship_name=ship_name,
            ship_category=ship_category,
            ship_type=ship_type,
            source=source,
            destination=destination,
            ship_description=ship_description,
            ship_details=ship_details,
            departure_date=departure_date,
            imo_number=imo_number,
            mmsi_number=mmsi_number,
            flag_state=flag_state
        )
        messages.success(request, 'Ship added successfully!')
        return render(request, 'add_ship.html', {'ship': ship})

    return render(request, 'add_ship.html')
def edit_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)

    if request.method == 'POST':
        ship.ship_name = request.POST.get('ship_name')
        ship.ship_category = request.POST.get('ship_category')
        ship.source = request.POST.get('source')
        ship.destination = request.POST.get('destination')
        ship.ship_description = request.POST.get('ship_description')
        ship.ship_details = request.POST.get('ship_details')
        ship.save()
        messages.success(request, 'Ship updated successfully!')
        return redirect('view_ships')

    return render(request, 'edit_ship.html', {'ship': ship})
def delete_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    ship.delete()
    messages.success(request, 'Ship deleted successfully!')
    return redirect('view_ships')
def view_ships(request):
    company_login = request.session.get('company_id')
    if not company_login:
        return redirect('user_login')  # Redirect to login if not logged in as a company

    ships = Ship.objects.filter(login_id=company_login)
    return render(request, 'view_ships.html', {'ships': ships})
def exporting(request):
    ships = None
    query = request.GET.get('query')
    if query:
        ships = Ship.objects.filter(source__icontains=query) | Ship.objects.filter(destination__icontains=query)
    else:
        ships = Ship.objects.all()

    # Add company name to each ship
    company_map = {c.login.id: c.company_name for c in company_register.objects.all()}
    for ship in ships:
        ship.company_name = company_map.get(ship.login_id, '')

    exports = Export.objects.none()
    if request.session.get('user_id'):
        user_login = request.session['user_id']
        exports = Export.objects.filter(user_login_id=user_login)

    return render(request, 'exporting.html', {'ships': ships, 'exports': exports, 'query': query})


def add_export(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    user_login = get_object_or_404(Login, id=request.session.get('user_id'))
    companies = company_register.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        company_name = request.POST.get('company_name')
        product_description = request.POST.get('product_description')
        quantity = request.POST.get('quantity')
        recipient_name = request.POST.get('recipient_name')
        recipient_address = request.POST.get('recipient_address')
        recipient_contact_number = request.POST.get('recipient_contact_number')
        destination = request.POST.get('destination')

        # Validate quantity
        try:
            quantity_int = int(quantity)
            if quantity_int <= 0:
                messages.error(request, "Quantity must be a positive number.")
                return render(request, 'add_export.html', {'ship': ship, 'companies': companies})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid quantity.")
            return render(request, 'add_export.html', {'ship': ship, 'companies': companies})

        export = Export.objects.create(
            user_login=user_login,
            ship=ship,
            product_name=product_name,
            company_name=company_name,
            product_description=product_description,
            quantity=quantity_int,
            recipient_name=recipient_name,
            recipient_address=recipient_address,
            recipient_contact_number=recipient_contact_number,
            destination=destination,
            # export_uid will be auto-generated
        )
        messages.success(request, f'Export added successfully! Export ID: {export.export_uid}')
        return redirect('my_exports')  # or wherever you want to show the export

    return render(request, 'add_export.html', {'ship': ship, 'companies': companies})
def view_exports(request):
    if 'user_id' in request.session:  # Check if the logged-in user is a user
        user_login = request.session.get('user_id')
        exports = Export.objects.filter(user_login_id=user_login)  # Filter exports for the logged-in user
    elif 'company_id' in request.session:  # Check if the logged-in user is a company
        company_login = request.session.get('company_id')
        exports = Export.objects.filter(ship__login_id=company_login)  # Filter exports for the logged-in company
    else:
        messages.error(request, "You must be logged in to view exports.")
        return redirect('user_login')

    return render(request, 'view_exports.html', {'exports': exports})
def edit_export(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    companies = company_register.objects.all()
    if request.method == 'POST':
        export.product_name = request.POST.get('product_name')
        export.company_name = request.POST.get('company_name')
        export.product_description = request.POST.get('product_description')
        export.quantity = request.POST.get('quantity')
        export.recipient_name = request.POST.get('recipient_name')
        export.recipient_address = request.POST.get('recipient_address')
        export.recipient_contact_number = request.POST.get('recipient_contact_number')
        export.destination = request.POST.get('destination')
        export.save()
        messages.success(request, 'Export updated successfully!')
        return redirect('exporting')
    return render(request, 'edit_export.html', {'export': export, 'companies': companies})
def cancel_export(request, export_id):
    user_login = request.session.get('user_id')
    if not user_login:
        messages.error(request, "You must be logged in to cancel export details.")
        return redirect('user_login')

    export = get_object_or_404(Export, id=export_id, user_login_id=user_login)
    export.cancel_status = 1
    export.save()
    messages.success(request, 'Export canceled successfully!')
    # return redirect('view_exports')
def view_export_details(request, export_id):
    if 'user_id' in request.session:
        export = get_object_or_404(Export, id=export_id, user_login_id=request.session.get('user_id'))
    elif 'company_id' in request.session:
        export = get_object_or_404(Export, id=export_id, ship__login_id=request.session.get('company_id'))
    else:
        messages.error(request, "You must be logged in to view export details.")
        return redirect('user_login')

    return render(request, 'view_export_details.html', {'export': export})
def complaints(request, export_id):
    export = Export.objects.get(id=export_id)
    user_id = request.session.get('user_id')  # Use 'user_id' from session
    if not user_id:
        return redirect('user_login')
    user = Login.objects.get(id=user_id)

    user_complaints = Complaint.objects.filter(user=user)
    if request.method == 'POST':
        complaint_text = request.POST.get('complaint_text')
        if complaint_text:
            Complaint.objects.create(
                export=export,
                user=user,
                complaint_text=complaint_text
            )
            # Optionally redirect after POST

    return render(request, 'complaints.html', {
        'export': export,
        'user_complaints': user_complaints
    })
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user_id=request.session.get('user_id'))
    if request.method == 'POST':
        complaint.complaint_text = request.POST.get('complaint_text')
        complaint.save()
        messages.success(request, "Complaint updated successfully.")
        return redirect('complaints', complaint.export.id)  
    return render(request, 'edit_complaint.html', {'complaint': complaint})
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user_id=request.session.get('user_id'))
    complaint.delete()
    messages.success(request, "Complaint deleted successfully.")
    return redirect('complaints')
# For company/admin to view all complaints:
def admin_view_all_complaints(request):
    if request.session.get('user_type') != 'admin':
        messages.error(request, "Unauthorized access.")
        return redirect('user_login')
    complaints = Complaint.objects.all()
    return render(request, 'view_all_complaints.html', {'complaints': complaints})
def company_view_complaints(request):
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, "Unauthorized access.")
        return redirect('user_login')
    company_exports = Export.objects.filter(ship__login_id=company_id)
    complaints = Complaint.objects.filter(export__in=company_exports)
    return render(request, 'view_complaints1.html', {'complaints': complaints})

from django.db.models import Max, Subquery, OuterRef

def add_notification(request):
    companies = company_register.objects.all()

    if request.method == 'POST':
        recipient_type = request.POST.get('recipient_type')
        message = request.POST.get('message')

        if recipient_type == 'user' and message:
            all_users = Login.objects.filter(user_type='user')
            for user in all_users:
                Notification.objects.create(user=user, message=message)
            messages.success(request, "Notification sent to all users.")
        elif recipient_type == 'company' and message:
            company_id = request.POST.get('company_id')
            if company_id:
                company = company_register.objects.get(id=company_id)
                CompanyNotification.objects.create(company=company, message=message)
                messages.success(request, f"Notification sent to {company.company_name}.")
            else:
                messages.error(request, "Please select a company.")
        else:
            messages.error(request, "Please select recipient and enter a message.")
        return redirect('add_notification')

    # Grouped user notifications: one per unique message, with latest id and created_at
    latest_notifications = Notification.objects.filter(
        message=OuterRef('message')
    ).order_by('-created_at')

    notifications = (
        Notification.objects
        .values('message')
        .annotate(
            latest=Max('created_at'),
            latest_id=Subquery(latest_notifications.values('id')[:1]),
            latest_created_at=Subquery(latest_notifications.values('created_at')[:1])
        )
        .order_by('-latest')
    )

    company_notifications = CompanyNotification.objects.all().order_by('-created_at')

    return render(request, 'add_notification.html', {
        'notifications': notifications,
        'company_notifications': company_notifications,
        'companies': companies
    })
def edit_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            notification.message = message
            notification.save()
            messages.success(request, "Notification updated.")
            return redirect('add_notification')
    return render(request, 'edit_notification.html', {'notification': notification})
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    messages.success(request, "Notification deleted.")
    return redirect('add_notification')
def user_notifications(request):
    user_id = request.session.get('user_id')
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    return render(request, 'user_notifications.html', {'notifications': notifications})
def add_tender(request):
    # if not request.session.get('user_type') == 'admin':
    #     messages.error(request, "Only admin can add tenders.")
    #     return redirect('admin')
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tender created successfully.")
            return redirect('add_tender')
    else:
        form = TenderForm()
    return render(request, 'add_tender.html', {'form': form})
def view_tenders(request):
    contract_id = request.session.get('contract_id')
    tenders = Tender.objects.all()
    for tender in tenders:
        app = TenderApplication.objects.filter(tender=tender, contract_login_id=contract_id).first()
        tender.user_status = app.status if app else None
        tender.contract_agreement = app.contract_agreement if (app and app.contract_agreement) else None
    return render(request, 'view_tenders.html', {'tenders': tenders})

def track_location(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    locations = Location.objects.filter(ship=ship).order_by('-current_date', '-current_time')
    return render(request, 'track_location.html', {'ship': ship, 'locations': locations})

def export_product_list(request):
    company_id = request.session.get('company_id')
    products = ExportProduct.objects.filter(login_id=company_id)
    return render(request, 'export_product_list.html', {'products': products})

def add_export_product(request):
    if request.method == 'POST':
        product_category = request.POST.get('product_category')
        product_name = request.POST.get('product_name')
        amount = request.POST.get('amount')
        tax = request.POST.get('tax')
        login = Login.objects.get(id=request.session.get('company_id'))
        ExportProduct.objects.create(
            login=login,
            product_category=product_category,
            product_name=product_name,
            amount=amount,
            tax=tax
        )
        return redirect('export_product_list')
    return render(request, 'add_export_product.html')
def edit_export_product(request, product_id):
    product = get_object_or_404(ExportProduct, id=product_id)
    if request.method == 'POST':
        product.product_category = request.POST.get('product_category')
        product.product_name = request.POST.get('product_name')
        product.amount = request.POST.get('amount')
        product.tax = request.POST.get('tax')
        product.save()
        return redirect('export_product_list')
    return render(request, 'edit_export_product.html', {'product': product})

def delete_export_product(request, product_id):
    product = get_object_or_404(ExportProduct, id=product_id)
    product.delete()
    return redirect('export_product_list')
def user_export_products(request):
    query = request.GET.get('query', '')
    products = ExportProduct.objects.all()
    company_map = {c.login.id: c.company_name for c in company_register.objects.all()}
    for p in products:
        p.company_name = company_map.get(p.login_id, '')

    if query:
        products = [
            p for p in products
            if query.lower() in p.product_name.lower()
            or query.lower() in p.product_category.lower()
            or query.lower() in (p.company_name or '').lower()
        ]

    return render(request, 'user_export_products.html', {'products': products, 'query': query})

from .models import Ship, ShipLocation

def update_location(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    if request.method == 'POST':
        location = request.POST.get('location')
        # Get the company login from the ship
        company_login = ship.login
        ShipLocation.objects.create(
            ship=ship,
            location=location,
            company_login=company_login,  # <-- Add this line
            # Optionally add current_date/current_time if your model has them
        )
        return redirect('view_ships')
    return render(request, 'update_location.html', {'ship': ship})
def add_user_export_product(request, product_id):
    product = get_object_or_404(ExportProduct, id=product_id)
    if request.method == 'POST':
        number_of_product = int(request.POST.get('number_of_product'))
        amount = float(product.amount)
        tax = float(product.tax)
        total_amount = (amount * number_of_product) + tax

        # Pass all needed info to payment.html
        context = {
            'product_name': product.product_name,
            'product_category': product.product_category,
            'amount': amount,
            'tax': tax,
            'number_of_product': number_of_product,
            'total_amount': total_amount,
        }
        return render(request, 'payment.html', context)
    return render(request, 'add_user_export_product.html', {'product': product})


def update_ship_space(request, ship_id):
    if request.method == 'POST':
        ship = get_object_or_404(Ship, id=ship_id)
        space_value = request.POST.get('space')
        if space_value in ['available', 'not_available']:
            ship.space = space_value
            ship.save()
    return redirect('view_ships')

def add_export(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    companies = company_register.objects.all()
    company_obj = company_register.objects.filter(login=ship.login).first()
    selected_company_name = company_obj.company_name if company_obj else ''

    # Get export products for this user/company
    products = ExportProduct.objects.filter(login=ship.login)
    product_categories = products.values_list('product_category', flat=True).distinct()
    product_names_by_category = {}
    product_info = {}
    for category in product_categories:
        names = list(products.filter(product_category=category).values_list('product_name', flat=True).distinct())
        product_names_by_category[category] = names
        for name in names:
            prod = products.filter(product_category=category, product_name=name).first()
            if prod:
                product_info[name] = {
                    'amount': prod.amount,
                    'tax': prod.tax,
                }

    # Get user_id and company_id from session and models
    user_id = request.session.get('user_id')
    company_id = ship.login.id  # ship.login is a Login instance

    user_instance = None
    company_instance = None
    if user_id:
        user_instance = user_register.objects.filter(login_id=user_id).first()
    if company_id:
        company_instance = company_register.objects.filter(login_id=company_id).first()

    if request.method == 'POST':
        selected_product = ExportProduct.objects.filter(
            login=ship.login,
            product_category=request.POST.get('product_category'),
            product_name=request.POST.get('product_name')
        ).first()
        exporting_price = selected_product.amount if selected_product else 0
        tax = selected_product.tax if selected_product else 0

        export = Export.objects.create(
    user_login=user_instance.login if user_instance else None,
    ship=ship,
    product_category=request.POST.get('product_category'),
    product_name=request.POST.get('product_name'),
    company_name=request.POST.get('company_name'),
    exporting_price=exporting_price,
    tax=tax,
    product_description=request.POST.get('product_description'),
    quantity=request.POST.get('quantity'),
    recipient_name=request.POST.get('recipient_name'),
    recipient_address=request.POST.get('recipient_address'),
    recipient_contact_number=request.POST.get('recipient_contact_number'),
    source=request.POST.get('source'),
    destination=request.POST.get('destination'),
)
        return redirect('view_export_details', export_id=export.id)

    return render(request, 'add_export.html', {
        'companies': companies,
        'selected_company_name': selected_company_name,
        'product_categories': product_categories,
        'product_names_by_category': product_names_by_category,
        'product_info': product_info,
        'ship': ship,
    })

def view_export_details(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    try:
        exporting_price = float(export.exporting_price)
        quantity = int(export.quantity)
        tax = float(export.tax)
        total_price = (exporting_price * quantity) + tax
    except Exception as e:
        total_price = 0
    return render(request, 'view_export_details.html', {
        'export': export,
        'total_price': total_price,
    })

def make_payment(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    try:
        total_price = float(export.exporting_price) * int(export.quantity) + float(export.tax)
    except Exception:
        total_price = 0

    if request.method == 'POST':
        Payment.objects.create(
            export=export,
            login=export.user_login,
            card_holder=request.POST.get('card_holder'),
            card_number=request.POST.get('card_number'),
            expiry_date=request.POST.get('expiry_date'),
            cvv=request.POST.get('cvv'),
            amount=total_price,
        )
        # Set payment status to 1 (Paid)
        export.payment_status = 1
        export.save()
        return redirect('payment_success')

    return render(request, 'make_payment.html', {
        'export': export,
        'total_price': total_price,
    })

def payment_success(request):
    return render(request, 'payment_success.html')

def company_exports(request):
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, "You must be logged in as a company to view exports.")
        return redirect('user_login')

    company_obj = company_register.objects.filter(login_id=company_id).first()
    company_name = company_obj.company_name if company_obj else ''

    exports = Export.objects.filter(company_name=company_name)

    return render(request, 'company_exports.html', {
        'exports': exports,
        'company_name': company_name,
    })

def my_exports(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view your exports.")
        return redirect('user_login')
    exports = Export.objects.filter(user_login_id=user_id, payment_status=1)
    return render(request, 'my_exports.html', {'exports': exports})
def replay_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        replay_text = request.POST.get('replay_text')
        if replay_text:
            complaint.replay_text = replay_text
            complaint.save()
            return redirect('company_view_complaints')
    return render(request, 'replay_complaint.html', {'complaint': complaint})

def add_product_status(request, ship_id, export_id):
    ship = get_object_or_404(Ship, id=ship_id)
    export = get_object_or_404(Export, id=export_id)
    company_login = ship.login  # Assuming ship.login is the company Login

    # Get the latest status for this ship and export
    latest_status = ProductStatus.objects.filter(ship=ship, export=export).order_by('-current_date', '-current_time').first()

    if request.method == 'POST':
        booking_confirmed = bool(request.POST.get('booking_confirmed'))
        customs_cleared = bool(request.POST.get('customs_cleared'))
        loaded_on_vessel = bool(request.POST.get('loaded_on_vessel'))
        in_transit = bool(request.POST.get('in_transit'))
        arrived_at_port = bool(request.POST.get('arrived_at_port'))
        delivered = bool(request.POST.get('delivered'))

        if latest_status:
            # Update the latest status
            latest_status.booking_confirmed = booking_confirmed
            latest_status.customs_cleared = customs_cleared
            latest_status.loaded_on_vessel = loaded_on_vessel
            latest_status.in_transit = in_transit
            latest_status.arrived_at_port = arrived_at_port
            latest_status.delivered = delivered
            latest_status.save()
        else:
            # Create a new status if none exists
            ProductStatus.objects.create(
                company_login=company_login,
                ship=ship,
                export=export,
                booking_confirmed=booking_confirmed,
                customs_cleared=customs_cleared,
                loaded_on_vessel=loaded_on_vessel,
                in_transit=in_transit,
                arrived_at_port=arrived_at_port,
                delivered=delivered
            )
        return redirect('company_exports')

    # For GET, pre-fill the form with the latest status if it exists
    context = {
        'ship': ship,
        'export': export,
        'latest_status': latest_status
    }
    return render(request, 'add_product_status.html', context)
def view_product_status(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    status_updates = ProductStatus.objects.filter(export=export).order_by('-current_date', '-current_time')

    for status in status_updates:
        status.step_statuses = [
            {'label': 'Booking Confirmed', 'value': status.booking_confirmed},
            {'label': 'Customs Cleared', 'value': status.customs_cleared},
            {'label': 'Loaded on Vessel', 'value': status.loaded_on_vessel},
            {'label': 'In Transit', 'value': status.in_transit},
            {'label': 'Arrived at Port', 'value': status.arrived_at_port},
            {'label': 'Delivered', 'value': status.delivered},
        ]

    latest_status = status_updates.first()
    ship = latest_status.ship if latest_status else None

    # ✅ Get the latest ship location
    latest_location = ShipLocation.objects.filter(ship=ship).order_by('-current_date').first() if ship else None

    return render(request, 'view_product_status.html', {
        'export': export,
        'status_updates': status_updates,
        'latest_status': latest_status,
        'latest_location': latest_location,
    })

def cancel_export(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    export.cancel_status = 1
    export.save()
    return redirect('my_exports')
def refund_export(request, export_id):
    export = get_object_or_404(Export, id=export_id)
    export.refund_status = 1
    export.save()
    return redirect('company_exports')
def user_logout(request):
    # Get any possible login session key
    user_id = request.session.get('user_id') or request.session.get('company_id') or request.session.get('contract_id')
    if user_id:
        try:
            user = Login.objects.get(id=user_id)
            user.status = 0  # Mark user as logged out/inactive
            user.save()
        except Login.DoesNotExist:
            pass
    request.session.flush()  # Clear all session data
    return redirect('user_login')  # Redirect to login page
def chat_view(request, receiver_id):
    sender_id = request.session.get('user_id') or request.session.get('company_id')
    if not sender_id:
        return redirect('user')

    sender = get_object_or_404(Login, id=sender_id)
    receiver = get_object_or_404(Login, id=receiver_id)

    messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
    ).order_by('current_date', 'current_time')

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Chat.objects.create(sender=sender, receiver=receiver, message=message_text)
            return redirect('chat', receiver_id=receiver.id)

    return render(request, 'chat.html', {
        'receiver': receiver,
        'sender': sender,
        'messages': messages,
        'current_user': sender,
    })

def company_chat_view(request, receiver_id):
    sender_id = request.session.get('user_id') or request.session.get('company_id')
    if not sender_id:
        return redirect('company')

    sender = get_object_or_404(Login, id=sender_id)
    receiver = get_object_or_404(Login, id=receiver_id)

    # Fetch chat messages between company and user
    messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
    ).order_by('current_date', 'current_time')

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Chat.objects.create(
                sender=sender,
                receiver=receiver,
                message=msg
            )
            return redirect('chat1', receiver_id=receiver.id)

    return render(request, 'chat1.html', {
        'receiver': receiver,
        'sender': sender,
        'messages': messages,
        'current_user': sender,
    })

def company_inbox(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('user_login')
    company = get_object_or_404(Login, id=company_id)
    # Get all unique user IDs who have chatted with the company
    user_ids_1 = Chat.objects.filter(receiver=company).values_list('sender', flat=True)
    user_ids_2 = Chat.objects.filter(sender=company).values_list('receiver', flat=True)
    user_ids = set(user_ids_1) | set(user_ids_2)
    users = Login.objects.filter(id__in=user_ids, user_type='user')
    # Get the last message and user name for each user
    last_messages = []
    for user in users:
        user_profile = user_register.objects.filter(login=user).first()
        last_msg = Chat.objects.filter(
            Q(sender=company, receiver=user) | Q(sender=user, receiver=company)
        ).order_by('-current_date', '-current_time').first()
        last_messages.append({'user': user, 'user_profile': user_profile, 'last_msg': last_msg})
    return render(request, 'company_inbox.html', {'last_messages': last_messages, 'company': company})
def apply_tender(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    contract_id = request.session.get('contract_id')
    contract = get_object_or_404(Login, id=contract_id)
    error = None

    if request.method == 'POST':
        try:
            applied_amount = float(request.POST.get('applied_amount'))
        except (TypeError, ValueError):
            applied_amount = None
        if applied_amount is None or applied_amount >= float(tender.amount):
            error = f"Tender amount must be less than the admin amount ({tender.amount})."
        else:
            TenderApplication.objects.create(
                tender=tender,
                contract_login=contract,
                applied_amount=applied_amount
            )
            return redirect('view_tenders')

    return render(request, 'apply_tender.html', {'tender': tender, 'error': error})
def view_all_tender_applications(request):
    applications = TenderApplication.objects.select_related('tender', 'contract_login').all().order_by('applied_amount')

    # Handle agreement upload
    if request.method == 'POST' and 'upload_agreement' in request.POST:
        app_id = request.POST.get('upload_agreement')
        app = get_object_or_404(TenderApplication, id=app_id)
        file_field = f'agreement_{app_id}'
        if file_field in request.FILES:
            app.contract_agreement = request.FILES[file_field]
            app.save()
        return redirect('view_all_tender_applications')

    # Handle approve action
    if request.method == 'POST' and 'approve_app' in request.POST:
        app_id = request.POST.get('approve_app')
        app = get_object_or_404(TenderApplication, id=app_id)
        app.status = 1  # Approved
        app.save()
        return redirect('view_all_tender_applications')

    return render(request, 'view_all_tender_applications.html', {'applications': applications})
def approve_tender_application(request, app_id):
    application = get_object_or_404(TenderApplication, id=app_id)
    application.status = 1  # Approved
    application.save()
    Alerts.objects.create(
        contract=application.contract_login,
        message=f"Your application for {application.tender.category} has been approved!",
        type="approval"
    )
    return redirect('view_all_tender_applications')

def reject_tender_application(request, app_id):
    app = get_object_or_404(TenderApplication, id=app_id)
    app.status = 2  # Rejected
    app.save()
    return redirect('view_all_tender_applications')
def user_help(request):
    return render(request, 'user_help.html')
def about_contractor(request):
    return render(request, 'about_contractor.html')
def upload_agreement(request, app_id):
    app = get_object_or_404(TenderApplication, id=app_id)

    # Ensure only approved applications can upload agreements
    if app.status != 1:
        return redirect('view_all_tender_applications')

    if request.method == 'POST':
        form = AgreementUploadForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('view_all_tender_applications')
    else:
        form = AgreementUploadForm(instance=app)

    return render(request, 'upload_agreement.html', {'form': form, 'app': app})
def work_status(request, app_id):
    contract_id = request.session.get('contract_id')
    if not contract_id:
        messages.error(request, "You must be logged in as a contractor to upload work status.")
        return redirect('user_login')

    app = get_object_or_404(TenderApplication, id=app_id, contract_login_id=contract_id)
    reports = WorkStatusReport.objects.filter(tender_application=app).order_by('-created_at')

    if request.method == 'POST':
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        if file:
            WorkStatusReport.objects.create(
                contract=app.contract_login,
                tender_application=app,
                description=description,
                file=file
            )
            messages.success(request, "Work status uploaded successfully.")
            return redirect('work_status', app_id=app_id)
        else:
            messages.error(request, "Please select a file to upload.")

    return render(request, 'work_status.html', {'app': app, 'reports': reports})

def view_my_applications(request):
    contract_id = request.session.get('contract_id')
    if not contract_id:
        messages.error(request, "You must be logged in as a contractor to view applications.")
        return redirect('user_login')

    applications = TenderApplication.objects.filter(contract_login_id=contract_id).order_by('-applied_date')
    return render(request, 'view_my_applications.html', {'applications': applications})
def admin_work_status_reports(request):
    if request.session.get('user_type') != 'admin':
        messages.error(request, "Only admin can view work status reports.")
        return redirect('user_login')

    reports = WorkStatusReport.objects.all().order_by('-created_at')
    return render(request, 'admin_work_status_reports.html', {'reports': reports})
def tender_alerts(request):
    contract_id = request.session.get('contract_id')
    if not contract_id:
        return redirect('user_login')
    alerts = Alerts.objects.filter(contract_id=contract_id).order_by('-created_at')
    return render(request, 'tender_alerts.html', {'alerts': alerts})
def notify_tender_deadlines():
    soon = timezone.now() + timedelta(days=2)
    tenders = Tender.objects.filter(deadline__lte=soon, deadline__gte=timezone.now())
    for tender in tenders:
        for application in tender.tenderapplication_set.all():
            Alerts.objects.create(
                contract=application.contract_login,
                message=f"Tender '{tender.category}' deadline is approaching!",
                type="deadline"
            )
def notify_document_expiry():
    soon = timezone.now() + timedelta(days=7)
    expiring_docs = Document.objects.filter(expiry_date__lte=soon, expiry_date__gte=timezone.now())
    for doc in expiring_docs:
        Alerts.objects.create(
            contract=doc.contractor,
            message=f"Your document {doc.name} is about to expire. Please update it.",
            type="expiry"
        )


def imported_items(request):
    # Fetch all companies and their related ships
    companies = company_register.objects.all()
    company_ships = []
    for company in companies:
        ships = Ship.objects.filter(login=company.login, ship_type='Import')
        if ships.exists():
            company_ships.append({
                'company': company,
                'ships': ships
            })
    return render(request, 'imported_items.html', {'company_ships': company_ships})

def add_items(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            imp = form.save(commit=False)
            imp.ship = ship
            imp.save()
            return redirect('add_items', ship_id=ship.id)
    else:
        form = ImportForm()
    imports = Import.objects.filter(ship=ship)
    return render(request, 'add_items.html', {'ship': ship, 'form': form, 'imports': imports})

def my_company_ships(request):
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, "You must be logged in as a company to view your ships.")
        return redirect('user_login')
    company = get_object_or_404(company_register, login_id=company_id)
    ships = Ship.objects.filter(login=company.login, ship_type__iexact='import')
    return render(request, 'company_ships.html', {'company': company, 'ships': ships})

def view_imported_items(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    imported_items = Import.objects.filter(ship=ship)
    return render(request, 'view_imported_items.html', {'ship': ship, 'imported_items': imported_items})

def company_notifications(request):
    company_id = request.session.get('company_id')
    company = get_object_or_404(company_register, login_id=company_id)
    notifications = CompanyNotification.objects.filter(company=company).order_by('-created_at')
    return render(request, 'company_notifications.html', {'notifications': notifications})
def edit_company_notification(request, notification_id):
    notification = get_object_or_404(CompanyNotification, id=notification_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            notification.message = message
            notification.save()
            messages.success(request, "Company notification updated.")
            return redirect('add_notification')
        else:
            messages.error(request, "Message cannot be empty.")
    return render(request, 'edit_company_notification.html', {'notification': notification})
def delete_company_notification(request, notification_id):
    notification = get_object_or_404(CompanyNotification, id=notification_id)
    notification.delete()
    messages.success(request, "Company notification deleted.")
    return redirect('add_notification')

def request_release(request, ship_id):
    company_id = request.session.get('company_id')
    if not company_id:
        # Handle missing session (redirect or error)
        return redirect('user_login')  # Use your login view name

    ship = get_object_or_404(Ship, id=ship_id)
    company = get_object_or_404(company_register, login_id=company_id)
    imported_items = Import.objects.filter(ship=ship)
    admin_company = get_object_or_404(company_register, company_name="Admin")
    if request.method == 'POST':
        items_list = ", ".join([f"{item.item_name} (qty: {item.quantity})" for item in imported_items])
        message = f"Release requested by {company.company_name} for ship '{ship.ship_name}'. Items: {items_list}"
        CompanyNotification.objects.create(
            company=admin_company,
            message=message
        )
        return redirect('view_imported_items', ship_id=ship.id)
    return redirect('view_imported_items', ship_id=ship.id)

def request_release_view(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Import, id=item_id)
        if item.release_status != 'pending':
            item.release_status = 'pending'
            item.save()
            messages.success(request, f"Release request sent for item: {item.item_name}")
        else:
            messages.warning(request, f"Release request already pending.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def import_requests(request):
    # Fetch all Import items where release_status is not empty
    items = Import.objects.exclude(release_status='').order_by('-added_at')
    # Attach company_name for each item (via ship.login -> company_register)
    company_map = {c.login.id: c.company_name for c in company_register.objects.all()}
    for item in items:
        ship_login_id = item.ship.login.id if item.ship and item.ship.login else None
        item.company_name = company_map.get(ship_login_id, '')
    return render(request, 'import_requests.html', {'items': items})

def request_documents(request, import_id):
    if request.method == 'POST':
        import_item = get_object_or_404(Import, id=import_id)
        import_item.release_status = 'request_documents'
        import_item.save()
        return redirect('import_requests')  # or your current page
    return redirect('import_requests')

def upload_documents(request):
    # Get the logged-in company's ID from session
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('user_login')
    company = get_object_or_404(company_register, login_id=company_id)
    # Get all import items for this company where release_status is 'request_documents'
    items = Import.objects.filter(
        ship__login=company.login,
        release_status='request_documents'
    ).order_by('-added_at')
    return render(request, 'upload_documents.html', {'items': items})

def upload_item_documents(request, import_id):
    import_item = get_object_or_404(Import, id=import_id)
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.import_item = import_item
            doc.save()
            # Change release_status to 'documents_submitted'
            import_item.release_status = 'documents_submitted'
            import_item.save()
            messages.success(request, "Documents uploaded successfully.")
            return redirect('upload_documents')
    else:
        form = DocumentsForm()
    return render(request, 'upload_item_documents.html', {'import_item': import_item, 'form': form})

def view_uploaded_documents(request):
    # Fetch all Import items with release_status 'documents_submitted'
    items = Import.objects.filter(release_status='documents_submitted').order_by('-added_at')
    return render(request, 'view_uploaded_documents.html', {'items': items})

def accept_import(request, import_id):
    if request.method == 'POST':
        import_item = get_object_or_404(Import, id=import_id)
        import_item.release_status = 'accepted'
        import_item.save()
    return redirect('view_uploaded_documents')

def reject_import(request, import_id):
    if request.method == 'POST':
        import_item = get_object_or_404(Import, id=import_id)
        import_item.release_status = 'rejected'
        import_item.save()
    return redirect('view_uploaded_documents')

def accept_import(request, import_id):
    if request.method == 'POST':
        import_item = get_object_or_404(Import, id=import_id)
        import_item.release_status = 'accepted'
        # Generate a unique gate pass (you can customize the format)
        import_item.gate_pass = f"GP-{uuid.uuid4().hex[:8].upper()}"
        import_item.save()
    return redirect('view_uploaded_documents')

def gatepasses(request):
    items = Import.objects.exclude(gate_pass__isnull=True).exclude(gate_pass__exact='').order_by('-added_at')
    return render(request, 'gatepasses.html', {'items': items})
def home(request):
    return render(request, 'home.html')




from django.shortcuts import render
from django.db.models import Sum
from .models import Export
import calendar

def export_summary_view(request):
    # Group by year
    yearly_data = Export.objects.values('year').annotate(
        total_tax=Sum('tax'),
        total_amount=Sum('exporting_price')
    ).order_by('year')

    yearly_labels = [str(d['year']) for d in yearly_data]
    yearly_tax = [float(d['total_tax'] or 0) for d in yearly_data]
    yearly_amount = [float(d['total_amount'] or 0) for d in yearly_data]

    # Group by year + month
    monthly_data = Export.objects.values('year', 'month').annotate(
        total_tax=Sum('tax'),
        total_amount=Sum('exporting_price')
    ).order_by('year', 'month')

    monthly_labels = [f"{calendar.month_abbr[d['month']]} {d['year']}" for d in monthly_data]
    monthly_tax = [float(d['total_tax'] or 0) for d in monthly_data]
    monthly_amount = [float(d['total_amount'] or 0) for d in monthly_data]

    return render(request, 'export_chart.html', {
        'yearly_labels': yearly_labels,
        'yearly_tax': yearly_tax,
        'yearly_amount': yearly_amount,
        'monthly_labels': monthly_labels,
        'monthly_tax': monthly_tax,
        'monthly_amount': monthly_amount,
    })
def company_export_summary_view(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('user_login')  # Or show an error

    # Filter exports for this company
    company_exports = Export.objects.filter(ship__login_id=company_id)

    # Yearly summary
    yearly_data = company_exports.values('year').annotate(
        total_tax=Sum('tax'),
        total_amount=Sum('exporting_price')
    ).order_by('year')

    yearly_labels = [str(d['year']) for d in yearly_data]
    yearly_tax = [float(d['total_tax'] or 0) for d in yearly_data]
    yearly_amount = [float(d['total_amount'] or 0) for d in yearly_data]

    # Monthly summary
    monthly_data = company_exports.values('year', 'month').annotate(
        total_tax=Sum('tax'),
        total_amount=Sum('exporting_price')
    ).order_by('year', 'month')

    monthly_labels = [f"{calendar.month_abbr[d['month']]} {d['year']}" for d in monthly_data]
    monthly_tax = [float(d['total_tax'] or 0) for d in monthly_data]
    monthly_amount = [float(d['total_amount'] or 0) for d in monthly_data]

    return render(request, 'company_export_chart.html', {
        'yearly_labels': yearly_labels,
        'yearly_tax': yearly_tax,
        'yearly_amount': yearly_amount,
        'monthly_labels': monthly_labels,
        'monthly_tax': monthly_tax,
        'monthly_amount': monthly_amount,
    })


from django.db.models.functions import TruncMonth, ExtractYear
from django.db.models import Count
from datetime import date

def chart_data(request):
    # Monthly data
    import_monthly = Import.objects.filter(import_date__isnull=False).annotate(
        month_annotated=TruncMonth('import_date')
    ).values('month_annotated').annotate(count=Count('id')).order_by('month_annotated')
    import_monthly = [
        {
            'month_annotated': d['month_annotated'] if d['month_annotated'] else None,
            'count': d['count']
        }
        for d in import_monthly if d['month_annotated']
    ]

    export_monthly = Export.objects.values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')
    export_monthly = [
        {
            'month_annotated': date(d['year'], d['month'], 1),
            'count': d['count']
        }
        for d in export_monthly
    ]

    # Yearly data
    import_yearly = Import.objects.filter(import_date__isnull=False).annotate(
        year_annotated=ExtractYear('import_date')
    ).values('year_annotated').annotate(count=Count('id')).order_by('year_annotated')
    export_yearly = Export.objects.values('year').annotate(count=Count('id')).order_by('year')

    # Prepare monthly labels and data
    months = sorted(set([d['month_annotated'] for d in import_monthly] + [d['month_annotated'] for d in export_monthly]))
    monthly_labels = [m.strftime('%b %Y') for m in months]
    monthly_imports = [next((d['count'] for d in import_monthly if d['month_annotated'] == m), 0) for m in months]
    monthly_exports = [next((d['count'] for d in export_monthly if d['month_annotated'] == m), 0) for m in months]

    # Prepare yearly labels and data
    years = sorted(set([d['year_annotated'] for d in import_yearly] + [d['year'] for d in export_yearly]))
    yearly_labels = [str(y) for y in years]
    yearly_imports = [next((d['count'] for d in import_yearly if d['year_annotated'] == y), 0) for y in years]
    yearly_exports = [next((d['count'] for d in export_yearly if d['year'] == y), 0) for y in years]

    return JsonResponse({
        'monthly_labels': monthly_labels,
        'monthly_imports': monthly_imports,
        'monthly_exports': monthly_exports,
        'yearly_labels': yearly_labels,
        'yearly_imports': yearly_imports,
        'yearly_exports': yearly_exports,
    })
def import_export_graph(request):
    return render(request, 'import_export_graph.html')