from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework


from api.models import Comment, Post, Follow, Group
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, PostSerializer,
                             FollowSerializer, GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ('group', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        comments = Comment.objects.all()
        post_id = self.kwargs['id']
        queryset = comments.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs['id']
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        queryset = self.request.user.following
        return queryset

    def perform_create(self, serializer):
        if self.request.user.username == self.request.POST.get('following'):
            raise serializers.ValidationError
        serializer.save(user=self.request.user)


class GroupViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
