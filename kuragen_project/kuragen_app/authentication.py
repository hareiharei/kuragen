from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomBackend(ModelBackend):
    def authenticate(self, request, name=None, password=None, **kwargs):
        Member = get_user_model()
        try:
            member = Member.objects.get(name=name)
            if member.check_password(password):
                return member
        except Member.DoesNotExist:
            return None
    
    def get_member(self, member_id):
        Member = get_user_model()
        try:
            return Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return None