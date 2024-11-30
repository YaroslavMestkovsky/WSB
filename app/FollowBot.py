import asyncio
import os
import cv2
import win32gui
import yaml
from ultralytics import YOLO

from helpers.helpers import capture_win_frame
from states.bot_states import StateMachine

directory = os.path.dirname(__file__)
config_path = os.path.join(directory, 'config.yml')


class Bot:
    def __init__(self):
        # Флаг остановки
        self.end_loop = False

        # Приложение
        self.hwnd = None
        self.window_name = None

        # Модель
        self.model = None

        # Конфиг
        self.config = None
        self.init_config()
        self.get_hwnd()

        # Стейты
        self.state_machine = StateMachine(self.hwnd, self.model)
        self.main_state = self.state_machine.check
        self.additional_state = self.state_machine.heal

    def init_config(self):
        """Инициализируем конфиг."""

        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self.config = config
        self.window_name = config['hwnd_name']
        model_path = os.path.join(directory, config['model'])
        self.model = YOLO(model_path)

    def get_hwnd(self):
        """Поиск и подключение к окну.
        В будущем их будет много.
        """
        self.hwnd = win32gui.FindWindow(None, self.window_name)

    def get_frame(self):
        """Получение фрейма из окна."""
        return capture_win_frame(self.hwnd)
    
    def check_key_input(self):
        """Ловим нажатие кнопок. Возвращает флаг завершения исполнения.
        Пока что очень грубо выглядит, нужно интерфейс придумать, и тыкать в него мышкой.
        """
        
        end_loot = False
        key = cv2.waitKey(1) & 0xFF
        state = self.state_machine.states.get(key)
        additional_state = self.state_machine.additional_states.get(key)

        if state:
            self.main_state = state
        elif additional_state:
            self.additional_state = additional_state

        if key == ord('q'):
            end_loot = True
            
        return end_loot
        
    async def main_loop(self):
        """Alga!"""

        await asyncio.gather(
            self.run_main_state(),
            self.run_additional_state(),
            self.manage_key_inputs(),
        )

    async def manage_key_inputs(self):
        while True:
            end_loop = self.check_key_input()

            if end_loop:
                  break

            await asyncio.sleep(0.01)

        self.end_loop = True
        cv2.destroyAllWindows()

    async def run_main_state(self):
        while True:
            if self.end_loop:
                break

            frame = self.get_frame()
            await self.main_state.do_thing(frame=frame)


    async def run_additional_state(self):
        while True:
            if self.end_loop:
                break

            frame = self.get_frame()
            await self.additional_state.do_thing(frame=frame)
