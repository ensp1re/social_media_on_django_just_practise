from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    pform = PostModelForm()
    cform = PostModelForm()
    post_add = False

    if 'submit_c_form' in request.POST:
        pform = PostModelForm(request.POST, request.FILES)
        if cform.is_valid():
            instance = cform.save(commit=False)
            instance.author = profile
            instance.save()
            cform = CommentModelForm()
            post_add = True

    if 'submit_p_form' in request.POST:
        cform = PostModelForm(request.POST)
        if pform.is_valid():
            instance = pform.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            pform = PostModelForm()



    context = {
        "qs": qs,
        'profile' : profile,
        'p_form' : pform,
        'post_add' : post_add,


    }

    return render(request, "posts/main.html", context)

def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value = "Like"

            post_obj.save()
            like.save()
        data = {
            "value" : like.value,
            'likes' : post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('posts:main-post-view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/confirm_del.html"
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "You need to be author of the post to be deleted")
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be author of the post to be updated")
            return super().form_invalid(form)