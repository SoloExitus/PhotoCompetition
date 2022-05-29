from rest_framework import serializers

from competition.models import PhotoPost
from competition.serializers.User import UserSerializer
from competition.serializers.Comment import PostCommentSerializer
from competition.services import is_liked_post


class PhotoPostListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    author = UserSerializer(source='user', read_only=True)
    preview_image = serializers.ImageField(read_only=True)

    class Meta:
        model = PhotoPost
        fields = ['id', 'title', 'description', 'is_liked', 'updated_at', 'created_at', 'full_image', 'preview_image',
                  'state', 'total_likes', 'total_comments', 'author']
        read_only_fields = ['updated_at', 'state', 'likes_count', 'comments_count', 'author']

    def get_is_liked(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` post.
        """
        user = self.context.get('request').user
        return is_liked_post(obj, user)


class PhotoPostInfoSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = PhotoPost
        fields = ['is_liked', 'total_likes', 'total_comments']

    def get_is_liked(self, post) -> bool:
        """Проверяет, лайкнул ли `request.user` post.
        """
        user = self.context.get('request').user
        return is_liked_post(post, user)


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
            'created_at',
            'author',
            'comments',
        )