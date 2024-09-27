from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être renseigné")
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            username = username.strip(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')

        return self.create_user(username=username, email=email, password=password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=255,
        help_text='Obligatoire. 255 caractères ou moins. Lettres, chiffres et espaces uniquement',
        verbose_name="Nom d'utilisateur"
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text='Obligatoire. 255 caractères ou moins. Lettres, chiffres, @ uniquement',
        verbose_name='Email'
    )

    is_active = models.BooleanField(
        default=True,
        help_text="L'utilisateur est actif",
        verbose_name='Est actif'
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Est un super utilisateur",
        verbose_name='Est un superuser'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Fait parti de l'équipe d'administration",
        verbose_name='Est un admin'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name='Utilisateur'

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=255,
        help_text='Le titre doit être brêf',
        verbose_name='Titre'
    )
    details = models.TextField(
        help_text='Donnez des détails de votre tache',
        verbose_name='Details'
    )
    date = models.DateTimeField(
        help_text='La date de création de la tache',
        default=timezone.now,
        verbose_name='Date de création'
    )

    def __str__(self):
        return self.title


