from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.

def posts_view(request):

    post = Post.objects.all()
    context = {'posts': post}

    return render(request, 'blog/posts.html', context)


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'