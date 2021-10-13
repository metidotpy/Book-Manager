from django.contrib import admin
from .models import BookModel

# disable delete action in admin panel
admin.site.disable_action('delete_selected')

# all make read in admin panel
def make_read(modeladmin, request, queryset):
    # how much rows is updated
    rows_updated = queryset.update(book_status = True)
    # if rows updated eq to one we want to say one book
    if rows_updated == 1:
        message_bit = 'One Book'
    # else we want to say {rows_updated} number
    else:
        message_bit = '{} Books'.format(rows_updated)
    # return this message
    return modeladmin.message_user(request, '{} Updated.'.format(message_bit))

# create a short description for make_read function
make_read.short_description='Make True All Book Statuses'

# all make unread in admin panel
def make_unread(modeladmin, request, queryset):
    # how much rows is updated
    rows_updated = queryset.update(book_status = False)
    # if rows updated eq to one we want to say one book
    if rows_updated == 1:
        message_bit = 'One Book'
    # else we want to say {rows_updated} number
    else:
        message_bit = '{} Books'.format(rows_updated)
    # return this message
    return modeladmin.message_user(request, '{} Updated.'.format(message_bit))
# create a short description for make_unread function
make_unread.short_description='Make False All Book Statuses'


# Register your models here.

# create admin model for our model
class BookAdmin(admin.ModelAdmin):
    # create list_display for showing this fields to admin panel
    list_display = (
        'book_name',
        'book_slug',
        'book_writer',
        'get_image',
        'book_author',
        'book_status',
    )
    # add our action to the admin panel
    actions =  [make_read, make_unread]
# register model BookModel and BookAdmin
admin.site.register(BookModel, BookAdmin)