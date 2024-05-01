from rest_framework import serializers

from .models import Care, Advice, CustomUser, Post, Pictures, Category, Comment


class CareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Care
        fields = '__all__'

class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'