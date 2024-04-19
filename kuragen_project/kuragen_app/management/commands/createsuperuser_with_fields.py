from django.core.management.base import BaseCommand
from kuragen_app.models import Member, Position

class Command(BaseCommand):
    help = 'Create superuser with additional fields'

    def handle(self, *args, **options):
        name = input('Name: ')
        generation = input('Generation: ')
        position_id = input('Position (Position.id): ')
        password = input('Password: ')
        confirm_password = input('Password (again): ')

        if password != confirm_password:
            self.stdout.write(self.style.ERROR('Passwords do not match'))
            return
        
        try:
            position = Position.objects.get(pk=position_id)
        except Position.DoesNotExist:
            self.stdout.write(self.style.ERROR('Position with provided ID does not exist'))
            return

        Member.objects.create_superuser(name=name, generation=generation, position=position, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))