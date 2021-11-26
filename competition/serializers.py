from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import PhotoPost, User, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'thumbnail', 'profile_image')


class PhotoPostListSerializer(ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    author = UserSerializer(source='user', read_only=True)

    class Meta:
        model = PhotoPost
        fields = ['id', 'title', 'description', 'published_at', 'updated_at', 'full_image', 'state', 'likes_count',
                  'comments_count', 'author']
        read_only_fields = ['published_at', 'updated_at', 'state', 'likes_count', 'comments_count', 'author']


class CommentSerializer(ModelSerializer):
    author = UserSerializer(source='user')
    comment_children = serializers.SerializerMethodField()

    def get_comment_children(self, obj):
        if obj.comment_children is not None:
            return CommentSerializer(obj.comment_children, many=True).data
        else:
            return None

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at', 'updated_at', 'comment_children')


class PhotoPostDetailSerializer(PhotoPostListSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = PhotoPost
        fields = (
            'id',
            'title',
            'description',
            'full_image',
            'published_at',
            'likes_count',
            'comments_count',
            'author',
            'comments',
        )