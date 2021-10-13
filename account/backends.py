from django.contrib.auth.backends import ModelBackend
from .models import User

# write this class for authenticate users by email and username
class EmailModelBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        # if '@' in our user name field
        if '@' in username:
            # emial is username field for authenticate our user
            kwargs = {'email': username}
        
        # if our username fields starts with (09, +98, 0098, 9)
        elif username.startswith('09') or username.startswith('+98') or username.startswith('0098') or username.startswith('9'):
            # phone is username field for authenticate our user
            kwargs = {'phone': username}
        
        # then if conditionals up eq to False
        else:
            # username is fields for authenticateusers
            kwargs = {'username' : username}

        # if password eq to None
        if password is None:
            #return None for user
            return None
        try:
            # try to get user for authenication
            user = User.objects.get(**kwargs)
        # if user doesn't exists
        except User.DoesNotExist:
            # pass, go away
            pass

        else:
            # and if else and password eq to user password and can be authenticate
            if user.check_password(password) and self.user_can_authenticate(user):
                # return user for login
                return user