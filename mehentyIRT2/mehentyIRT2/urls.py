"""
service
"""
from django.contrib import admin
from django.urls import path
from service import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
# from .views import import_data, export_data

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('import/', views.import_customers, name='import-customers'),
    path('export/', views.export_customers, name='export-customers'),

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
   

    path('admin-Technician', views.admin_Technician_view,name='admin-Technician'),
    path('admin-view-Technician',views.admin_view_Technician_view,name='admin-view-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
    path('update-Technician/<int:pk>', views.update_Technician_view,name='update-Technician'),
    path('admin-add-Technician',views.admin_add_Technician_view,name='admin-add-Technician'),
    path('admin-approve-Technician',views.admin_approve_Technician_view,name='admin-approve-Technician'),
    path('approve-Technician/<int:pk>', views.approve_Technician_view,name='approve-Technician'),
    path('delete-Technician/<int:pk>', views.delete_Technician_view,name='delete-Technician'),
   
    
  
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='service/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='service/customerlogin.html'),name='customerlogin'),
    path('Techniciansignup', views.Technician_signup_view,name='Techniciansignup'),
    path('Technicianlogin', LoginView.as_view(template_name='service/Technicianlogin.html'),name='Technicianlogin'),   
]

