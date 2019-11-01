from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.generic import ListView

from app.forms import CommentForm, UserForm
from app.models import Post, Comment, Tag


# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 2  # Two posts on default page
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def comment_approve(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    comment.approve()
    return redirect('post_detail', slug=comment.post.slug)


def comment_remove(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    comment.delete()
    return redirect('post_detail', slug=comment.post.slug)


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)  # slug_iexact is a sort method
    return render(request, 'tag_detail.html', context={'tag': tag})


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             registered = True
#         else:
#             print(user_form.errors)
#     else:
#         user_form = UserForm()
#     return render(request, 'registration/registration.html',
#                   {'user_form': user_form},
#                   {'registered': registered})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'registration/registration.html',
                  {'user_form': user_form,
                   'registered': registered})


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list
