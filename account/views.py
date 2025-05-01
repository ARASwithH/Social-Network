from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from . import forms
from .models import Relation, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views


# Create your views here.

class UserRegistration(View):
    form_class = forms.UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404('page not found')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/registration.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            return redirect('account:profile_detail', user.id)
        print(form.errors)
        messages.error(request, 'Invalid username or password', 'warning')
        return render(request, 'account/registration.html', {'form': form})


class UserLogin(View):
    form_class = forms.UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next_url = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404('page not found')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'{cd["username"]} logged in', 'success')
                if self.next_url:
                    return redirect(self.next_url)
                return redirect('home:index')
        messages.error(request, 'Invalid username or password', 'warning')
        return render(request, 'account/login.html', {'form': form})


class UserProfile(LoginRequiredMixin, View):
    form_class = forms.UserProfileForm

    def get(self, request):
        posts = request.user.posts.all()
        return render(request, 'account/profile.html', {"posts": posts})

    def post(self, request):
        if 'logout-button' in request.POST:
            logout(request)
            messages.success(request, 'Logged out successfully', 'success')
            return redirect('home:index')


class UserPage(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        rel = Relation.objects.filter(from_user=request.user.id, to_user=user_id)
        if rel.exists():
            is_following = True

        posts = user.posts.all()
        return render(request, 'account/page.html', {'user': user,
                                                     'posts': posts,
                                                     'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password/resetpassword.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Email'})
        return form


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'New password'})
        form.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'New password confirmation'})

        return form


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relations = Relation.objects.filter(from_user=request.user.id, to_user=user_id)
        if relations.exists():
            messages.warning(request, 'You are already following this user', 'warning')
            return redirect('account:page', user_id=user.id)
        Relation.add(request.user, user)
        return redirect('account:page', user_id=user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relations = Relation.objects.filter(from_user=request.user.id, to_user=user_id)
        if relations.exists():
            relations.delete()
            return redirect('account:page', user_id=user.id)
        messages.warning(request, 'You are not following this user', 'warning')
        return redirect('account:page', user_id=user.id)


class UserProfileDetailView(View):
    form = forms.UserProfileDetailsForm

    def get(self, request, user_id):
        return render(request, 'account/profile_detail.html', {'form': self.form,
                                                               'name': 'sign'})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = forms.UserProfileDetailsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = Profile.objects.get(user=user)
            profile.bio = cd['bio']
            profile.age = cd['age']
            profile.gender = cd['gender']
            user.profile = profile
            messages.success(request, 'Account created successfully', 'success')
            return redirect('home:index')
        messages.error(request, 'Invalid username or password', 'warning')
        print(form.errors)
        return render(request, 'account/profile_detail.html', {'form': self.form})


class UserProfileDetailUpdateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        profile = user.profile
        form = forms.UserProfileDetailsForm(instance=profile)
        return render(request, 'account/profile_detail.html', {'form': form,
                                                               'name': 'Edit'})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        profile = user.profile
        form = forms.UserProfileDetailsForm(request.POST, instance=profile)
        if form.is_valid():
            cd = form.cleaned_data
            profile.age = cd['age']
            profile.bio = cd['bio']
            profile.gender = cd['gender']
            profile.save()
            messages.success(request, 'Account updated successfully', 'success')
            return redirect('account:profile')
        return render(request, 'account/profile_detail.html', {'form': form})

