from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from .models import Post, Category
from .serializers import PostSerializer, CatSerializer, PostBaseSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.forms import model_to_dict
from .utils import get_filterquery, get_excludequery, PostBase
from .pagination import PageLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly




class PostListAPIView(PostBase, generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageLimitPagination
    #filterset_fields = ("title", "body")
    filterset_fields = "__all__"

    def get_queryset(self):
        ordering = self.request.GET.get("_sort", "pk")
        queryset_order = self.queryset.order_by(ordering)
        queryset_exclude = Post.objects.exclude(**get_excludequery(self.request.GET))
        return queryset_order & queryset_exclude


class PostCreate(PostBase, generics.CreateAPIView):
    pass


class PostRetrive(PostBase, generics.RetrieveAPIView):
    pass


class PostUpdate(PostBase, generics.RetrieveAPIView):
    pass


class PostDelete(PostBase, generics.RetrieveAPIView):
    pass



class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageLimitPagination
    #filterset_fields = ("title", "body")
    filterset_fields = "__all__"
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        ordering = self.request.GET.get("_sort", "pk")
        queryset_order = self.queryset.order_by(ordering)
        queryset_exclude = Post.objects.exclude(**get_excludequery(self.request.GET))
        return queryset_order & queryset_exclude


class PostRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)



class PostAPIView(APIView, PageLimitPagination): 
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        # retrive
        if pk:

            try:
                instance = Post.objects.get(pk=pk)
            except:
                return Response({"Error": "That object does not exist"})
            serializer = PostSerializer(instance)
            # instance = model_to_dict(instance)
        # list
        else:
            ordering = request.GET.get("_sort", "pk")
            try:
                queryset = self.paginate_queryset(
                    Post.objects.filter(
                        **get_filterquery(request.GET)).order_by(ordering)
                    &
                    Post.objects.exclude(**get_excludequery(request.GET)), 
                    request,
                    view = self
                )
            except:
                return Response("there is no such parameter")
            serializer = PostSerializer(queryset, many=True)
        # list_queryset= list(queryset.values())
        return Response(serializer.data)

    # create
    def post(self, request):
        #new_post = Post.objects.create(
        #    title=request.data["title"],
        #    body=request.data["body"],
        #    category_id=request.data["category_id"],
        #)
        serializer = PostSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # destroy
    def delete(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response("method DELETE not allowed")
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"Error": "That object does not exist"})
        instance.delete()
        return Response(f"{instance.title} has been deleted")

    # update
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response("method PUT not allowed")
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"Error": "That object does not exist"})
        #instance.title = request.data["title"]
        #instance.body = request.data["body"]
        #instance.category_id = request.data["category_id"]
        #instance.save()

        serializer = PostSerializer(data = request.data, instance = instance) 
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # patch
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response("method PATCH not allowed")
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"Error": "That object does not exist"})

        #instance.title = request.data.get("title",instance.title )  
        #instance.body = request.data.get("body", instance.body)
        #instance.category_id = request.data.get(
        #    "category_id", instance.category_id)
        #instance.save()

        serializer = PostSerializer(data = request.data, instance = instance, partial = True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CategoryAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        # retrive
        if pk:
            try:
                instance = Category.objects.get(pk=pk)
            except:
                return Response({"Error": "That object does not exist"})
            serializer = CatSerializer(instance)
            # instance = model_to_dict(instance)
        # list
        else:
            queryset = Category.objects.all()
            serializer = CatSerializer(queryset, many=True)
            # list_queryset= list(queryset.values())
        return Response(serializer.data)


class CategoryPostAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        category = Category.objects.prefetch_related("posts").get(pk=pk)
        queryset = category.posts.all()
        serializer = CatSerializer(queryset, many=True)
        # list_queryset= list(queryset.values())
        return Response(serializer.data)


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatSerializer
    permission_classes = (IsAdminOrReadOnly,) 

