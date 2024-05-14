"""
service
"""
from django.contrib import admin
from django.urls import path
from service import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

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
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-Technician', views.admin_Technician_view,name='admin-Technician'),
    path('admin-view-Technician',views.admin_view_Technician_view,name='admin-view-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
    path('update-Technician/<int:pk>', views.update_Technician_view,name='update-Technician'),
    path('admin-add-Technician',views.admin_add_Technician_view,name='admin-add-Technician'),
    path('admin-approve-Technician',views.admin_approve_Technician_view,name='admin-approve-Technician'),
    path('approve-Technician/<int:pk>', views.approve_Technician_view,name='approve-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
    path('admin-view-Technician-salary',views.admin_view_Technician_salary_view,name='admin-view-Technician-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    path('admin-Technician-attendance', views.admin_Technician_attendance_view,name='admin-Technician-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),

    
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='service/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]