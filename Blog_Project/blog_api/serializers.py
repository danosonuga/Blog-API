from django.contrib.auth.models import User
from blog_api.models import Post, Comment, Category, Like, SubComment, UserProfile
from rest_framework import serializers


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_pic', 'created']

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'img_thumbnail', 'body', 'category', 'date_created']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'message', 'author', 'added_at']

class SubCommentSerializer(serializers.ModelSerializer):
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = SubComment
        fields = ['id', 'message', 'author', 'added_at']

class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = ['id', 'value', 'author', 'added_at']