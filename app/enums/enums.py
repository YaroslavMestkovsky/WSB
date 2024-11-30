import win32con


class KeysEnum:
    """Кнопки и клавиши, которые будем клацать."""

    HOLD = 0
    LOOSE = 1

    LEFT = {
        HOLD: [win32con.WM_KEYDOWN, win32con.VK_LEFT, 0],
        LOOSE: [win32con.WM_KEYUP, win32con.VK_LEFT, 0],
    }
    RIGHT = {
        HOLD: [win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0],
        LOOSE: [win32con.WM_KEYUP, win32con.VK_RIGHT, 0],
    }
    UP = {
        HOLD: [win32con.WM_KEYDOWN, win32con.VK_UP, 0],
        LOOSE: [win32con.WM_KEYUP, win32con.VK_UP, 0],
    }
    DOWN = {
        HOLD: [win32con.WM_KEYDOWN, win32con.VK_DOWN, 0],
        LOOSE: [win32con.WM_KEYUP, win32con.VK_DOWN, 0],
    }
    L_CLIK = {
        HOLD: [win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON],
        LOOSE: [win32con.WM_LBUTTONUP, None],
    }
    R_CLIK = {
        HOLD: [],
        LOOSE: [],
    }
