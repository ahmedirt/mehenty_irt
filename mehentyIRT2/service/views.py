from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
import csv
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from .forms import CSVUploadForm
from .models import Customer
from django.contrib.auth.models import User
from django.conf import settings
import csv
import os
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Customer

def import_customers(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={'first_name': row['first_name'], 'last_name': row['last_name'], 'email': row['email']}
                    )
                    customer, created = Customer.objects.get_or_create(
                        user=user,
                        defaults={
                            'address': row['address'],
                            'mobile': row['mobile']
                        }
                    )
                    if 'profile_pic' in row and row['profile_pic']:
                        profile_pic_path = os.path.join(settings.BASE_DIR, 'media', row['profile_pic'].strip('/'))
                        if os.path.exists(profile_pic_path):
                            with open(profile_pic_path, 'rb') as f:
                                file_name = os.path.basename(profile_pic_path)
                                customer.profile_pic.save(file_name, ContentFile(f.read()))
                return JsonResponse({'message': 'Données importées avec succès.'})
            except Exception as e:
                print(e)  # Log the error to the console
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Form not valid'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def export_customers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['username', 'first_name', 'last_name', 'email', 'address', 'mobile', 'profile_pic'])

    customers = Customer.objects.all()
    for customer in customers:
        profile_pic_url = customer.profile_pic.url if customer.profile_pic else ''
        writer.writerow([
            customer.user.username, 
            customer.user.first_name, 
            customer.user.last_name, 
            customer.user.email, 
            customer.address, 
            customer.mobile,
            profile_pic_url
        ])

    return response

    return response     
def export_to_csv(request):
    # Récupérer les données des deux modèles
    customers = Customer.objects.all()
    technicians = Technician.objects.all()

    # Fusionner les données dans une liste
    all_data = list(customers) + list(technicians)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    # Définir les noms de colonnes pour les deux modèles
    fieldnames = ['Name', 'Address', 'Mobile', 'Skill', 'Salary', 'Status']

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()

    # Écrire les données dans le fichier CSV
    for obj in all_data:
        if isinstance(obj, Customer):
            row = {'Name': obj.get_name, 'Address': obj.address, 'Mobile': obj.mobile,
                   'Skill': '', 'Salary': '', 'Status': ''}
        elif isinstance(obj, Technician):
            row = {'Name': obj.get_name, 'Address': obj.address, 'Mobile': obj.mobile,
                   'Skill': obj.skill, 'Salary': obj.salary, 'Status': obj.status}
        writer.writerow(row)

    return response

    context = {'form': form}
    return render(request, 'service/export.html', context)




def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'service/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'service/customerclick.html')

#for showing signup/login button for Technicians
def Techniciansclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'service/Techniciansclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'service/customersignup.html',context=mydict)


def Technician_signup_view(request):
    userForm=forms.TechnicianUserForm()
    TechnicianForm=forms.TechnicianForm()
    mydict={'userForm':userForm,'TechnicianForm':TechnicianForm}
    if request.method=='POST':
        userForm=forms.TechnicianUserForm(request.POST)
        TechnicianForm=forms.TechnicianForm(request.POST,request.FILES)
        if userForm.is_valid() and TechnicianForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            Technician=TechnicianForm.save(commit=False)
            Technician.user=user
            Technician.save()
            my_Technician_group = Group.objects.get_or_create(name='Technician')
            my_Technician_group[0].user_set.add(user)
        return HttpResponseRedirect('Technicianlogin')
    return render(request,'service/Techniciansignup.html',context=mydict)


