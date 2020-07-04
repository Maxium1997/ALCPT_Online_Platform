from os import listdir

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, TemplateView, CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Q

from ALCPT_Online_Platform.settings import LOGOUT_REDIRECT_URL, MEDIA_ROOT
from registration.models import User, Student
from registration.forms import SignUpForm, ProfileEditForm, UserFilterForm
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
    return redirect(LOGOUT_REDIRECT_URL)


# For system manager to query the users in the system.
@method_decorator(login_required, name='dispatch')
class UserListView(View):
    def dispatch(self, request, *args, **kwargs):
        required_privilege = Privilege.SystemManager
        if not request.user.has_permission(required_privilege):
            raise PermissionDenied
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        template = 'user/list.html'
        context = {'users': User.objects.all(),
                   'user_filter_form': UserFilterForm()}
        return render(request, template, context)

    def post(self, request):
        user_filter_form = UserFilterForm(request.POST)

        if user_filter_form.is_valid():
            filter_criteria = Q()
            if user_filter_form.cleaned_data['content']:
                filter_criteria &= Q(username__icontains=user_filter_form.cleaned_data['content']) | \
                                   Q(last_name__icontains=user_filter_form.cleaned_data['content']) | \
                                   Q(first_name__icontains=user_filter_form.cleaned_data['content'])
            if user_filter_form.cleaned_data['identity']:
                filter_criteria &= Q(identity=user_filter_form.cleaned_data['identity'])

            users = list(User.objects.filter(filter_criteria))

        else:
            users = User.objects.all()

        template = 'user/list.html'
        context = {'users': users,
                   'user_filter_form': user_filter_form}
        return render(request, template, context)


# For system manager to view the user in the system.
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


# For users to view the profile of themselves.
@login_required
def profile(request):
    context = {'user': request.user,
               'privileges': Privilege.__members__}

    return render(request, 'account/profile.html', context)


# For users to edit the profile of themselves.
@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = User
    template_name = 'account/profile_edit.html'
    form_class = ProfileEditForm
    success_url = 'profile'

    def form_valid(self, form):
        # the left side 'form' means 'User' object
        form = form.save(commit=False)
        if form.identity == Identity.Student.value[0]:
            try:
                student = Student.objects.create(user=self.request.user)
                student.save()
            except IntegrityError:
                pass
        else:
            student = Student.objects.get(user=form)
            student.delete()
        form.save()
        return redirect('profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)


# A function to upload the user photo
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


# A function to delete the current photo of user
@login_required
def current_photo_delete(request):
    user = request.user
    user_photo_remove(user)
    return redirect('profile_edit')


@method_decorator(login_required, name='dispatch')
class AlbumView(TemplateView):
    template_name = 'account/album.html'

    def get_context_data(self, **kwargs):
        photo_path_list = []

        album_path = MEDIA_ROOT + 'photos/' + self.request.user.username

        for file in listdir(album_path):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                photo_path_list.append(
                    '/' + MEDIA_ROOT.split('/')[-2] + '/photos/' + self.request.user.username + '/' + file)

        context = {'user': self.request.user,
                   'photo_list': photo_path_list}

        return context
