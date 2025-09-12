from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render

from .models import Service, Project, Testimonial
from .serializers import (
    ServiceSerializer, ProjectSerializer, TestimonialSerializer,
    DashboardStatsSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    """Pagination standard pour les APIs"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ServiceListView(generics.ListAPIView):
    """API endpoint pour lister tous les services actifs"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    pagination_class = None  # Pas de pagination pour les services


class ProjectListView(generics.ListAPIView):
    """API endpoint pour lister tous les projets"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Permet de filtrer par technologie si spécifiée"""
        queryset = Project.objects.all()
        technology = self.request.query_params.get('technology', None)
        if technology:
            queryset = queryset.filter(technologies__icontains=technology)
        return queryset


class TestimonialListView(generics.ListAPIView):
    """API endpoint pour lister tous les témoignages approuvés"""
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Permet de filtrer par note minimale si spécifiée"""
        queryset = Testimonial.objects.filter(is_approved=True)
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            try:
                min_rating = int(min_rating)
                if 1 <= min_rating <= 5:
                    queryset = queryset.filter(rating__gte=min_rating)
            except ValueError:
                pass
        return queryset


@api_view(['GET'])
def dashboard_stats(request):
    """API endpoint pour les statistiques du dashboard"""
    # Statistiques des services
    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()
    inactive_services = total_services - active_services

    # Statistiques des projets
    total_projects = Project.objects.count()
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_projects = Project.objects.filter(completion_date__gte=thirty_days_ago).count()

    # Statistiques des témoignages
    total_testimonials = Testimonial.objects.count()
    approved_testimonials = Testimonial.objects.filter(is_approved=True).count()
    pending_testimonials = total_testimonials - approved_testimonials
    
    avg_rating = Testimonial.objects.filter(is_approved=True).aggregate(
        avg=Avg('rating')
    )['avg'] or 0

    # Distribution des notes
    rating_distribution = Testimonial.objects.filter(is_approved=True).values(
        'rating'
    ).annotate(
        count=Count('rating')
    ).order_by('rating')

    stats_data = {
        'services': {
            'total_services': total_services,
            'active_services': active_services,
            'inactive_services': inactive_services
        },
        'projects': {
            'total_projects': total_projects,
            'recent_projects': recent_projects
        },
        'testimonials': {
            'total_testimonials': total_testimonials,
            'approved_testimonials': approved_testimonials,
            'pending_testimonials': pending_testimonials,
            'average_rating': round(avg_rating, 2)
        },
        'rating_distribution': list(rating_distribution)
    }

    serializer = DashboardStatsSerializer(data=stats_data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_overview(request):
    """Vue d'ensemble de l'API avec tous les endpoints disponibles"""
    api_urls = {
        'Services': {
            'List active services': '/api/services/',
            'Service detail': '/api/services/{id}/',
        },
        'Projects': {
            'List all projects': '/api/projects/',
            'Filter by technology': '/api/projects/?technology={tech_name}',
            'Project detail': '/api/projects/{id}/',
        },
        'Testimonials': {
            'List approved testimonials': '/api/testimonials/',
            'Filter by min rating': '/api/testimonials/?min_rating={1-5}',
            'Testimonial detail': '/api/testimonials/{id}/',
        },
        'Dashboard': {
            'Statistics': '/api/dashboard/stats/',
        },
        'API Info': {
            'This overview': '/api/',
        }
    }
    
    return Response({
        'message': 'Bienvenue sur l\'API FiiTech Solutions',
        'version': '1.0',
        'endpoints': api_urls
    })