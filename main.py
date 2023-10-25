import tkinter as tk
from imageRefactorApp import ImageRefactorApp
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRefactorApp(root)
    root.mainloop()


# # import time
# #
# # root = tk.Tk()
# # app = ImageRefactorApp(root)
# # st = time.time()
# # for r in range(256):
# #     for g in range(256):
# #         for b in range(256):
# #             h, s, v = app.convertRGBtoHSV(r, g, b)
# #             if 0 > h >= 360:
# #                 raise Exception("H NIE PASUJE")
# #             if 0 > s > 100 or 0 > v > 100:
# #                 raise Exception("S lub V nie pasuje")
# #             r2, g2, b2 = app.convertHSVtoRGB(h, s, v)
# #             if 0 > r2 > 256 or 0 > g2 > 256 or 0 > b2 > 256:
# #                 raise Exception("R2 lub G2 lub B2 nie pasuje")
# #             if r != r2 or g != g2 or b != b2:
# #                 print(f"STARE RGB ={r} {g} {b}\n NOWE RGB = {r2} {g2} {b2}")
# # end = time.time()
# # timedelta = end - st
# # print(f"Czas: {timedelta}")
#
#
# class RGB:
#     def __init__(self, r, g, b):
#         self.r = r
#         self.g = g
#         self.b = b
#
# class HSV:
#     def __init__(self, h, s, v):
#         self.h = h
#         self.s = s
#         self.v = v
#
# def RGB2HSV(input):
#     output = HSV(None, None, None)
#     min_val = min(input.r, input.g, input.b)
#     max_val = max(input.r, input.g, input.b)
#     delta = max_val - min_val
#     output.v = max_val
#     if delta < 0.00001:
#         output.s = 0
#         output.h = 0
#         return output
#     if max_val > 0.0:
#         output.s = delta / max_val  # s
#     else:
#         output.s = 0.0
#         output.h = float('nan')  # it's now undefined
#         return output
#     if input.r >= max_val:
#         output.h = (input.g - input.b) / delta  # between yellow & magenta
#     elif input.g >= max_val:
#         output.h = 2.0 + (input.b - input.r) / delta  # between cyan & yellow
#     else:
#         output.h = 4.0 + (input.r - input.g) / delta  # between magenta & cyan
#     output.h *= 60.0  # degrees
#     if output.h < 0.0:
#         output.h += 360.0
#     return output
#
# def HSV2RGB(input):
#     hh = input.h
#     if hh >= 360.0:
#         hh = 0.0
#     hh /= 60.0
#     i = int(hh)
#     ff = hh - i
#     p = input.v * (1.0 - input.s)
#     q = input.v * (1.0 - (input.s * ff))
#     t = input.v * (1.0 - (input.s * (1.0 - ff)))
#     if i == 0:
#         output = RGB(input.v, t, p)
#     elif i == 1:
#         output = RGB(q, input.v, p)
#     elif i == 2:
#         output = RGB(p, input.v, t)
#     elif i == 3:
#         output = RGB(p, q, input.v)
#     elif i == 4:
#         output = RGB(t, p, input.v)
#     else:
#         output = RGB(input.v, p, q)
#     return output
#
#
# # st = time.time()
# # for r in range(256):
# #     for g in range(256):
# #         for b in range(256):
# #             rgb_color = RGB(r / 255, g / 255, b / 255)
# #             hsv_color = RGB2HSV(rgb_color)
# #             new_rgb_color = HSV2RGB(hsv_color)
# # end = time.time()
# # timedelta = end - st
# # print(f"Czas: {timedelta}")
#
#
#
# # Example usage:
# r, g, b = 0, 0, 0
# rgb_color = RGB(r/255, g/255, b/255)
# hsv_color = RGB2HSV(rgb_color)
# print("RGB to HSV:", hsv_color.h, hsv_color.s, hsv_color.v)
#
# new_rgb_color = HSV2RGB(hsv_color)
# print("HSV to RGB:", new_rgb_color.r*255, new_rgb_color.g*255, new_rgb_color.b*255)