from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from account.models import User
from django.utils.crypto import get_random_string
import string
import uuid


# Create your models here.

# create book model
class BookModel(models.Model):
    # this is book name field
    # [max_length: it mean you can just write 100 charachter in this field]
    book_name = models.CharField(max_length=100)

    # this is book slug
    # its create a random unique string for slug
    # [default: it mean make a default value for this field]
    # [max_length: it mean you can just write 8 charachter in this field]
    # [unique: it say this fields should be unique item]
    book_slug = models.SlugField(default = uuid.uuid4().hex[:6].lower(), max_length=8, unique=True)
    # this is book write field
    # [max_length: it mean you can just write 100 charachter in this field]
    book_writer = models.CharField(max_length=100)
    # this is book description
    book_description = models.TextField()
    # this is book image
    # [upload_to: it mean upload this image to path]
    book_image = models.ImageField(upload_to='images')
    # this is book author, it's a foreign key from User model
    # [on_delete: it mean if this user object deleted delete books from this user]
    book_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    # this is save book date time
    # [default: it mean make a default value for this field]
    # timezone.now eq to now datetime
    book_datetime = models.DateTimeField(default=timezone.now)
    # this is save readest book
    # [default: it mean make a default value for this field]
    # [verbose_name: it mean make a name for this field]
    book_status = models.BooleanField(default=False, verbose_name='Are You Read That Book?')
    # if object created add now
    created = models.DateTimeField(auto_now_add=True)
    # if object updated make now value
    updated = models.DateTimeField(auto_now=True)

    # meta class
    class Meta:
        # order objects with book_status, pk, book_name
        ordering = ['-book_status', 'pk', 'book_name']

    # send image for admin panel
    def get_image(self):
        # return image html
        return format_html('<img src="{}" width="30" style="border-radius:50%;" />'.format(self.book_image.url))

    # str object
    def __str__(self):
        # return book_name for str method
        return self.book_name