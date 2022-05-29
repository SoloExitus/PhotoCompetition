from rest_framework import serializers

from competition.serializers.User import UserSerializer
from competition.models import Comment


class NestedCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user')
    comment_children = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, comment):
        return comment.created_at.strftime("%d-%m-%Y")

    def get_comment_children(self, comment):
        if comment.comment_children is not None:
            return NestedCommentSerializer(comment.comment_children, many=True).data
        else:
            return None

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at', 'comment_children')


class FilteredNestedCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent__isnull=True)
        return super(FilteredNestedCommentListSerializer, self).to_representation(data)


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user')
    comment_children = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_comment_children(self, comment):
        return NestedCommentSerializer(comment.comment_children, many=True).data

    def get_created_at(self, comment):
        return comment.created_at.strftime("%d-%m-%Y")

    class Meta:
        model = Comment
        list_serializer_class = FilteredNestedCommentListSerializer
        fields = ('id', 'author', 'text', 'created_at', 'comment_children')


class CommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user', read_only=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, comment):
        return comment.created_at.strftime("%d-%m-%Y")

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'parent', 'created_at')
