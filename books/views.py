from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls.base import reverse
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView, TemplateView
from .models import BookModel
from django.urls import reverse_lazy
from .mixins import SetAuthorMixin, AuthorMixin, GetAuthor
import random
import uuid
from account.forms import PasswordChangeForm
from account.models import User

# Create your views here.

# handle 404 error
def handler404(request, exception):
    return render(request, '404.html')
# handle 403 error
def handler403(request, exception):
    return render(request, '403.html')
# handle 400 error
def handler400(request, exception):
    return render(request, '400.html')
# handle 500 error
def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)


# book list view
class BookList(LoginRequiredMixin, ListView):
    # get queryset
    def get_queryset(self):
        # return book objects if author eq to request user
        return BookModel.objects.filter(book_author = self.request.user)
    # template name
    template_name = 'books/all_books.html'
    # make paginate
    paginate_by = 5
    # get user object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# false book list
class BookFalse(LoginRequiredMixin, ListView):
    # get queryset
    def get_queryset(self):
        # return book objects if author eq to request user and false book_status
        return BookModel.objects.filter(book_author=self.request.user, book_status=False)
    # template name
    template_name = 'books/unread_books.html'
    # make paginate
    paginate_by = 5
    # get user object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# true book list
class BookTrue(LoginRequiredMixin, ListView):
    # get queryset
    def get_queryset(self):
        # return book objects if author eq to request user and true book_status
        return BookModel.objects.filter(book_author=self.request.user, book_status=True)
    # template name
    template_name = 'books/read_books.html'
    # make paginate
    paginate_by = 5
    # get user object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# random false book list
class BookRandom(LoginRequiredMixin, ListView):
    # get queryset
    def get_queryset(self):
        # get list from book model
        # book objects if author eq to request user and false book_status
        item_list = list(BookModel.objects.filter(book_author=self.request.user, book_status=False))
        # if len item biggest 5
        if len(item_list) >= 5:
            # return 5 random item from item_list
            return random.sample(item_list, 5)
        # else
        else:
            # return len item list random book
            return random.sample(item_list, len(item_list))            
    # template name
    template_name = 'books/random_books.html'
    # make paginate
    paginate_by = 5
    # get user object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# create book view
class BookCreate(LoginRequiredMixin, SetAuthorMixin, CreateView):
    # make form validation
    def form_valid(self, form):
        # save form, commit false, if commit false you can edit object
        obj = form.save(commit=False)
        # slug a unique slug
        obj.book_slug = uuid.uuid4().hex[:6].lower()
        obj.book_author = self.request.user
        # save
        obj.save()
        return super().form_valid(form)


    # our model
    model = BookModel
    # our fields
    fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status']
    # template name
    template_name = 'books/insert-book/insert_book.html'
    # success_url
    success_url = reverse_lazy('books:index')

# update book view
class BookUpdate(LoginRequiredMixin, GetAuthor, UpdateView):
    # our model
    model = BookModel
    # our fields
    fields = ['book_name', 'book_writer', 'book_description', 'book_image', 'book_status']
    # use slug instead pk
    slug_field = 'book_slug'
    # template name
    template_name = 'books/insert-book/insert_book.html'
    # success url
    success_url = reverse_lazy('books:index')

# delete book view
class BookDelete(LoginRequiredMixin, DeleteView):
    # our model
    model = BookModel
    # use slug instead pk
    slug_field = 'book_slug'
    # success url
    success_url = reverse_lazy('books:index')
    # template name
    template_name = 'books/delete-templates/book_confirm_delete.html'

# detail book view
class BookDetail(LoginRequiredMixin, AuthorMixin, DetailView):
    # get object from book model
    def get_object(self):
        # slug eq to kwargs.slug
        slug = self.kwargs.get('slug')
        # get object or 404 from Book Model
        book = get_object_or_404(BookModel, book_slug = slug, book_author = self.request.user)

        # return book
        return book
    # template name
    template_name = 'books/details/details.html'

# password change view for users
class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    # get template name
    template_name = 'registration/password_change_form.html'
    # if success go to done
    success_url = reverse_lazy('books:password_change_done')
    # form class
    form_class = PasswordChangeForm

# change PasswordChangeDoneView for users
class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    # template name
    template_name = 'registration/password_change_done.html'

# make true books
def true_book(request, slug):
    # get book
    book = BookModel.objects.get(book_slug = slug)
    # book_status eq to true
    book.book_status = True
    # save book
    book.save()
    # redirect to home
    return redirect(reverse_lazy('books:index'))

# make false book
def false_book(request, slug):
    # get book
    book = BookModel.objects.get(book_slug = slug)
    # book_status eq to false
    book.book_status = False
    # save book
    book.save()
    # redirect to home
    return redirect(reverse_lazy('books:index'))


