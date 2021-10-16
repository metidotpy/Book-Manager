#import useful modules
from django.db import models
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import User
from .forms import UserForm, UserFormAccess, UserFormNotAccess
from django.urls import reverse_lazy
from django.http import HttpResponse, request
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from books.models import BookModel
from .mixins import GetAccessMixin, GetAccessCreateMixin, SetAuthorMixin, SetNotAccessMixin, GetUserFormsMixin, UpdateUserFormMixin, UserDeleteAccessMixin, ReturnIfAuthenticateMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from .forms import UserFormAccess, UserFormNotAccess, UserFormEdit, UserFormEditAccess, UserFormAccessOnlyYouSuper, UserFormAccessOnlyYou, PasswordChangeForm

# Create your views here.

# login view it inheritance from LoginView in django.contrib.auth.views.LoginView and im change success url according to user access
class LoginView(ReturnIfAuthenticateMixin ,LoginView):
    #for redirect users
    redirect_authenticated_user = True

    # this method can let us to acces to self for authenticate users
    def get_success_url(self):
        # if user is superuser or access reverse to admin panel
        if self.request.user.is_superuser or self.request.user.is_access:
            return reverse_lazy('account:book_list')
        
        #if not superuser or access reverse to index page :)
        return reverse_lazy('books:index')
# change the PasswordChangeView for change form class and success url
class PasswordChangeView(LoginRequiredMixin, GetAccessMixin,PasswordChangeView):
    # password change
    form_class = PasswordChangeForm
    # template name
    template_name = 'registration/admin-account/password_change_form.html'
    # success url
    success_url = reverse_lazy('account:password_change_done')

# change PasswordChangeDone view for admins
class PasswordChangeDoneView(LoginRequiredMixin, GetAccessMixin, PasswordChangeDoneView):
    # template name
    template_name = 'registration/admin-account/password_change_done.html'

# register view (you can registration with email confirm link)
class CreateUser(SetNotAccessMixin, ReturnIfAuthenticateMixin, CreateView):
    # get form class for registration users
    form_class = UserForm
    # our model is User
    model = User
    # form validation for send email confirmation link
    def form_valid(self, form):
        # we are save user with commit false if commit false you can change anything to the object and save it later
        user = form.save(commit=False)
        # user activation to false if active is false user cant login and work to the site
        user.is_active = False
        # we save user with is_active eq to false
        user.save()
        # get current site url
        current_site = get_current_site(self.request)
        # subject for send mail
        mail_subject = 'Activate Your Account'
        # our message, im use render to string a html file
        # it give an html file and renders to string for send to user
        message = render_to_string('email-confirmation/email_template.html', {
            # get current user
            'user': user,
            # our domain we get in in current_site
            'domain': current_site.domain,
            # make a uid for token with user.pk
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            # create token only for this user
            'token':account_activation_token.make_token(user),
        })
        # send email for user email in registration page
        to_email = form.cleaned_data.get('email')
        # send email with Email Message
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        # send email
        email.send()
        # render page to confirmation send
        return render(self.request, 'email-confirmation/email_send_login.html')
    # if is success rever user to login page
    success_url = reverse_lazy('login')
    # our template name
    template_name = 'registration/signup.html'


# make active token
def activate(request, uidb64, token):
    try:
        # get uid from user
        uid = force_text(urlsafe_base64_decode(uidb64))
        # get user with uid variable
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        # if we have error user eq to None
        user = None

    # if user not none and checked token if token is ok
    if user is not None and account_activation_token.check_token(user, token):
        # user active to true and save it
        user.is_active = True
        user.save()
        # if user authenticated
        if request.user.is_authenticated:
            # if superuser or access
            if request.user.is_superuser or request.user.is_access:
                # return to admin page
                return render(request, 'registration/admin-account/confirmed.html')
        else:
            #else go to site
            return render(request, 'email-confirmation/confirmed.html')
        return render(request, 'email-confirmation/confirmed.html')
    else:
        # if user authenticate with token false
        if request.user.is_authenticated:
            # if superuser or acceess
            if request.user.is_superuser or request.user.is_access:
                # go to admin panel
                return render(request, 'registration/admin-account/not_confirmed.html')
        else:
            #else go to site
            return render(request, 'email-confirmation/not_confirmed.html')
        return render(request, 'email-confirmation/not_confirmed.html')


