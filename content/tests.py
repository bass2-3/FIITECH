from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from PIL import Image
import io
import json

from .models import Service, Project, Testimonial

class ServiceModelTest(TestCase):
    """Tests pour le modèle Service"""
    
    def setUp(self):
        self.service = Service.objects.create(
            title="Développement Web",
            description="Création de sites web modernes",
            icon="fas fa-laptop-code",
            display_order=1
        )
    
    def test_service_creation(self):
        """Test de création d'un service"""
        self.assertEqual(self.service.title, "Développement Web")
        self.assertTrue(self.service.is_active)
        self.assertEqual(self.service.display_order, 1)
        
    def test_service_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.service), "Développement Web")
    
    def test_service_ordering(self):
        """Test de l'ordre d'affichage des services"""
        service2 = Service.objects.create(
            title="Design UI/UX",
            description="Design d'interfaces utilisateur",
            icon="fas fa-paint-brush",
            display_order=0
        )
        services = list(Service.objects.all())
        self.assertEqual(services[0], service2)  # Order 0 en premier
        self.assertEqual(services[1], self.service)  # Order 1 en second


class ProjectModelTest(TestCase):
    """Tests pour le modèle Project"""
    
    def setUp(self):
        # Créer une image de test
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        self.project = Project.objects.create(
            name="Site E-commerce",
            description="Plateforme de vente en ligne",
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=image_file.getvalue(),
                content_type='image/jpeg'
            ),
            technologies="Django, React, PostgreSQL",
            demo_url="https://demo.example.com",
            github_url="https://github.com/example/project",
            completion_date=date.today()
        )
    
    def test_project_creation(self):
        """Test de création d'un projet"""
        self.assertEqual(self.project.name, "Site E-commerce")
        self.assertEqual(self.project.technologies, "Django, React, PostgreSQL")
        
    def test_technologies_list_property(self):
        """Test de la propriété technologies_list"""
        expected_techs = ["Django", "React", "PostgreSQL"]
        self.assertEqual(self.project.technologies_list, expected_techs)
    
    def test_project_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.project), "Site E-commerce")


class TestimonialModelTest(TestCase):
    """Tests pour le modèle Testimonial"""
    
    def setUp(self):
        self.testimonial = Testimonial.objects.create(
            author="Jean Dupont",
            position="CEO",
            company="TechCorp",
            content="Excellent travail, très satisfait !",
            rating=5
        )
    
    def test_testimonial_creation(self):
        """Test de création d'un témoignage"""
        self.assertEqual(self.testimonial.author, "Jean Dupont")
        self.assertEqual(self.testimonial.rating, 5)
        self.assertFalse(self.testimonial.is_approved)  # Par défaut non approuvé
        
    def test_rating_stars_property(self):
        """Test de la propriété rating_stars"""
        self.assertEqual(self.testimonial.rating_stars, "★★★★★")
        
        # Test avec 3 étoiles
        testimonial_3_stars = Testimonial.objects.create(
            author="Marie Martin",
            position="Manager",
            company="WebCorp",
            content="Bon travail",
            rating=3
        )
        self.assertEqual(testimonial_3_stars.rating_stars, "★★★☆☆")
    
    def test_testimonial_str_method(self):
        """Test de la méthode __str__"""
        expected_str = "Jean Dupont - TechCorp"
        self.assertEqual(str(self.testimonial), expected_str)


