from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    inn = models.CharField(max_length=20, null=True, verbose_name='ИНН')
    score = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='Счет')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class MoneyTransferHistory(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='senders', verbose_name='Отправитель')
    recipient = models.ManyToManyField(User, related_name='recipients', verbose_name='Получатель')
    amount_to_transfer = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Сумма для перевода')

    class Meta:
        verbose_name = 'История перевода'
        verbose_name_plural = 'История переводов'

    def __str__(self):
        return f'{self.sender.username} ({self.amount_to_transfer})'
