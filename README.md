### Тескт задания

Напишите код приложения для Django (Python 3), в котором у пользователей (пользователей в системе может быть очень много) есть помимо основных полей 2 дополнительных: ИНН (уникально, ИНН может начинаться с нуля) и счет (в рублях, с точностью до копеек). Также есть форма состоящая из полей (в приоритете  использование REST API или же чистый Django):

- Выпадающий список со всеми пользователями в системе с возможностью выбора пользователя, со счета которого нужно перевести деньги
- Поле для ввода одного или нескольких ИНН пользователей, на счета которых будут переведены деньги
- Поле для указания какую сумму нужно перевести с одного счета на другие

Необходимо проверять есть ли достаточная сумма у пользователя, со счета которого списываются средства, и есть ли пользователи с указанным ИНН в БД. При валидности введенных данных необходимо указанную сумму списать со счета указанного пользователя и перевести на счета пользователей с указанным ИНН в равных частях (если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет).



*Обязательно наличие unit-тестов.*

*Требуется реализовать только бэк. Фронт и шаблоны можно не настраивать.*

*Код в приватном репозитории.*