class ServiceAPITest(APITestCase):
    """Tests pour l'API des services"""
    
    def setUp(self):
        self.service_active = Service.objects.create(
            title="Service Actif",
            description="Service activé",
            icon="fas fa-check",
            is_active=True
        )
        self.service_inactive = Service.objects.create(
            title="Service Inactif",
            description="Service désactivé",
            icon="fas fa-times",
            is_active=False
        )
    
    def test_service_list_api(self):
        """Test de l'endpoint de liste des services"""
        url = reverse('content:service_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Seulement les services actifs
        self.assertEqual(response.data[0]['title'], "Service Actif")
    
    def test_service_list_format(self):
        """Test du format de réponse de l'API services"""
        url = reverse('content:service_list')
        response = self.client.get(url)
        
        service_data = response.data[0]
        expected_fields = ['id', 'title', 'description', 'icon', 'display_order']
        
        for field in expected_fields:
            self.assertIn(field, service_data)


class ProjectAPITest(APITestCase):
    """Tests pour l'API des projets"""
    
    def setUp(self):
        # Créer une image de test
        image = Image.new('RGB', (100, 100), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        self.project1 = Project.objects.create(
            name="Projet Django",
            description="Application Django",
            image=SimpleUploadedFile(
                name='test_project.jpg',
                content=image_file.getvalue(),
                content_type='image/jpeg'
            ),
            technologies="Django, Python, PostgreSQL",
            completion_date=date.today()
        )
        
        self.project2 = Project.objects.create(
            name="App React",
            description="Application React Native",
            image=SimpleUploadedFile(
                name='test_project2.jpg',
                content=image_file.getvalue(),
                content_type='image/jpeg'
            ),
            technologies="React, JavaScript, Node.js",
            completion_date=date.today() - timedelta(days=30)
        )
    
    def test_project_list_api(self):
        """Test de l'endpoint de liste des projets"""
        url = reverse('content:project_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_project_technology_filter(self):
        """Test du filtrage par technologie"""
        url = reverse('content:project_list')
        response = self.client.get(url, {'technology': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Projet Django")
    
    def test_project_data_format(self):
        """Test du format de données des projets"""
        url = reverse('content:project_list')
        response = self.client.get(url)
        
        project_data = response.data['results'][0]
        expected_fields = [
            'id', 'name', 'description', 'image_url', 'technologies', 
            'technologies_list', 'demo_url', 'github_url', 'completion_date'
        ]
        
        for field in expected_fields:
            self.assertIn(field, project_data)
        
        # Test de technologies_list
        self.assertIsInstance(project_data['technologies_list'], list)


class TestimonialAPITest(APITestCase):
    """Tests pour l'API des témoignages"""
    
    def setUp(self):
        self.testimonial_approved = Testimonial.objects.create(
            author="Client Satisfait",
            position="Manager",
            company="HappyCorp",
            content="Travail exceptionnel !",
            rating=5,
            is_approved=True
        )
        
        self.testimonial_pending = Testimonial.objects.create(
            author="Client En Attente",
            position="CEO",
            company="PendingCorp",
            content="En cours de validation",
            rating=4,
            is_approved=False
        )
    
    def test_testimonial_list_api(self):
        """Test de l'endpoint de liste des témoignages"""
        url = reverse('content:testimonial_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Seulement les approuvés
        self.assertEqual(response.data['results'][0]['author'], "Client Satisfait")
    
    def test_testimonial_min_rating_filter(self):
        """Test du filtrage par note minimale"""
        # Créer un témoignage avec note faible
        Testimonial.objects.create(
            author="Client Moyen",
            position="User",
            company="AverageCorp",
            content="Travail correct",
            rating=3,
            is_approved=True
        )
        
        url = reverse('content:testimonial_list')
        response = self.client.get(url, {'min_rating': '4'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Seulement note >= 4
    
    def test_testimonial_data_format(self):
        """Test du format de données des témoignages"""
        url = reverse('content:testimonial_list')
        response = self.client.get(url)
        
        testimonial_data = response.data['results'][0]
        expected_fields = [
            'id', 'author', 'position', 'company', 'content', 
            'rating', 'rating_stars', 'created_at'
        ]
        
        for field in expected_fields:
            self.assertIn(field, testimonial_data)
        
        self.assertEqual(testimonial_data['rating_stars'], "★★★★★")


class DashboardStatsAPITest(APITestCase):
    """Tests pour l'API des statistiques du dashboard"""
    
    def setUp(self):
        # Créer des données de test
        Service.objects.create(title="Service 1", description="Desc 1", icon="fa-1", is_active=True)
        Service.objects.create(title="Service 2", description="Desc 2", icon="fa-2", is_active=False)
        
        # Créer une image de test
        image = Image.new('RGB', (100, 100), color='green')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        Project.objects.create(
            name="Projet Recent",
            description="Projet récent",
            image=SimpleUploadedFile('recent.jpg', image_file.getvalue(), 'image/jpeg'),
            technologies="Tech1",
            completion_date=date.today()
        )
        
        Project.objects.create(
            name="Projet Ancien",
            description="Projet ancien",
            image=SimpleUploadedFile('old.jpg', image_file.getvalue(), 'image/jpeg'),
            technologies="Tech2",
            completion_date=date.today() - timedelta(days=60)
        )
        
        Testimonial.objects.create(
            author="Test 1", position="Pos 1", company="Corp 1",
            content="Content 1", rating=5, is_approved=True
        )
        
        Testimonial.objects.create(
            author="Test 2", position="Pos 2", company="Corp 2",
            content="Content 2", rating=4, is_approved=False
        )
    
    def test_dashboard_stats_api(self):
        """Test de l'endpoint des statistiques"""
        url = reverse('content:dashboard_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier la structure des données
        data = response.data
        self.assertIn('services', data)
        self.assertIn('projects', data)
        self.assertIn('testimonials', data)
        self.assertIn('rating_distribution', data)
        
        # Vérifier les statistiques des services
        services_stats = data['services']
        self.assertEqual(services_stats['total_services'], 2)
        self.assertEqual(services_stats['active_services'], 1)
        self.assertEqual(services_stats['inactive_services'], 1)
        
        # Vérifier les statistiques des projets
        projects_stats = data['projects']
        self.assertEqual(projects_stats['total_projects'], 2)
        self.assertEqual(projects_stats['recent_projects'], 1)  # Seulement le récent
        
        # Vérifier les statistiques des témoignages
        testimonials_stats = data['testimonials']
        self.assertEqual(testimonials_stats['total_testimonials'], 2)
        self.assertEqual(testimonials_stats['approved_testimonials'], 1)
        self.assertEqual(testimonials_stats['pending_testimonials'], 1)


class APIOverviewTest(APITestCase):
    """Tests pour la vue d'ensemble de l'API"""
    
    def test_api_overview(self):
        """Test de l'endpoint d'aperçu de l'API"""
        url = reverse('content:api_overview')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertIn('message', data)
        self.assertIn('version', data)
        self.assertIn('endpoints', data)
        
        # Vérifier que les endpoints principaux sont présents
        endpoints = data['endpoints']
        self.assertIn('Services', endpoints)
        self.assertIn('Projects', endpoints)
        self.assertIn('Testimonials', endpoints)
        self.assertIn('Dashboard', endpoints)