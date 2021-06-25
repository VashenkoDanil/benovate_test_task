from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import User


class MoneyTransferHistoryViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            'user1',
            email='user1@test.com',
            password='testing',
            inn='111',
            score=1000
        )
        self.user2 = User.objects.create_user(
            'user2',
            email='user2@test.com',
            password='testing',
            inn='222',
            score=0
        )
        self.user3 = User.objects.create_user(
            'user3',
            email='user3@test.com',
            password='testing',
            inn='333',
            score=0
        )

    def test_money_transfer_history_url(self):
        path = reverse('money_transfer_history-list')
        self.assertEqual(path, '/user/money-transfer-history/')

    def test_successful_money_transfer(self):
        user1 = User.objects.get(id=self.user1.id)
        self.assertEqual(user1.score, Decimal(1000))
        user2 = User.objects.get(id=self.user2.id)
        self.assertEqual(user2.score, Decimal(0))

        data = {
            'sender': self.user1.id,
            'amount_to_transfer': 100,
            'inn_recipient': self.user2.inn
        }
        response = self.client.post(reverse('money_transfer_history-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user1 = User.objects.get(id=self.user1.id)
        self.assertEqual(user1.score, Decimal(900))
        user2 = User.objects.get(id=self.user2.id)
        self.assertEqual(user2.score, Decimal(100))

    def test_successful_money_transfer_with_remainder(self):
        data = {
            'sender': self.user1.id,
            'amount_to_transfer': 100,
            'inn_recipient': f'{self.user1.inn}, {self.user2.inn}, {self.user3.inn}'
        }
        response = self.client.post(reverse('money_transfer_history-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user1 = User.objects.get(id=self.user1.id)
        self.assertEqual(user1.score, Decimal('933.34'))
        user2 = User.objects.get(id=self.user2.id)
        self.assertEqual(user2.score, Decimal('33.33'))
        user3 = User.objects.get(id=self.user3.id)
        self.assertEqual(user3.score, Decimal('33.33'))

    def test_not_validate_money_transfer(self):
        response = self.client.post(reverse('money_transfer_history-list'), data={
            'sender': self.user1.id,
            'amount_to_transfer': 10000,
            'inn_recipient': [self.user2.inn]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'amount_to_transfer': ['У пользователя недостаточно средств']})

        response = self.client.post(reverse('money_transfer_history-list'), data={
            'sender': self.user1.id,
            'amount_to_transfer': 10000,
            'inn_recipient': f'123456, 123445'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'inn_recipient': ['В базе данных по указанным инн не было найдено не одного пользователя']}
        )
