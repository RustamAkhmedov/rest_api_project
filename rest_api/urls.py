from django.urls import path
from .views import PostRetriveUpdateDestroyApiView, PostListAPIView, PostListViewset, PostModelViewSet, PostAPIView, CategoryAPIView, CategoryPostAPIView, PostCreate, PostRetrive, PostUpdate, PostDelete, CategoryModelViewSet
from django.urls import include 
from rest_framework import routers


post_router = routers.SimpleRouter()
#post_router.register(r"posts", PostListViewset, basename= "post")
post_router.register(r"posts", PostModelViewSet)

category_router = routers.SimpleRouter()
#post_router.register(r"posts", PostListViewset, basename= "post")
category_router.register(r"categories", CategoryModelViewSet)


urlpatterns = [
    #path("api/posts/",PostAPIView.as_view()),
    #path("api/posts/<int:pk>/",PostAPIView.as_view()),
    path("api/categories/",CategoryAPIView.as_view()),
    path("api/categories/<int:pk>/",CategoryAPIView.as_view()),
    path("api/categories/<int:pk>/posts/",CategoryPostAPIView.as_view()),
    path("api/",include(post_router.urls)),

    path("post/list/",PostListAPIView.as_view()),
    path("post/create/",PostCreate.as_view()),
    path("post/<int:pk>/retrive/",PostRetrive.as_view()),
    path("post/<int:pk>/update/",PostUpdate.as_view()),
    path("post/<int:pk>/destroy/",PostDelete.as_view()),

    path("posts/",PostAPIView.as_view()),
    path("posts/<int:pk>/",PostAPIView.as_view()),
    path("",include(category_router.urls)),
    path("api-auth",include("rest_framework.urls")),
    path("auth",include("djoser.urls")),
    path("auth",include("djoser.urls.authtoken")),
] 

