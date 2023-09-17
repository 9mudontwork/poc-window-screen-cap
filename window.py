import win32gui


class Window:
    window_pid = None
    window_react = None

    def __init__(self):
        pass

    def find_window_pid(self, title):
        def callback(hwnd, extra):
            if title in win32gui.GetWindowText(hwnd):
                extra.append(hwnd)

        found_windows = []
        win32gui.EnumWindows(callback, found_windows)

        # check if any windows were found
        if len(found_windows) == 0:
            return None
        else:
            self.window_pid = found_windows[0]
            self.window_react = win32gui.GetWindowRect(self.window_pid)
            return found_windows[0]

    # get real window size
    def get_window_size(self):
        if self.window_react is None:
            return None
        else:
            return (
                self.window_react[2] - self.window_react[0],
                self.window_react[3] - self.window_react[1],
            )
