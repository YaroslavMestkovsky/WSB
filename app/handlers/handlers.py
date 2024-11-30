import win32api
import win32con
from enums.enums import KeysEnum


class InputHandler:
    """Хендлер, цепляющийся к окну, и клацающий кнопки клавиатуры и клавиши мыши."""

    def __init__(self, hwnd):
        self.hwnd = hwnd

    def go_left(self):
        """Топаем влево."""

        win32api.PostMessage(self.hwnd, *KeysEnum.LEFT[KeysEnum.HOLD])
        win32api.PostMessage(self.hwnd, *KeysEnum.LEFT[KeysEnum.LOOSE])

    def go_right(self):
        """Топаем вправо."""

        win32api.PostMessage(self.hwnd, *KeysEnum.RIGHT[KeysEnum.HOLD])
        win32api.PostMessage(self.hwnd, *KeysEnum.RIGHT[KeysEnum.LOOSE])

    def go_up(self):
        """Топаем вверх."""

        win32api.PostMessage(self.hwnd, *KeysEnum.UP[KeysEnum.HOLD])
        win32api.PostMessage(self.hwnd, *KeysEnum.UP[KeysEnum.LOOSE])

    def go_down(self):
        """Топаем вниз."""

        win32api.PostMessage(self.hwnd, *KeysEnum.DOWN[KeysEnum.HOLD])
        win32api.PostMessage(self.hwnd, *KeysEnum.DOWN[KeysEnum.LOOSE])

    def l_click(self, l_param):
        """Клик ЛКМ."""

        win32api.PostMessage(self.hwnd, *KeysEnum.L_CLIK[KeysEnum.HOLD], l_param)
        win32api.PostMessage(self.hwnd, *KeysEnum.L_CLIK[KeysEnum.LOOSE], l_param)

    def r_click(self):
        """Клик ПКМ. Пока вроде не нужно."""
        pass

    def press_key(self, key):
        """Клац по клавише key."""

        key = ord(str(key))

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, 0)
