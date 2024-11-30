import asyncio
import time

import cv2
import torch

from handlers.handlers import InputHandler
from model.classes import ModelClasses


class BaseState:
    """Базовый стейт."""
    def __init__(self, hwnd, model):
        self.hwnd = hwnd
        self.model = model
        self.input_handler = InputHandler(hwnd)

    async def do_thing(self, **kwargs):
        """Делает то, для чего он был предназначен."""

        print(self.__class__)
        await asyncio.sleep(0.01)

    @staticmethod
    def filter_targets(processed_frame, class_name):
        """Фильтруем результат обработки фрейма моделью, оставляя только нужные объекты."""

        for result in processed_frame:
            filtered_boxes = []

            for box in result.boxes.data.tolist():
                _, _, _, _, _, class_id = box

                if int(class_id) == class_name:
                    filtered_boxes.append(box)

            result.boxes.data = torch.tensor(filtered_boxes)

        return processed_frame


class IdleState(BaseState):
    """Стоим ждем."""

    name = 'idle'

    async def do_thing(self, **kwargs):
        pass


class CheckState(BaseState):
    """Проверяем модель."""

    name = 'check'

    async def do_thing(self, **kwargs):
        result = self.model(kwargs.get('frame'), conf=0.45, verbose=False)
        annotated_frame = result[0].plot()
        cv2.imshow("Check detection", annotated_frame)

        await asyncio.sleep(0.01)

class MoveState(BaseState):
    """Ползем куда-то."""

    name = 'move'


class FightState(BaseState):
    """Деремся."""

    name = 'fight'


class LootState(BaseState):
    """Лутаем."""

    name = 'loot'


class HealState(BaseState):
    """Хилим кого-то, по умолчанию - себя."""

    name = 'heal'
    
    async def do_thing(self, **kwargs):
        frame = kwargs.get('frame')
        model_class = kwargs.get('model_class', ModelClasses.SEAMNY)
        model_name = ModelClasses.classes[model_class]

        processed_frame = self.model(frame, conf=0.45, verbose=False)
        filtered_frame = self.filter_targets(processed_frame, model_class)

        result = filtered_frame[0].boxes.data.tolist()

        if result:
            x1, y1, x2, y2, confidence, class_id = result[0]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Вычисление l_param для центра
            l_param = (center_y << 16) | center_x

            self.input_handler.press_key(2)
            self.input_handler.l_click(l_param)

            print(f'HEAL_STATE: healed {model_name}, waiting 15')
            await asyncio.sleep(15) #todo чекать что откатилось?
        else:
            print(f'{model_name} not found')

class TestState(BaseState):
    """Тестим."""

    name = 'test'

    async def do_thing(self, **kwargs):
        frame = kwargs.get('frame')
        processed_frame = self.model(frame, conf=0.45, verbose=False)
        filtered_frame = self.filter_targets(processed_frame, ModelClasses.FAIRY)

        result = filtered_frame[0]
        img_with_boxes = result.plot()
        cv2.imshow("Check detection", img_with_boxes)
        await asyncio.sleep(0.01)


class StateMachine:
    """Стейт-машина."""

    def __init__(self, hwnd, model):
        self.idle = IdleState(hwnd, model)
        self.move = MoveState(hwnd, model)
        self.fight = FightState(hwnd, model)
        self.loot = LootState(hwnd, model)
        self.check = CheckState(hwnd, model)
        self.test = TestState(hwnd, model)
        self.heal = HealState(hwnd, model)

        self.states = {
            ord('i'): self.idle,
            ord('m'): self.move,
            ord('f'): self.fight,
            ord('l'): self.loot,
            ord('c'): self.check,
            ord('t'): self.test,
        }

        self.additional_states = {
            ord('h'): self.heal,
        }
