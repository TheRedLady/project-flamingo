from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    )
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Tag, Like, Share
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostCreateUpdateSerializer,
    PostLikeSerializer
    )


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostByTagAPIView(ListAPIView):
    model = Post
    serializer_class = PostListSerializer

    def get_queryset(self, *args, **kwargs):
        requested_tag = Tag.objects.get(tag='#' + self.kwargs['tag'])
        posts = Post.objects.filter(tag=requested_tag).order_by('-created')
        return posts


# Tova view moje da vryshta samo 1 element zashtoto izpylnqva get()
# Inache vryshta greshka
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # lookup_field = 'posted_by'  -  po koe pole ot modela tyrsim
    # lookup_url_kwarg = 'field2'  -  kak da se kazva to v url patterna


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PostEditAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def like(self, request, pk=None):
        user = self.request.user
        print "REQUEST QUERY PARAMETERS ", self.request.query_params
        pk = self.request.query_params['id']
        serializer = PostLikeSerializer(data=request.data)
        try:
            obj, created = Like.objects.get_or_create(Like, liked_by=user, post=pk)
            return Response({'liked_by_user': True})
        except:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
