# -*- coding: utf-8 -*-


TOKEN = "Здесь можно ввести свой токен VK"
GROUP_ID = "Здесь можно ввести GROUP_ID VK"

DEFAULT_ANSWER = 'Вас приветствует компания «Плати-лети». ' \
                 'Предлагаю ознакомиться с информацией, как работает диспетчер: ' \
                 ' 1. Введите город отправления; ' \
                 ' 2. Введите город назначения; ' \
                 ' 3. Введите дату вылета в формате 01-05-2021; ' \
                 ' 4. Выберите рейс и введите соответствующую цифру; ' \
                 ' 5. Укажите количество мест (от 1 до 5); ' \
                 ' 6. Оставьте комментарий в произвольной форме; ' \
                 ' 7. Подтвердите введенную информацию. Если все верно, введите "да", если нет - "нет"; ' \
                 ' 8. Введите номер телефона; ' \
                 ' 9. Получите подтверждение, что с вами свяжутся по введенному номеру; ' \
                 ' 10. Наслаждайтесь перелетом. ' \
                 ' Для поиска рейса и заказа билетов введите: "/ticket". ' \
                 ' Для вызова справки введите: "/help".' \

def_answer = DEFAULT_ANSWER

INTENTS = [
    {
        "name": "Приветствие",
        "tokens": ("здра", "приве", "добр"),
        "scenario": None,
        "answer": def_answer
    },
    {
        "name": "Помощь",
        "tokens": ("помощь", "справка", "/help"),
        "scenario": None,
        "answer": def_answer
    },
    {
        "name": "Регистрация",
        "tokens": "/ticket",
        "scenario": "registration",
        "answer": None
    }
]

SCENARIOS = {
    "registration": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Введите город отправления. Варианты городов, из которых есть рейсы: Москва, Лондон, Париж, "
                        "Екатеринбург, Торонто",
                "failure_text": "Варианты городов, из которых есть рейсы: Москва, Лондон, Париж, "
                                "Екатеринбург, Торонто",
                "handler": "handle_dep_city",
                "next_step": "step2"
            },
            "step2": {
                "text": "Введите город назначения.",
                "failure_text": "Заданное направление не найдено. Введите другой город назначения",
                "handler": "handle_destination_city",
                "next_step": "step3"
            },
            "step3": {
                "text": "Введите дату вылета в формате 01-05-2021.",
                "failure_text": "Во введенной дате ошибка. Попробуйте еще раз",
                "handler": "handle_date",
                "next_step": "step4"
            },
            "step4": {
                "text": f'Введите "ok" для просмотра ближайших рейсов по выбранному направлению',
                "failure_text": "Попробуйте еще раз",
                "handler": "handle_list_of_flights",
                "next_step": "step5"
            },
            "step5": {
                "text": "Выберите рейс и введите соответствующую цифру: {list_of_flights}",
                "failure_text": "Во введенном номере рейса ошибка. Попробуйте еще раз",
                "handler": "handle_flight_number",
                "next_step": "step6"
            },
            "step6": {
                "text": "Укажите количество мест (от 1 до 5).",
                "failure_text": "Указано неверное количество мест. Попробуйте еще раз.",
                "handler": "handle_number_of_seats",
                "next_step": "step7"
            },
            "step7": {
                "text": "Оставьте комментарий в произвольной форме.",
                "failure_text": None,
                "handler": "handle_comment",
                "next_step": "step8"
            },
            "step8": {
                "text": 'Подтвердите введенную информацию: Рейс {flight_number}, '
                        'Количество мест - {number_of_seats}, комментарий - {comment}. '
                        'Если все верно, введите "да", если нет - "нет".',
                "failure_text": 'Вы не подтвердили данные. Попробуйте еще раз или начните заново /ticket',
                "handler": "handle_confirmation",
                "next_step": "step9"
            },
            "step9": {
                "text": "Введите номер телефона в формате +7XXXXXXXXXX.",
                "failure_text": 'Введен неверный номер телефона. Попробуйте еще раз.',
                "handler": "handle_phone",
                "next_step": "step10"
            },
            "step10": {
                "text": "Введите фамилию пассажира",
                "failure_text": 'Фамилия введена неправильно. Попробуйте еще раз.',
                "handler": "handle_name",
                "next_step": "step11"
            },
            "step11": {
                "text": "Введите свой email.",
                "failure_text": 'Введен неверный email. Попробуйте еще раз.',
                "handler": "handle_email",
                "next_step": "step12"
            },
            "step12": {
                "text": "Спасибо за то, что выбрали нас, {name}! Мы также отправили Ваш билет на email {email}.",
                "image": "generate_ticket_handler",
                "failure_text": None,
                "handler": None,
                "next_step": None
            }

        }

    }

}

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    database='vk_chat_bot'
)
