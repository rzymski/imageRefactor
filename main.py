import tkinter as tk
from imageRefactorApp import ImageRefactorApp
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRefactorApp(root)
    root.mainloop()


# import numpy as np
# a = np.array([[1, 2], [3, 4]])
# print(a)
# a2 = np.pad(a, ((0, 0), (2, 3)), 'edge')
# print(a2)
#
# # a1 = [1, 2, 3]
# # a2 = [4, 5, 6]
# # a3 = np.add(a1, a2)
# # print(a3)
#
#
# # arr = np.arange(0, 48, 1, dtype=int)
# # for i in np.nditer(arr):
# #     arr[i] += i*i/2
# arr = np.random.randint(10, size=(1, 147))
#
# # print(f"Shape = {arr.shape} Arr:\n{arr}")
# arr = arr.reshape((7, 7, 3))
# # print(f"Shape = {arr.shape} Arr:\n{arr}")
# reds = arr[:, :, 0]
# print(f"Reds:\n{reds}\n")
#
# # redSquares = reds[1:-1, 1:-1]
# # print(redSquares)
#
# # redSquaresChanged = np.average()
# print("KWADRATY")
# if reds.shape >= (3, 3):
#     print("OK")
#     squares = np.lib.stride_tricks.sliding_window_view(reds, (5, 5), subok=True)
#     print(squares)
#     # print("Średnie:\n")
#     # averagesOfSquares = np.average(squares, axis=(2, 3))
#     # print(averagesOfSquares)
#
# else:
#     print("NIE OK")
#
# # print("Srodki")
# # redSquares = reds[1:-1, 1:-1]
# # print(redSquares)
# # print("Zmiana")
# # reds[1:-1, 1:-1] = averagesOfSquares
# # print(reds)
# # print("Tablica po zmianach:")
# # arr[:, :, 0][1:-1, 1:-1] = averagesOfSquares
# # print(arr)
