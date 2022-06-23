from audioop import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment
from blog.forms import Postform, Commentform
from . import forms
# Create your views here.

def home(request):
    return render(request, 'blog/base.html', {'title': 'Home'})

class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    #context_object_name = 'post'
    def get_queryset(self):
        return Post.objects.all()
    

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = Postform
    model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = Postform
    model = Post

def DeletePostView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:draft_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    context_object_name = 'drafts'
    model = Post

    def get_queryset(self):
        return Post.objects.all()

class RegisterView(CreateView):
    form_class = forms.RegForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

#For Comment
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = Commentform()
    return render(request, 'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_details',pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_details',pk = comment.id)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=id)
    post.publish()
    return redirect('blog:post_details',pk=id)

