from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    thumbnail_200 = serializers.SerializerMethodField()
    thumbnail_400 = serializers.SerializerMethodField()
    original_image = serializers.SerializerMethodField()
    expiring_link = serializers.SerializerMethodField()

    def get_thumbnail_200(self, obj):
        return obj.thumbnail_200_path.url
    
    def get_thumbnail_400(self, obj):
        return obj.thumbnail_400_path.url if obj.user.account_tier in ('premium', 'enterprise') else None
    
    def get_original_image(self, obj):
        return obj.image.url if obj.user.account_tier == 'enterprise' else None

    def get_expiring_link(self, obj):
        return None
    
    class Meta:
        model = Image
        fields = ('id', 'thumbnail_200', 'thumbnail_400', 'original_image', 'expiring_link', 'created')


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)