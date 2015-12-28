from django.contrib.auth.models import User
User.objects.create_superuser(username='admin', password='admin', email='') 
