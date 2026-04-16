
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # If it's a valid email, get the user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Otherwise, get the user by username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None  # If no user is found, return None

        # Check if the password matches
        if user.check_password(password):
            return user  # Return the user object if password is correct
        return None  # If password doesn't match, return None


        