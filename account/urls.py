from django.contrib.auth import views
from django.urls import path
from .views import CreateUser, BookList, BookDelete, BookSearch, BookCreate, BookUpdate, UserList, UserCreate, UserUpdate, UserDelete, UserSearch, PasswordChangeView, PasswordChangeDoneView

# set app name for our account urls
app_name = 'account'

# add our urls

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


urlpatterns += [
    path('book/book_list/', BookList.as_view(), name='book_list'),
    path('book/book_search/', BookSearch.as_view(), name='book_search'),
    path('book/book_delete/<slug:slug>', BookDelete.as_view(), name='book_delete'),
    path('book/book_create/', BookCreate.as_view(), name='book_create'),
    path('book/book_update/<slug:slug>/', BookUpdate.as_view(), name='book_update'),
    path('user/user_list/', UserList.as_view(), name='user_list'),
    path('user/user_search/', UserSearch.as_view(), name='user_search'),
    path('user/user_create/', UserCreate.as_view(), name='user_create'),
    path('user/user_update/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('user/user_delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
    path('password_change', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),
]