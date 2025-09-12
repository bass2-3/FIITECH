from rest_framework import serializers
from .models import Service, Project, Testimonial

class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'icon', 'display_order']


class ProjectSerializer(serializers.ModelSerializer):
    technologies_list = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'image_url', 'technologies', 
            'technologies_list', 'demo_url', 'github_url', 'completion_date'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class TestimonialSerializer(serializers.ModelSerializer):
    rating_stars = serializers.ReadOnlyField()
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'author', 'position', 'company', 'content', 
            'rating', 'rating_stars', 'created_at'
        ]


# Sérialiseurs pour les statistiques du dashboard
class ServiceStatsSerializer(serializers.Serializer):
    total_services = serializers.IntegerField()
    active_services = serializers.IntegerField()
    inactive_services = serializers.IntegerField()


class ProjectStatsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    recent_projects = serializers.IntegerField()


class TestimonialStatsSerializer(serializers.Serializer):
    total_testimonials = serializers.IntegerField()
    approved_testimonials = serializers.IntegerField()
    pending_testimonials = serializers.IntegerField()
    average_rating = serializers.FloatField()


class RatingDistributionSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    count = serializers.IntegerField()


class DashboardStatsSerializer(serializers.Serializer):
    services = ServiceStatsSerializer()
    projects = ProjectStatsSerializer()
    testimonials = TestimonialStatsSerializer()
    rating_distribution = RatingDistributionSerializer(many=True)