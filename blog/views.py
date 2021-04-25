from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,  ListView, UpdateView, DeleteView
from blog.forms import UserForm, PostForm, LoginForm
from blog.models import Profile, Post


class SignUp(CreateView):
    form_class = UserForm
    template_name = 'blog/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        form.save()
        profession = form.cleaned_data['profession']
        mobile = form.cleaned_data['mobile']
        Profile.objects.create(profession=profession, mobile=mobile, user=user)
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        valid = super(SignUp, self).form_valid(form)
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_success_url(self):
        return reverse('index')


class Login(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = '/dashboard/'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardListView(ListView):
    model = Post
    template_name = 'blog/dashboard.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return super(DashboardListView, self).get_queryset()
        else:
            return super(DashboardListView, self).get_queryset()


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
            return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_queryset(self):
        return super(PostUpdate, self).get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse('dashboard')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostDelete(DeleteView):
    model = Post

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            return Http404
        else:
            return obj
    def get_success_url(self):
        return reverse('dashboard')