#for checking user customer, Technician or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_Technician(user):
    return user.groups.filter(name='Technician').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_Technician(request.user):
        accountapproval=models.Technician.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('Technician-dashboard')
        else:
            return render(request,'service/Technician_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start by | ahmedabddaymeahmedbouha | 23243 |
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_Technician':models.Technician.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'service/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'service/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'service/admin_view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'service/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'service/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'service/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'service/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_Technician_view(request):
    return render(request,'service/admin_Technician.html')


@login_required(login_url='adminlogin')
def admin_approve_Technician_view(request):
    Technicians=models.Technician.objects.all().filter(status=False)
    return render(request,'service/admin_approve_Technician.html',{'Technicians':Technicians})

@login_required(login_url='adminlogin')
def approve_Technician_view(request,pk):
    TechnicianSalary=forms.TechnicianSalaryForm()
    if request.method=='POST':
        TechnicianSalary=forms.TechnicianSalaryForm(request.POST)
        if TechnicianSalary.is_valid():
            Technician=models.Technician.objects.get(id=pk)
            Technician.salary=TechnicianSalary.cleaned_data['salary']
            Technician.status=True
            Technician.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-Technician')
    return render(request,'service/admin_approve_Technician_details.html',{'TechnicianSalary':TechnicianSalary})


@login_required(login_url='adminlogin')
def delete_Technician_view(request,pk):
    Technician=models.Technician.objects.get(id=pk)
    user=models.User.objects.get(id=Technician.user_id)
    user.delete()
    Technician.delete()
    return redirect('admin-approve-Technician')


@login_required(login_url='adminlogin')
def admin_add_Technician_view(request):
    userForm=forms.TechnicianUserForm()
    TechnicianForm=forms.TechnicianForm()
    TechnicianSalary=forms.TechnicianSalaryForm()
    mydict={'userForm':userForm,'TechnicianForm':TechnicianForm,'TechnicianSalary':TechnicianSalary}
    if request.method=='POST':
        userForm=forms.TechnicianUserForm(request.POST)
        TechnicianForm=forms.TechnicianForm(request.POST,request.FILES)
        TechnicianSalary=forms.TechnicianSalaryForm(request.POST)
        if userForm.is_valid() and TechnicianForm.is_valid() and TechnicianSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            Technician=TechnicianForm.save(commit=False)
            Technician.user=user
            Technician.status=True
            Technician.salary=TechnicianSalary.cleaned_data['salary']
            Technician.save()
            my_Technician_group = Group.objects.get_or_create(name='Technician')
            my_Technician_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-Technician')
        else:
            print('problem in form')
    return render(request,'service/admin_add_Technician.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_Technician_view(request):
    Technicians=models.Technician.objects.all()
    return render(request,'service/admin_view_Technician.html',{'Technicians':Technicians})


@login_required(login_url='adminlogin')
def delete_Technician_view(request,pk):
    Technician=models.Technician.objects.get(id=pk)
    user=models.User.objects.get(id=Technician.user_id)
    user.delete()
    Technician.delete()
    return redirect('admin-view-Technician')


@login_required(login_url='adminlogin')
def update_Technician_view(request,pk):
    Technician=models.Technician.objects.get(id=pk)
    user=models.User.objects.get(id=Technician.user_id)
    userForm=forms.TechnicianUserForm(instance=user)
    TechnicianForm=forms.TechnicianForm(request.FILES,instance=Technician)
    mydict={'userForm':userForm,'TechnicianForm':TechnicianForm}
    if request.method=='POST':
        userForm=forms.TechnicianUserForm(request.POST,instance=user)
        TechnicianForm=forms.TechnicianForm(request.POST,request.FILES,instance=Technician)
        if userForm.is_valid() and TechnicianForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            TechnicianForm.save()
            return redirect('admin-view-Technician')
    return render(request,'service/update_Technician.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_Technician_salary_view(request):
    Technicians=models.Technician.objects.all()
    return render(request,'service/admin_view_Technician_salary.html',{'Technicians':Technicians})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    TechnicianSalary=forms.TechnicianSalaryForm()
    if request.method=='POST':
        TechnicianSalary=forms.TechnicianSalaryForm(request.POST)
        if TechnicianSalary.is_valid():
            Technician=models.Technician.objects.get(id=pk)
            Technician.salary=TechnicianSalary.cleaned_data['salary']
            Technician.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-Technician-salary')
    return render(request,'service/admin_approve_Technician_details.html',{'TechnicianSalary':TechnicianSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'service/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'service/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.Technician=adminenquiry.cleaned_data['Technician']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'service/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.Technician=adminenquiry.cleaned_data['Technician']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'service/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'service/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.Technician=adminenquiry.cleaned_data['Technician']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'service/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'service/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'service/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_Technician_attendance_view(request):
    return render(request,'service/admin_Technician_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    Technicians=models.Technician.objects.all().filter(status=True)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                print(Technicians[i].id)
                print(int(Technicians[i].id))
                Technician=models.Technician.objects.get(id=int(Technicians[i].id))
                AttendanceModel.Technician=Technician
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request,'service/admin_take_attendance.html',{'Technicians':Technicians,'aform':aform})

@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date)
            Techniciandata=models.Technician.objects.all().filter(status=True)
            mylist=zip(attendancedata,Techniciandata)
            return render(request,'service/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'service/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'service/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'service/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END by | ahmedabddaymeahmedbouha | 23243 |
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start  by | ahmedabddaymeahmedbouha | 23243 |
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'service/customer_dashboard.html',context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'service/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'service/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'service/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'service/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'service/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'service/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'service/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'service/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'service/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'service/customer_feedback.html',{'feedback':feedback,'customer':customer})

#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================





#============================================================================================
# Technician RELATED views start by 23243| 23104 |23044
#============================================================================================


@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_dashboard_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(Technician_id=Technician.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(Technician_id=Technician.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(Technician_id=Technician.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':Technician.salary,
    'Technician':Technician,
    }
    return render(request,'service/Technician_dashboard.html',context=dict)

@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_work_assigned_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(Technician_id=Technician.id)
    return render(request,'service/Technician_work_assigned.html',{'works':works,'Technician':Technician})


@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_update_status_view(request,pk):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    updateStatus=forms.TechnicianUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.TechnicianUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/Technician-work-assigned')
    return render(request,'service/Technician_update_status.html',{'updateStatus':updateStatus,'Technician':Technician})

@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_attendance_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(Technician=Technician)
    return render(request,'service/Technician_view_attendance.html',{'attendaces':attendaces,'Technician':Technician})





@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_feedback_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'service/feedback_sent.html',{'Technician':Technician})
    return render(request,'service/Technician_feedback.html',{'feedback':feedback,'Technician':Technician})

@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_salary_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(Technician_id=Technician.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'service/Technician_salary.html',{'workdone':workdone,'Technician':Technician})

@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def Technician_profile_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    return render(request,'service/Technician_profile.html',{'Technician':Technician})

@login_required(login_url='Technicianlogin')
@user_passes_test(is_Technician)
def edit_Technician_profile_view(request):
    Technician=models.Technician.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=Technician.user_id)
    userForm=forms.TechnicianUserForm(instance=user)
    TechnicianForm=forms.TechnicianForm(request.FILES,instance=Technician)
    mydict={'userForm':userForm,'TechnicianForm':TechnicianForm,'Technician':Technician}
    if request.method=='POST':
        userForm=forms.TechnicianUserForm(request.POST,instance=user)
        TechnicianForm=forms.TechnicianForm(request.POST,request.FILES,instance=Technician)
        if userForm.is_valid() and TechnicianForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            TechnicianForm.save()
            return redirect('Technician-profile')
    return render(request,'service/edit_Technician_profile.html',context=mydict)






#============================================================================================
# Technician RELATED views end by | Ahmed Abd Dayme Ahmed Bouha 23243
#============================================================================================

#============================================================================================
#for aboutus and contact
#==============================================================================================
def aboutus_view(request):
    return render(request,'service/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'service/contactussuccess.html')
    return render(request, 'service/contactus.html', {'form':sub})

# moi tp2
def import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                if 'email' in row:  # Assuming the presence of 'email' indicates Customer data
                    customer, created = Customer.objects.get_or_create(
                        email=row['email'],
                        defaults={
                            'name': row['name'],
                            'phone': row['phone']
                        }
                    )
                else:  # Otherwise, it's Service data
                    customer = Customer.objects.get(email=row['customer_email'])
                    Service.objects.create(
                        service_name=row['service_name'],
                        description=row['description'],
                        customer=customer
                    )
            return redirect('success')
    else:
        form = CSVImportForm()
    return render(request, 'import_csv.html', {'form': form})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'email', 'phone'])
    customers = Customer.objects.all()
    for customer in customers:
        writer.writerow([customer.id, customer.name, customer.email, customer.phone])

    writer.writerow([])
    writer.writerow(['id', 'service_name', 'description', 'customer_id'])
    services = Service.objects.all()
    for service in services:
        writer.writerow([service.id, service.service_name, service.description, service.customer.id])
    
    return response


def success(request):
    return HttpResponse('Importation réussie!')

