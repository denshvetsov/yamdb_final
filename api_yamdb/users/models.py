import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField('email address', blank=False, unique=True)
    role = models.CharField(
        'Роль', max_length=9, choices=ROLE_CHOICES, default=USER,
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )
    confirmation_code = models.UUIDField(default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username
