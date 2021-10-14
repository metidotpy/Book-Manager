from django.urls import path
from . import views

app_name = 'books'

handler404 = 'books.views.handler404'
handler403 = 'books.views.handler403'
handler400 = 'books.views.handler400'
handler500 = 'books.views.handler500'

urlpatterns = [
    path('', views.BookList.as_view(), name='index'),
    path('<int:page>', views.BookList.as_view(), name='index'),
    path('book/<slug:slug>', views.BookDetail.as_view(), name='details'),
    path('update/<slug:slug>', views.BookUpdate.as_view(), name='update'),
    path('create/', views.BookCreate.as_view(), name='create'),
    path('unread/', views.BookFalse.as_view(), name='unread'),
    path('unread/<int:page>', views.BookFalse.as_view(), name='unread'),
    path('read/', views.BookTrue.as_view(), name='read'),
    path('read/<int:page>', views.BookTrue.as_view(), name='read'),
    path('random/', views.BookRandom.as_view(), name='random'),
    path('random/<int:page>', views.BookRandom.as_view(), name='random'),
    path('true/<slug:slug>', views.true_book, name='true'),
    path('false/<slug:slug>', views.false_book, name='false'),
    path('delete/<slug:slug>', views.BookDelete.as_view(), name='delete'),
]