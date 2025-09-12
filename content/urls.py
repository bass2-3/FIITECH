from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # API Overview
    path('api/', views.api_overview, name='api_overview'),
    
    # Services endpoints
    path('api/services/', views.ServiceListView.as_view(), name='service_list'),
    
    # Projects endpoints  
    path('api/projects/', views.ProjectListView.as_view(), name='project_list'),
    
    # Testimonials endpoints
    path('api/testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    
    # Dashboard endpoints
    path('api/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    
]