from .serializers import PostSerializer
from .models import Post


def get_filterquery(request_get):
    filt_query = {}
    for key in request_get:
        if key[0] != "_" and key[-3:] != "_ne":
            
            filt_query.update(
                {
                    f"{key[:-5]}__icontains"if key[-5:]=="_like" else key: request_get[key]
                }
            )
    return filt_query 


def get_excludequery(request_get):
    excludequery = {}
    for key in request_get:
       if key[-3:] == "_ne":
            
            excludequery.update(
                {
                    key[:-3]: request_get[key]
                }
            )
    return excludequery 


class PostBase:
    queryset = Post.objects.all()
    serializer_class = PostSerializer