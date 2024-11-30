import unittest

import numpy as np

from FollowBot import Bot


class TestBot(unittest.TestCase):
    """"""
    bot = Bot()

    def test_bot_initialisation(self):

        assert self.bot.window_name is not None, "#1 Имя окна не указано в настройках!"
        assert self.bot.hwnd is not None, "#1 Окно не найдено!"

        print('Бот инициализирован, всё в порядке.')
