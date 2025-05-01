from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View

from home.forms import PostForm, CommentForm, CommentReplyForm
from home.models import Post


# Create your views here.

class HomeView(View):
    def get(self, request):
        order = request.GET.get('order', 'date_updated')
        reverse = request.GET.get('reverse') is not None
        query = request.GET.get('search')
        order_by = f'-{order}' if reverse else order

        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            posts = Post.objects.all().order_by(order_by)

        return render(request, 'home/index.html', {
            'posts': posts,
            'order': order,
            'reverse': reverse
        })


class PostView(View):
    form = CommentForm
    form_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['pk'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.pcomments.all()
        return render(request, 'home/post_detail.html', {'post': post,
                                                         'comments': comments,
                                                         'comment_form': self.form,
                                                         'comment_reply': self.form_reply, })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        print(request.POST)
        post = self.post_instance

        if request.POST.get("comment"):
            cform = CommentForm(request.POST)
            if cform.is_valid():
                comment = cform.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, 'Your comment has been saved.', 'success')
                return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)

        if request.POST.get("reply"):
            replied_comment = request.POST.get("replied_comment", None)
            if replied_comment:
                rform = CommentReplyForm(request.POST)
                print(replied_comment)
                replied_comment = post.pcomments.get(pk=replied_comment)
                if rform.is_valid():
                    comment = rform.save(commit=False)
                    comment.author = request.user
                    comment.post = post
                    comment.comment = replied_comment
                    comment.is_reply = True
                    comment.save()
                    messages.success(request, 'Your reply has been saved.', 'success')
                    return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
                print(rform.errors)
            print(replied_comment)
        print(1)


class PostEditView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['pk'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.auther.id != request.user.id:
            messages.error(request, 'You are not authorized to edit this post.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        edit_post = self.post_instance
        post_form = PostForm(instance=edit_post)
        return render(request, 'home/post_edit.html', {'post': edit_post, 'post_form': post_form})

    def post(self, request, *args, **kwargs):
        edit_post = self.post_instance

        post_form = PostForm(request.POST, instance=edit_post)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.slug = slugify(f'{post_form.cleaned_data["title"]}')
            new_post.save()
            messages.success(request, 'Your post has been edited.', 'success')
            return redirect(edit_post.get_absolute_url())
        else:
            messages.error(request, 'Somthing went wrong', 'danger')
            return redirect(edit_post.get_absolute_url())


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, post_slug):
        post = Post.objects.get(id=pk, slug=post_slug)
        if request.user.id == post.auther.id:
            post.delete()
            messages.success(request, 'Your post has been deleted.', 'success')
            return redirect('account:profile')
        else:
            messages.warning(request, 'You can not delete this post', 'warning')
            return redirect(post.get_absolute_url())


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostForm

    def get(self, request):
        form = self.form_class
        return render(request, 'home/post_create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(f'{form.cleaned_data["title"]}')
            new_post.auther = request.user
            new_post.save()
            messages.success(request, 'Your post has been created.', 'success')
            return redirect('home:index')
        else:
            messages.error(request, 'Somthing went wrong', 'danger')
            return redirect('home:index')


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        like = post.likes.filter(user=request.user)
        if like.exists():
            like.delete()
        else:
            post.likes.create(user=request.user, post=post)
        return redirect('home:post_detail', post.id, post.slug)
