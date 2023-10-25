import tkinter as tk
from imageRefactorApp import ImageRefactorApp
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRefactorApp(root)
    root.mainloop()







# r, g, b = 232, 255, 254
# root = tk.Tk()
# app = ImageRefactorApp(root)
#
# for r in range(256):
#     for g in range(256):
#         for b in range(256):
#             h, s, v = app.convertRGBtoHSV(r, g, b)
#             if 0 > h >= 360:
#                 raise Exception("H NIE PASUJE")
#             if 0 > s > 100 or 0 > v > 100:
#                 raise Exception("S lub V nie pasuje")
#             r2, g2, b2 = app.convertHSVtoRGB(h, s, v)
#             if 0 > r2 > 256 or 0 > g2 > 256 or 0 > b2 > 256:
#                 raise Exception("R2 lub G2 lub B2 nie pasuje")
#             if r != r2 or g != g2 or b != b2:
#                 print(f"STARE RGB ={r} {g} {b}\n NOWE RGB = {r2} {g2} {b2}")
# print("WSZYSTKO OK")
