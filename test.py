import ctypes

# import win32api
# PROCESS_PER_MONITOR_DPI_AWARE = 2
# MDT_EFFECTIVE_DPI = 0
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
from ctypes import windll

def get_ppi():
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    user32 = windll.user32
    user32.SetProcessDPIAware()
    dc = user32.GetDC(0) 
    pix_per_inch = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
    print("Horizontal DPI is", windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX))
    print("Vertical DPI is", windll.gdi32.GetDeviceCaps(dc, LOGPIXELSY))
    user32.ReleaseDC(0, dc)
    return pix_per_inch

get_ppi()

# def print_dpi():
#     shcore = ctypes.windll.shcore
#     monitors = win32api.EnumDisplayMonitors()
#     hresult = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
#     assert hresult == 0
#     dpiX = ctypes.c_uint()
#     dpiY = ctypes.c_uint()
#     for i, monitor in enumerate(monitors):
#         shcore.GetDpiForMonitor(
#             monitor[0].handle,
#             MDT_EFFECTIVE_DPI,
#             ctypes.byref(dpiX),
#             ctypes.byref(dpiY)
#         )
#         print(
#             f"Monitor {i} (hmonitor: {monitor[0]}) = dpiX: {dpiX.value}, dpiY: {dpiY.value}"
#         )
# if __name__ == "__main__":
#     print_dpi()

# from windowcapture import WindowCapture
# import cv2 as cv
# wincap = WindowCapture("Bluestacks App Player")

# while True:
#     screenshot = wincap.get_screenshot()

#     cv.imshow("screenshot",screenshot)

#     key = cv.waitKey(1)
#     if key == ord('q'):
#         cv.destroyAllWindows()
#         break

import tkinter
root = tkinter.Tk()
dpi = root.winfo_fpixels('1i')
print(f"tkinter: {dpi}")
