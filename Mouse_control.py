from matplotlib.pyplot import flag
import pyautogui
import numpy as np

class Mouse_control:
    '''
    1. Double_Left_mouse
    2. Left_mouse
    3. Long_press_mouse
    4. Move_mouse
    5. Right_mouse
    6. Scroll_mouse
    '''

    w_screen, h_screen = pyautogui.size()
    flag = False
    grabflag = False
    prev_center = None
    prev_y = 0

    def __init__(self, cam_size=(640, 480), frameR = 100):
        self.w_cam, self.h_cam = map(int, cam_size)
        self.frameR = frameR
    
    def get_position(self, center):
        x = np.interp(center[0], (self.frameR, self.w_cam), (0, self.w_screen))
        y = np.interp(center[1], (self.frameR, self.h_cam), (0, self.h_screen))
        return (x, y)

    def mouse(self, target, center):
        x, y = self.get_position(center)

        if target != 3 and Mouse_control.grabflag:
            Mouse_control.grabflag = False
            pyautogui.mouseUp(button='left')

        if target == 1 and Mouse_control.flag:
            pyautogui.doubleClick(button='left')
            Mouse_control.flag = False

        elif target == 2 and Mouse_control.flag:
            pyautogui.click(button='left')
            Mouse_control.flag = False

        elif target == 3:
            if not Mouse_control.grabflag:
                Mouse_control.grabflag = True
                pyautogui.mouseDown(button='left')
            pyautogui.moveTo(x, y, 0.1)

        elif target == 4:
            pyautogui.moveTo(x, y, 0.1)
            Mouse_control.flag = True

        elif target == 5 and Mouse_control.flag:
            pyautogui.click(button='right')
            Mouse_control.flag = False

        elif target == 6 and Mouse_control.flag:
            pyautogui.scroll((y - Mouse_control.prev_y)*10)
            Mouse_control.flag = False
            Mouse_control.prev_y = y