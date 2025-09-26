from rest_framework import serializers
from .models import Repository
class RepoSerializer(serializers.ModelSerializer):
    owner_username=serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model=Repository
        fields=['id','owner','owner_username','name','description','is_private','created_at']
        read_only_fields=['owner','created_at']
