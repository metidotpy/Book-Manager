from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
import six

# create token for out confirmation email
# for this thing we user as PasswordResetTokenGenerator for generate a token for every user
class TokenGenerator(PasswordResetTokenGenerator):
    # make a hash value with our user and a timestamp for expiration
    def _make_has_value(self, user, timestamp):
        # return our token
        return (
            six.text_type(user.pk) + six.text_type(timestamp)+
            six.text_type(user.is_active)
        )

# make an instance from our TokenGenerator class
account_activation_token = TokenGenerator()