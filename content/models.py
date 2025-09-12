from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    icon = models.CharField(
        max_length=50, 
        verbose_name="Icône FontAwesome", 
        help_text="Ex: fas fa-laptop-code"
    )
    display_order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du projet")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='projects/', verbose_name="Image du projet")
    technologies = models.CharField(
        max_length=300, 
        verbose_name="Technologies utilisées", 
        help_text="Séparer par des virgules"
    )
    demo_url = models.URLField(blank=True, verbose_name="Lien de démonstration")
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    completion_date = models.DateField(verbose_name="Date d'achèvement")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-completion_date', 'name']

    def __str__(self):
        return self.name

    @property
    def technologies_list(self):
        """Retourne la liste des technologies sous forme de liste Python"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class Testimonial(models.Model):
    RATING_CHOICES = [(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(1, 6)]
    
    author = models.CharField(max_length=100, verbose_name="Auteur")
    position = models.CharField(max_length=100, verbose_name="Poste")
    company = models.CharField(max_length=100, verbose_name="Entreprise")
    content = models.TextField(verbose_name="Contenu du témoignage")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} - {self.company}"

    @property
    def rating_stars(self):
        """Retourne la note sous forme d'étoiles"""
        return "★" * self.rating + "☆" * (5 - self.rating)