from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Service, Project, Testimonial

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['display_order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['display_order', 'title']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Paramètres d\'affichage', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'completion_date', 'display_technologies', 'has_demo', 'has_github']
    list_filter = ['completion_date', 'created_at']
    search_fields = ['name', 'description', 'technologies']
    date_hierarchy = 'completion_date'
    
    fieldsets = (
        ('Informations du projet', {
            'fields': ('name', 'description', 'image')
        }),
        ('Technologies et liens', {
            'fields': ('technologies', 'demo_url', 'github_url')
        }),
        ('Dates', {
            'fields': ('completion_date',)
        }),
    )
    
    def display_technologies(self, obj):
        """Affiche les technologies avec un format lisible"""
        techs = obj.technologies_list
        if len(techs) <= 3:
            return ', '.join(techs)
        return f"{', '.join(techs[:3])}... (+{len(techs)-3})"
    display_technologies.short_description = "Technologies"
    
    def has_demo(self, obj):
        """Indique si le projet a une démo"""
        if obj.demo_url:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_demo.short_description = "Démo"
    
    def has_github(self, obj):
        """Indique si le projet a un lien GitHub"""
        if obj.github_url:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_github.short_description = "GitHub"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'company', 'rating_display', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at', 'company']
    list_editable = ['is_approved']
    search_fields = ['author', 'company', 'content']
    actions = ['approve_testimonials', 'unapprove_testimonials']
    
    fieldsets = (
        ('Informations de l\'auteur', {
            'fields': ('author', 'position', 'company')
        }),
        ('Témoignage', {
            'fields': ('content', 'rating')
        }),
        ('Modération', {
            'fields': ('is_approved',)
        }),
    )
    
    def rating_display(self, obj):
        """Affiche la note avec des étoiles"""
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span>',
            obj.rating_stars
        )
    rating_display.short_description = "Note"
    
    def approve_testimonials(self, request, queryset):
        """Action pour approuver les témoignages sélectionnés"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request, 
            f'{updated} témoignage(s) approuvé(s) avec succès.'
        )
    approve_testimonials.short_description = "Approuver les témoignages sélectionnés"
    
    def unapprove_testimonials(self, request, queryset):
        """Action pour désapprouver les témoignages sélectionnés"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request, 
            f'{updated} témoignage(s) désapprouvé(s) avec succès.'
        )
    unapprove_testimonials.short_description = "Désapprouver les témoignages sélectionnés"
    
    def get_queryset(self, request):
        """Optimise les requêtes"""
        return super().get_queryset(request).select_related()