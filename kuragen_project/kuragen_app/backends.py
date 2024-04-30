from django.contrib.auth.backends import ModelBackend
from .models import Member

class MemberAuthBackend(ModelBackend):
    def authenticate(self, request, name=None, password=None, **kwargs):
        try:
            member = Member.objects.get(name=name)
        except Member.DoesNotExist:
            return None
        else:
            if member.check_password(password and self.user_can_authenticate(member)):
                return member