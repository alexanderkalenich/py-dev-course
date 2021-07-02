# -*- coding: utf-8 -*-

from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import db_session, rollback

import settings
from bot import Bot

from vk_api.bot_longpoll import VkBotMessageEvent
from freezegun import freeze_time
import datetime

from generate_ticket import generate_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper

class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1603567441, 'from_id': 573716757, 'id': 93, 'out': 0, 'peer_id': 573716757,
                               'text': 'Привет, бот!', 'conversation_message_id': 92, 'fwd_messages': [],
                               'important': False,
                               'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info':
                       {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'], 'keyboard': True,
                        'inline_keyboard': True, 'carousel': False, 'lang_id': 0}},
        'group_id': 199401315,
        'event_id': '3d8e1dbfbdee8b438b6f8fdcbc498c879e2db4b1'}


    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        '/help',
        'какие направления?',
        '/ticket',
        'Москва',
        'Лондон',
        '05-06-2021',
        'ok',
        '1',
        '1',
        'Два обеда',
        'да',
        '+79225555555',
        'Иванов',
        'ivanov@gmail.com',
    ]
    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'],
        settings.SCENARIOS['registration']['steps']['step4']['text'],
        settings.SCENARIOS['registration']['steps']['step5']['text'].format(list_of_flights=
                            '1:  Москва – Лондон: 5-6-2021 вылет 17:30; '
                            '2:  Москва – Лондон: 12-6-2021 вылет 17:30; '
                            '3:  Москва – Лондон: 19-6-2021 вылет 17:30; '
                            '4:  Москва – Лондон: 26-6-2021 вылет 17:30; '
                            '5:  Москва – Лондон: 10-7-2021 вылет 17:30'),
        settings.SCENARIOS['registration']['steps']['step6']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['text'],
        settings.SCENARIOS['registration']['steps']['step8']['text'].format(flight_number=
                            ' Москва – Лондон: 5-6-2021 вылет 17:30',
                            number_of_seats='1', comment='Два обеда'),
        settings.SCENARIOS['registration']['steps']['step9']['text'],
        settings.SCENARIOS['registration']['steps']['step10']['text'],
        settings.SCENARIOS['registration']['steps']['step11']['text'],
        settings.SCENARIOS['registration']['steps']['step12']['text'].format(name='Иванов', email='ivanov@gmail.com',
                            flight_number='Москва – Лондон: 5-6-2021 вылет 17:30', number_of_seats='1')

    ]

    @isolate_db
    @freeze_time("2021-06-05")
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

        assert datetime.datetime.now() == datetime.datetime(2021, 0o6, 0o5)

    def test_image_generation(self):
        ticket_file = generate_ticket('Иванов', 'ivanov@gmail.com', 'Москва – Лондон: 5-6-2021 вылет 17:30', '1')
        with open("files/ticket_test.png", 'rb') as expected_file:
            expected_bytes = expected_file.read()
        assert ticket_file.read() == expected_bytes
