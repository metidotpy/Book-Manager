from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from random import randint
import os
from django.utils.html import format_html

# split ext for filepath
def split_ext(file):
    # base name
    base_name = os.path.basename(file)
    # name and ext
    name, ext = os.path.splitext(base_name)
    # return ext and name
    return name, ext
# get upload path for save a avatar
def upload_path(instance, filepath):
    # name and ext
    name, ext = split_ext(filepath)
    # new name for random number
    new_name = randint(0, 999999999)
    # final name for path
    final_path = f"avatar/{instance.username}/{instance.id}/{new_name}{ext}"
    # return final path
    return final_path



# Create your models here.

#custom user model
#its for your custom fields or changing another fields in User model
class User(AbstractUser):
    # this is a regex for (Iran Mobile Number) Validation
    PhoneValid = RegexValidator(regex = r'^(?:98|\+98|0098|0)?9[0-9]{9}$', message = 'Phone Is Not Good')
    # this is (Phone Number) field, this field have
    # [max_length: it mean you can just write 14 charachter in this field],
    # [validator: for Validations Phone Number With our Regex Mobile Number Validator],
    # [verbose_name: for a name for show label in everywhere],
    # [unique: it say this fields should be unique item]
    phone = models.CharField(validators = [PhoneValid], max_length= 14, verbose_name='Phone Number', unique=True)
    # this field for get acces to user
    # if user have this access, he/she can be your admin
    # [default: the default for this field is False]
    is_access = models.BooleanField(default=False)
    # i am changing the main first_name to this first_name
    first_name = models.CharField(_('first name'), max_length=150)
    # i am changing the main last_name to this last_name
    last_name = models.CharField(_('last name'), max_length=150)
    # i am changing the main email to this email
    email = models.EmailField(_('email address'), unique=True)

    # set a profile image for user
    # [default: the default for this field is default.png]
    # [upload_to: it mean upload this image to path]
    avatar = models.ImageField(default = 'avatar/default.png', upload_to = upload_path)


    # this fields is required for compeleting
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name', 'email']
    # out email field
    EMAIL_FIELD = 'email'

    class Meta:
        # order items
        ordering = ['-is_superuser', '-is_access', '-is_active', 'pk']
    
    # send image for admin panel
    def get_avatar(self):
        # return image html
        return format_html('<img src="{}" width="30" style="object-fit: cover;border-radius:50%;" />'.format(self.avatar.url))