# show book list view for admins
class BookList(LoginRequiredMixin, GetAccessMixin, ListView):
    # get queryset
    def get_queryset(self):
        # if user is superuser or access give all objects
        if self.request.user.is_superuser or self.request.user.is_access:
            return BookModel.objects.all()
    # template name
    template_name = 'registration/admin-account/books_list.html'

# search books
class BookSearch(LoginRequiredMixin, GetAccessMixin, ListView):
    # our model
    model = BookModel
    # queryset for give result
    def get_queryset(self):
        result = super(BookSearch, self).get_queryset()
        # get query from the search input
        query = self.request.GET.get('table_search')
        if query:
            # if query exists if useruser
            if self.request.user.is_superuser:
                #search books for fields
                bookresult = BookModel.objects.filter(
                    Q(book_name__contains = query) | Q(book_writer__contains = query) | Q(book_description__contains = query) | Q(pk__contains = query) | Q(book_slug__contains = query)
                )
            #else if query exists and user is access
            elif self.request.user.is_access:
                # search books for fields
                bookresult = BookModel.objects.filter(
                    Q(book_name__contains = query) | Q(book_writer__contains = query) | Q(book_description__contains = query) | Q(pk__contains = query)
                )
            result = bookresult
        else:
            # if qiery doesn't exists result = None
            result: None
        # return result
        return result
    # template
    template_name = 'registration/admin-account/book_search.html'

# delete books
class BookDelete(LoginRequiredMixin, GetAccessMixin, DeleteView):
    # our model
    model = BookModel
    # user slug instead of pk
    slug_field = 'book_slug'
    # success url
    # reverse to admin panel book list
    success_url = reverse_lazy('account:book_list')
    # template name
    template_name = 'registration/admin-account/book_confirm_delete.html'

#create books
class BookCreate(LoginRequiredMixin, GetAccessMixin, SetAuthorMixin, CreateView):
    # our model
    model = BookModel
    # our fields
    fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status']
    # template name
    template_name = 'registration/admin-account/book_add_edit.html'

#update books
class BookUpdate(LoginRequiredMixin, GetAccessCreateMixin, UpdateView):
    # our model
    model = BookModel
    # our fields
    fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status']
    # use slug instead of pk
    slug_field = 'book_slug'
    # template name
    template_name = 'registration/admin-account/book_add_edit.html'

# show admin panel user list
class UserList(LoginRequiredMixin, GetAccessMixin, ListView):
    # get queryset
    def get_queryset(self):
        # if user is superuser or user is access return all objects
        if self.request.user.is_superuser or self.request.user.is_access:
            return User.objects.all()
    # template name
    template_name = 'registration/admin-account/users_list.html'

# user search
class UserSearch(LoginRequiredMixin, GetAccessMixin, ListView):
    # our model
    model = User
    # get queryset
    def get_queryset(self):
        result = super(UserSearch, self).get_queryset()
        # get query from the search input
        query = self.request.GET.get('table_search')
        if query:
            # if query exists if user is super user
            if self.request.user.is_superuser:
                userresult = User.objects.filter(
                    Q(username__contains = query) | Q(first_name__contains = query) | Q(last_name__contains = query) | Q(pk__contains = query) | Q(email__contains = query) | Q(phone__contains = query)
                )
            #search user for fields
            elif self.request.user.is_access:
                userresult = User.objects.filter(
                    Q(username__contains = query) | Q(first_name__contains = query) | Q(last_name__contains = query) | Q(pk__contains = query)
                )
            # search user for fields
            result = userresult
        else:
            # if qiery doesn't exists result = None
            result: None
        # return result
        return result
    # template
    template_name = 'registration/admin-account/user_search.html'

