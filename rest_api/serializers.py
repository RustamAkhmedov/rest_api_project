from rest_framework import serializers
from .models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("__all__")  


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")  


class PostBaseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    body = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published= serializers.BooleanField(default=True)
    category = serializers.IntegerField()
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.category_id = validated_data.get(
            "category_id", instance.category_id)
        instance.save()
        return instance
