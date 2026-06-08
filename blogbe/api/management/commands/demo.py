from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    info = "Create demo account"

    def handle(self, *args, **kwargs):
        users = [
            {
                "email":"admin@ex.com",
                "username":"admin",
                "answer":"Example",
                "password":"Qwerty123!",
                "is_staff":True,
                "is_superuser":True,
                "is_demo":True
            },
            {
                "email":"user1@ex.com",
                "username":"user1",
                "answer":"Test",
                "password":"Qwerty321!",
                "is_staff":False,
                "is_superuser":False,
                "is_demo":True
            },
            {
                "email":"user2@ex.com",
                "username":"user2",
                "answer":"Animal",
                "password":"Qwerty111!",
                "is_staff":False,
                "is_superuser":False,
                "is_demo":True
            },
        ]

        for data in users:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username":data["username"],
                    "answer": data["answer"],
                    "is_staff":data["is_staff"],
                    "is_superuser":data["is_superuser"],
                    "is_demo":data["is_demo"]
                },
            )
            user.username = data["username"]
            user.answer = data["answer"]
            user.is_staff = data["is_staff"]
            user.is_superuser = data["is_superuser"]
            user.is_demo = data["is_demo"]


            user.set_password(data["password"])
            user.save()

            status = "created" if created else "updated"
            self.stdout.write(f"{data['email']} {status}")