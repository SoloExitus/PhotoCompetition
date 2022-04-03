from django.forms import Field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListSerializer, BaseSerializer

from .models import PhotoPost, User, Comment
from .services import is_liked_post


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image')


class PhotoPostListSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    author = UserSerializer(source='user', read_only=True)

    class Meta:
        model = PhotoPost
        fields = ['id', 'title', 'description', 'is_liked', 'published_at', 'updated_at', 'full_image', 'state',
                  'total_likes', 'total_comments', 'author']
        read_only_fields = ['published_at', 'updated_at', 'state', 'likes_count', 'comments_count', 'author']

    def get_is_liked(self, post) -> bool:
        """Проверяет, лайкнул ли `request.user` post.
        """
        user = self.context.get('request').user
        return is_liked_post(post, user)


class PhotoPostInfoSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = PhotoPost
        fields = ['is_liked', 'total_likes', 'total_comments']

    def get_is_liked(self, post) -> bool:
        """Проверяет, лайкнул ли `request.user` post.
        """
        user = self.context.get('request').user
        return is_liked_post(post, user)


class FilteredNestedCommentListSerializer(ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent__isnull=True)
        return super(FilteredNestedCommentListSerializer, self).to_representation(data)


class NestedCommentSerializer(ModelSerializer):
    author = UserSerializer(source='user')
    comment_children = serializers.SerializerMethodField()

    def get_comment_children(self, comment):
        if comment.comment_children is not None:
            return NestedCommentSerializer(comment.comment_children, many=True).data
        else:
            return None

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at', 'comment_children')


class PostCommentSerializer(ModelSerializer):
    author = UserSerializer(source='user')
    comment_children = serializers.SerializerMethodField()

    def get_comment_children(self, comment):
        if comment.comment_children is not None:
            return NestedCommentSerializer(comment.comment_children, many=True).data
        else:
            return None

    class Meta:
        model = Comment
        list_serializer_class = FilteredNestedCommentListSerializer
        fields = ('id', 'author', 'text', 'created_at', 'comment_children')


class PhotoPostDetailSerializer(PhotoPostListSerializer):
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = PhotoPost
        fields = (
            'id',
            'title',
            'description',
            'is_liked',
            'full_image',
            'published_at',
            'total_likes',
            'total_comments',
            'author',
            'comments',
        )


class CommentsSerializer(ModelSerializer):
    author = UserSerializer(source='user')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_at')

