from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.core.exceptions import PermissionDenied

from ALCPT_Online_Platform.settings import LOGOUT_REDIRECT_URL
from registration.models import User, Student
from registration.forms import SignUpForm, ProfileEditForm
from registration.definition import Privilege, Identity
from registration.file import user_photo_storage, user_photo_remove

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('index')


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successfully")
    return redirect(LOGOUT_REDIRECT_URL)


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'user/list.html'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['privilege'] = Privilege.__members__
        return context


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'user/detail.html'
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    context = {'user': request.user,
               'privileges': Privilege.__members__}

    return render(request, 'account/profile.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = User
    template_name = 'account/profile_edit.html'
    form_class = ProfileEditForm
    success_url = 'profile'

    def form_valid(self, form):
        # the left side 'form' means 'User' object
        form = form.save(commit=False)
        # This statement seems doing nothing
        if form.identity == Identity.Student.value[0]:
            student = Student.objects.create(user=self.request.user)
            student.save()
        else:
            student = Student.objects.get(user=form)
            student.delete()
        form.save()
        return redirect('profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)


@login_required
def photo_upload(request):
    user = request.user

    if request.method == 'POST':
        try:
            photo = request.FILES.get('photo_file')
            user_photo_storage(user=user, photo=photo)
        except AttributeError:
            pass
        return redirect('profile_edit')
    else:
        context = {'user': user}
        return render(request, 'account/profile_edit.html', context)


@login_required
def current_photo_delete(request):
    user = request.user
    user_photo_remove(user)
    return redirect('profile_edit')
