import tkinter as tk
from imageRefactorApp import ImageRefactorApp
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ImageRefactorApp(root)
#     root.mainloop()

r, g, b = 255, 1, 3
root = tk.Tk()
app = ImageRefactorApp(root)
h, s, v = app.convertRGBtoHSV(r, g, b)
# print(f"RGB = {r} {g} {b}\nHSV = {h} {s} {v}")

r2, g2, b2 = app.convertHSVtoRGB(h, s, v)

print(f"RGB = {r} {g} {b}\nHSV = {h} {s} {v}  RGB2 = {r2} {g2} {b2}")