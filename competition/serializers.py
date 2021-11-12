from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import PhotoPost, User, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'thumbnail')


class PhotoPostListSerializer(ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    author = UserSerializer(source='user')

    class Meta:
        model = PhotoPost
        fields = ('id', 'title', 'description', 'published_date', 'full_image', 'likes_count', 'comments_count', 'author')


class CommentChildrenSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_date', 'children')


class CommentListSerializer(ModelSerializer):
    author = UserSerializer(source='user')
    children = CommentChildrenSerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id',  'author', 'text', 'created_date', 'children')


class PhotoPostDetailSerializer(ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    author = UserSerializer(source='user')
    comments = CommentListSerializer()

    class Meta:
        model = PhotoPost
        fields = ('id', 'title', 'description', 'published_date', 'full_image', 'likes_count', 'comments_count', 'author', 'comments')