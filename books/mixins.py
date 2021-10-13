from account.models import User
from .models import BookModel
from django.shortcuts import get_object_or_404
from django.http import Http404
from django import forms

# this mixin set author to user request
class SetAuthorMixin():
    # make form validation
    def form_valid(self, form):
        # save book object with commit false
        # if commit eq to false we can edit object and make some changes
        self.obj = form.save(commit=False)
        # obj book author eq to request user
        self.obj.book_author = self.request.user
        # save object
        self.obj.save()
        return super().form_valid(form)
# this mixin for get book
class AuthorMixin():
    def dispatch(self, request, slug, *args, **kwargs):
        # get book
        book = get_object_or_404(BookModel, book_slug = slug, book_author = request.user)
        # if book author eq to request user return book detail
        if book.book_author == request.user:
            return super().dispatch(request, slug, *args, **kwargs)
        # else raise 404 page
        else:
            raise Http404()

# this mixin for get book for users
class GetAuthor():
    # make a dispatch
    def dispatch(self, request, slug, *args, **kwargs):
        # get book
        book = get_object_or_404(BookModel, book_slug = slug)
        # if book author eq to request user or user is superuser return dispatch
        if book.book_author == request.user or request.user.is_superuser:
            return super().dispatch(request, slug, *args, **kwargs)
        # else raise 404 page
        else:
            raise Http404()

# get field for create book
class GetField():
    # make a dispatch
    def dispatch(self, request, *args, **kwargs):
        # if user is superuser get this fields
        if request.user.is_superuser:
            self.fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status', 'book_author']
        # else get this fields
        else:
            self.fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status']
        return super().dispatch(request, *args, **kwargs)