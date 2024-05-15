from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q


# importation et exportation :
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from .forms import CSVUploadForm

from .models import Customer,Technician
from .forms import CSVUploadForm
import csv
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from .forms import CSVUploadForm
import requests

def import_customers(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
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
                    profile_pic_url = row['profile_pic']
                    response = requests.get(profile_pic_url)
                    if response.status_code == 200:
                        file_name = profile_pic_url.split("/")[-1]
                        customer.profile_pic.save(file_name, ContentFile(response.content))
            messages.success(request, 'Données importées avec succès.')
            return redirect('admin-view-customer')
    else:
        form = CSVUploadForm()
    return render(request, 'service/import.html', {'form': form})

def import_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Le fichier n\'est pas au format CSV')
            return HttpResponseRedirect(request.path_info)

        # Lecture du fichier CSV et création des objets
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            if 'Skill' in row:  # Pour distinguer entre Customer et Technician
                technician = Technician.objects.create(
                    user=None,  # Vous devrez remplir ces champs en fonction de votre logique
                    address=row['Address'],
                    mobile=row['Mobile'],
                    skill=row['Skill'],
                    salary=row['Salary'],
                    status=row['Status']
                )
            else:
                customer = Customer.objects.create(
                    user=None,  # Vous devrez remplir ces champs en fonction de votre logique
                    address=row['Address'],
                    mobile=row['Mobile']
                )

        # Redirection après l'importation réussie
        return HttpResponseRedirect('/import/success/')  # Changer l'URL selon vos besoins

    else:
        form = ImportForm()  # Créez un formulaire d'importation si nécessaire
        return render(request, 'import.html', {'form': form})  # Afficher le formulaire d'importation dans le template
        
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

def export_customers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    # Ajouter le champ profile_pic à l'en-tête
    writer.writerow(['username', 'first_name', 'last_name', 'email', 'address', 'mobile', 'profile_pic'])

    customers = Customer.objects.all()
    for customer in customers:
        # Ajouter profile_pic à la ligne de données
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



# for aboutus and contact
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
