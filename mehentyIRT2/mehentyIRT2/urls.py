"""
service
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from service import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
#from .views import import_data, export_data
from django.conf.urls.static import static

urlpatterns = [
    path('admin_chart/', views.admin_chart, name='admin_chart'),
    path('admin/', admin.site.urls),
    path('import-customers/', views.import_customers, name='import-customers'),
    path('export-customers/', views.export_customers, name='export-customers'),
    # other paths...

    # path('import/', views.import_customers, name='import-customers'),
    # path('export/', views.export_customers, name='export-customers'),

    path('export_request/', views.export_to_csv, name='export_to_csv'),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('Techniciansclick', views.Techniciansclick_view),

   
    path('adminlogin', LoginView.as_view(template_name='service/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    path('admin-Technician', views.admin_Technician_view,name='admin-Technician'),
    path('admin-view-Technician',views.admin_view_Technician_view,name='admin-view-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
    path('update-Technician/<int:pk>', views.update_Technician_view,name='update-Technician'),
    path('admin-add-Technician',views.admin_add_Technician_view,name='admin-add-Technician'),
    path('admin-approve-Technician',views.admin_approve_Technician_view,name='admin-approve-Technician'),
    path('approve-Technician/<int:pk>', views.approve_Technician_view,name='approve-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),
    path('admin-view-Technician-salary',views.admin_view_Technician_salary_view,name='admin-view-Technician-salary'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),
    path('admin-report', views.admin_report_view,name='admin-report'),

    path('logout', LogoutView.as_view(template_name='service/index.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    #================
    #client or custmor
    #=================

    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='service/customerlogin.html'),name='customerlogin'),
    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),
    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),
    #================
    #Technician
    #================
    path('Techniciansignup', views.Technician_signup_view,name='Techniciansignup'),
    path('Technicianlogin', LoginView.as_view(template_name='service/Technicianlogin.html'),name='Technicianlogin'), 
    path('afterlogin', views.afterlogin_view,name='afterlogin'),  
    path('Technician-dashboard', views.Technician_dashboard_view,name='Technician-dashboard'),
    path('Technician-work-assigned', views.Technician_work_assigned_view,name='Technician-work-assigned'),
    path('Technician-update-status/<int:pk>', views.Technician_update_status_view,name='Technician-update-status'),
    path('Technician-profile', views.Technician_profile_view,name='Technician-profile'),
    path('edit-Technician-profile', views.edit_Technician_profile_view,name='edit-Technician-profile'),
    path('Technician-salary', views.Technician_salary_view,name='Technician-salary'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



   

