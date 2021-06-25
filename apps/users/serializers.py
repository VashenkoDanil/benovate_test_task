from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from apps.users.models import MoneyTransferHistory, User


class MoneyTransferHistorySerializer(serializers.ModelSerializer):
    inn_recipient = serializers.CharField(max_length=500, write_only=True, help_text='Список инн через запятую',
                                          label='ИНН получателей')

    class Meta:
        model = MoneyTransferHistory
        fields = ['id', 'sender', 'recipient', 'amount_to_transfer', 'inn_recipient']
        write_only_fields = ('id',)
        read_only_fields = ('recipient',)

    def validate_inn_recipient(self, inn_recipient):
        users = self._get_users_by_inn(inn_recipient)
        if len(users) < 1:
            raise serializers.ValidationError('В базе данных по указанным инн не было найдено не одного пользователя')
        return inn_recipient

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get('amount_to_transfer') > attrs.get('sender').score:
            raise serializers.ValidationError({'amount_to_transfer': 'У пользователя недостаточно средств'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        amount_to_transfer = validated_data.get('amount_to_transfer')
        sender = validated_data.get('sender')

        users = self._get_users_by_inn(validated_data.get('inn_recipient'))

        count_users = len(users)
        portion_each_user = self._calculated_portion_each_user(count_users, amount_to_transfer)
        real_amount_transfer = count_users * portion_each_user

        users.update(score=F('score') + portion_each_user)
        if sender in users:
            users.filter(id=sender.id).update(score=F('score') - real_amount_transfer)
        else:
            sender.score = sender.score - real_amount_transfer
            sender.save()

        return super().create({
            'sender': validated_data.get('sender'),
            'recipient': list(users),
            'amount_to_transfer': real_amount_transfer
        })

    def _calculated_portion_each_user(self, count_users: int, amount_to_transfer: Decimal):
        if count_users > 1:
            return (amount_to_transfer / count_users).quantize(Decimal('.01'), rounding='ROUND_DOWN')
        else:
            return amount_to_transfer

    def _get_users_by_inn(self, inn_recipient: str):
        inn_list = [
            inn.strip() for inn in inn_recipient.split(',')
        ]
        return User.objects.filter(inn__in=inn_list)