# create user from admin panel
class UserCreate(LoginRequiredMixin,GetAccessMixin, GetUserFormsMixin,CreateView):
    # our model
    model = User
    # validation our form
    def form_valid(self, form):
        # get user and commit eq to false
        # if commit eq to false we can edit this object and change it , then we can save it again
        user = form.save(commit = False)
        # check user access
        if self.request.user.is_superuser:
            # if user is super user and active eq to false
            # we want here send a email confirmation for this user
            if not user.is_active:
                # user is_active eq to false
                # if is_active is false user can't login and do can't anything to site
                user.is_active = False
                # save user
                user.save()
                # get current domain url
                current_site = get_current_site(self.request)
                # mail subject
                mail_subject = 'Activate Your Account'
                # message, we use render to string to html file to string for sending email
                message = render_to_string('email-confirmation/email_template.html', {
                    # get user
                    'user': user,
                    # get current site url
                    'domain': current_site.domain,
                    # create a uid
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    # create a token for this user
                    'token':account_activation_token.make_token(user),
                })
                # send email for email in registration form
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            # create a instance for send email
                            mail_subject, message, to=[to_email]
                )
                # sending email
                email.send()
                # reverse to "confirmation send" page
                return render(self.request, 'registration/admin-account/send_active.html')
            else:
                # if is_active eq to true
                # we save user and reverse to success page
                user.save()
                return render(self.request, 'registration/admin-account/user_creation.html')
        # if user is access
        elif self.request.user.is_access:
            # by default we is_active eq to false
            # if is_active is false user can't login and do can't anything to site
            user.is_active = False
            # save user
            user.save()
            # get current domain url
            current_site = get_current_site(self.request)
            # mail subject
            mail_subject = 'Activate Your Account'
            # message, we use render to string to html file to string for sending email
            message = render_to_string('email-confirmation/email_template.html', {
                # get user
                'user': user,
                # get current site url
                'domain': current_site.domain,
                # create a uid
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                # create a token for this user
                'token':account_activation_token.make_token(user),
            })
            # send email for email in registration form
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                        # create a instance for send email
                        mail_subject, message, to=[to_email]
            )
            # sending email
            email.send()
            # reverse to "confirmation send" page
            return render(self.request, 'registration/admin-account/send_active.html')
    # success url
    success_url = reverse_lazy('login')
    # template name
    template_name = 'registration/admin-account/user_add.html'

# update user views
class UserUpdate(LoginRequiredMixin, GetAccessMixin, UpdateUserFormMixin, UpdateView):
    # our model
    model = User
    # success url
    success_url = reverse_lazy('account:user_list')

# delete user view
class UserDelete(LoginRequiredMixin, UserDeleteAccessMixin, DeleteView):
    # our model
    model = User
    # success url
    success_url = reverse_lazy('account:user_list')
    # template name
    template_name = 'registration/admin-account/user_confirm_delete.html'

# make a Profile View for show user profile
class Profile(LoginRequiredMixin, UpdateView):
    # our model
    model = User
    # template name
    template_name = 'profile/profile.html'
    # success url
    success_url = reverse_lazy('books:index')
    # our fields for update
    fields = ['username', 'email', 'phone', 'avatar','first_name', 'last_name']
    # get user object
    def get_object(self):
        # return User
        self.user = User.objects.get(pk = self.request.user.pk) 
        self.user_email = self.user.email
        return self.user
    # validate form
    def form_valid(self, form):
        # we are save user with commit false if commit false you can change anything to the object and save it later
        user = form.save(commit=False)
        # if superuser or access change email without confirmation
        if self.request.user.is_superuser:
            user.is_active = True
            user.save()
        else:
        # check if email eq to email user or not
            if not user.email == self.user_email:
                # user activation to false if active is false user cant login and work to the site
                self.user.is_active = False
                # we save user with is_active eq to false
                self.user.save()
                # get current site url
                current_site = get_current_site(self.request)
                # subject for send mail
                mail_subject = 'Activate Your Account'
                # our message, im use render to string a html file
                # it give an html file and renders to string for send to user
                message = render_to_string('email-confirmation/email_template.html', {
                    # get current user
                    'user': self.user,
                    # our domain we get in in current_site
                    'domain': current_site.domain,
                    # make a uid for token with user.pk
                    'uid':urlsafe_base64_encode(force_bytes(self.user.pk)),
                    # create token only for this user
                    'token':account_activation_token.make_token(self.user),
                })
                # send email for user email in registration page
                to_email = form.cleaned_data.get('email')
                # send email with Email Message
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                # send email
                email.send()
                # render page to confirmation send
                return render(self.request, 'email-confirmation/email_send_login.html')

        return super().form_valid(form)
