from django.shortcuts import redirect
from django.http import Http404
from .models import User
from .forms import UserFormAccess, UserFormNotAccess, UserFormEdit, UserFormEditAccess, UserFormAccessOnlyYouSuper, UserFormAccessOnlyYou

#the mixins

# this mixin for get access to user for see this page or not
# if user not superuser or access it return a 404 errorr
class GetAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()

# this mixin for get acces just to superuser
# if user not superuser it return a 404 errorr
class GetAccessCreateMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()

# this mixin for valid a form
# this mixin set author to loggin user
class SetAuthorMixin():
    def form_valid(self, form):
        self.obj = form.save(commit = False)
        self.obj.book_author = self.request.user
        self.obj.save()
        return super().form_valid(form)

# this mixin for valid a form
# this mixin set superuser and access user to False
class SetNotAccessMixin():
    def form_valid(self, form):
        self.obj = form.save(commit = False)
        self.obj.is_access = False
        self.obj.is_superuser = False
        self.obj.save()
        return super().form_valid(form)

# this mixin for choise a form_class for our view According to user access
class GetUserFormsMixin():
    def get_form_class(self):
        if self.request.user.is_superuser:
            self.form_class = UserFormAccess
            return super().get_form_class()
        elif self.request.user.is_access:
            self.form_class = UserFormNotAccess
            return super().get_form_class()
        else:
            raise Http404()

# this mixin for get a form_class, dispatch, template_name for our view according to user access
class UpdateUserFormMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        self.user_get_access = User.objects.get(pk = pk)
        return super().dispatch(request, *args, **kwargs)
    def get_form_class(self):
        if self.request.user.is_superuser:
            if self.request.user == self.user_get_access:
                self.form_class = UserFormAccessOnlyYouSuper
            else:
                self.form_class = UserFormEditAccess
            return super().get_form_class()
        elif self.request.user.is_access:
            if self.request.user == self.user_get_access:
                self.form_class = UserFormAccessOnlyYou
            else:
                self.form_class = UserFormEdit
            return super().get_form_class()
        else:
            raise Http404()
    def get_template_names(self):
        if self.request.user == self.user_get_access:
            self.template_name = 'registration/admin-account/edit_user_access.html'
            return super().get_template_names()
        else:
            self.template_name = 'registration/admin-account/user_edit.html'
            return super().get_template_names()

# this mixin for access to our user for delete a object
class UserDeleteAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()
# this mixin redirect user to home if user is authenticate
class ReturnIfAuthenticateMixin():
    # dispatch method
    def dispatch(self, request, *args, **kwargs):
        # if user is authenticate return to home
        if request.user.is_authenticated:
            return redirect('books:index')
        # else return the page
        else:
            return super().dispatch(request, *args, **kwargs)