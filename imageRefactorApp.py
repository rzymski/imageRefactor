from tkinter import *
# import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.simpledialog as simpledialog
import time
import tkinter.font as font
from copy import deepcopy
import re

import numpy as np

class ImageRefactorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image viewer Piotr Szumowski")
        bigFont = font.Font(size=12, weight="bold")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.frame = LabelFrame(self.root, padx=0, pady=0, labelanchor="w")
        self.frame.pack(side="left", fill="both")

        self.loadJPGButton = Button(self.frame, text="Load JPG", command=self.loadJPG, padx=10, pady=10)
        self.loadJPGButton.grid(row=0, column=0, sticky="WE")
        self.loadJPGButton['font'] = bigFont

        self.reloadOriginalJPGButton = Button(self.frame, text="Reload original JPG", command=self.reloadOriginalJPG, padx=10, pady=10)
        self.reloadOriginalJPGButton.grid(row=1, column=0, sticky="WE")
        self.reloadOriginalJPGButton['font'] = bigFont

        self.saveJPGButton = Button(self.frame, text="Save JPG", command=self.saveJPG, padx=10, pady=10)
        self.saveJPGButton.grid(row=2, column=0, sticky="WE")
        self.saveJPGButton['font'] = bigFont
        # LabelFrame for pixel
        self.pixel_info_label = LabelFrame(self.frame, text="Pixel", padx=0, pady=0, labelanchor="nw")
        self.pixel_info_label.grid(row=4, column=0, sticky="WE")
        # labels for pixel
        self.pixelXLabel = Label(self.pixel_info_label, text="X")
        self.pixelXLabel.grid(row=0, column=0, sticky="E")
        self.pixelYLabel = Label(self.pixel_info_label, text="Y")
        self.pixelYLabel.grid(row=1, column=0, sticky="E")
        self.pixelRedLabel = Label(self.pixel_info_label, text="Red")
        self.pixelRedLabel.grid(row=2, column=0, sticky="E")
        self.pixelGreenLabel = Label(self.pixel_info_label, text="Green")
        self.pixelGreenLabel.grid(row=3, column=0, sticky="E")
        self.pixelBlueLabel = Label(self.pixel_info_label, text="Blue")
        self.pixelBlueLabel.grid(row=4, column=0, sticky="E")
        # entries for pixel
        self.pixelXEntry = Entry(self.pixel_info_label, state=DISABLED, disabledforeground="black", disabledbackground="white", justify=CENTER)
        self.pixelXEntry.grid(row=0, column=1)
        self.pixelYEntry = Entry(self.pixel_info_label, state=DISABLED, disabledforeground="black", disabledbackground="white", justify=CENTER)
        self.pixelYEntry.grid(row=1, column=1)
        self.pixelRedEntry = Entry(self.pixel_info_label, state=DISABLED, disabledforeground="black", disabledbackground="white", justify=CENTER)
        self.pixelRedEntry.grid(row=2, column=1)
        self.pixelGreenEntry = Entry(self.pixel_info_label, state=DISABLED, disabledforeground="black", disabledbackground="white", justify=CENTER)
        self.pixelGreenEntry.grid(row=3, column=1)
        self.pixelBlueEntry = Entry(self.pixel_info_label, state=DISABLED, disabledforeground="black", disabledbackground="white", justify=CENTER)
        self.pixelBlueEntry.grid(row=4, column=1)
        # LabelFrame for operations
        self.pointOperationsLabel = LabelFrame(self.frame, text="Point transformation", padx=10, pady=10, labelanchor="nw")
        self.pointOperationsLabel.grid(row=5, column=0, sticky="WE")
        # RadioButtons for operations
        self.operationType = StringVar(value="+")
        # self.operationType.set("+")
        self.radioAddition = Radiobutton(self.pointOperationsLabel, text="Addition", value="+", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioAddition.grid(row=0, column=0, sticky="W", columnspan=2)
        self.radioSubtraction = Radiobutton(self.pointOperationsLabel, text="Subtraction", value="-", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioSubtraction.grid(row=1, column=0, sticky="W", columnspan=2)
        self.radioMultiplication = Radiobutton(self.pointOperationsLabel, text="Multiplication", value="*", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioMultiplication.grid(row=2, column=0, sticky="W", columnspan=2)
        self.radioDivision = Radiobutton(self.pointOperationsLabel, text="Division", value="/", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioDivision.grid(row=3, column=0, sticky="W", columnspan=2)
        self.radioBrightness = Radiobutton(self.pointOperationsLabel, text="Lightness change", value="lightness", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioBrightness.grid(row=4, column=0, sticky="W", columnspan=2)
        self.radioGrayScale1 = Radiobutton(self.pointOperationsLabel, text="Gray Scale averaged", value="grayAverage", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioGrayScale1.grid(row=5, column=0, sticky="W", columnspan=2)
        self.radioGrayScale2 = Radiobutton(self.pointOperationsLabel, text="Gray Scale adjusted", value="grayAdjust", variable=self.operationType, command=self.onRadioButtonSelect)
        self.radioGrayScale2.grid(row=6, column=0, sticky="W", columnspan=2)
        self.operationSubmitButton = Button(self.pointOperationsLabel, text="Perform point transformation", command=self.doPointTransformation)
        self.operationSubmitButton.grid(row=8, column=0, sticky="WE", columnspan=2)
        # Parameters for operations
        vcmd = (self.pointOperationsLabel.register(self.validateEntryRGB))
        self.parameterOperationsLabel = LabelFrame(self.pointOperationsLabel, text="Parameters", padx=10, pady=10, labelanchor="nw")
        self.parameterOperationsLabel.grid(row=7, column=0, sticky="WE")
        self.redChangeLabel = Label(self.parameterOperationsLabel, text="Red")
        self.redChangeLabel.grid(row=0, column=0, sticky="W")
        self.redChangeEntry = Entry(self.parameterOperationsLabel, validate='all', validatecommand=(vcmd, '%P'))
        self.redChangeEntry.grid(row=0, column=1)
        self.greenChangeLabel = Label(self.parameterOperationsLabel, text="Green")
        self.greenChangeLabel.grid(row=1, column=0, sticky="W")
        self.greenChangeEntry = Entry(self.parameterOperationsLabel, validate='all', validatecommand=(vcmd, '%P'))
        self.greenChangeEntry.grid(row=1, column=1)
        self.blueChangeLabel = Label(self.parameterOperationsLabel, text="Blue")
        self.blueChangeLabel.grid(row=2, column=0, sticky="W")
        self.blueChangeEntry = Entry(self.parameterOperationsLabel, validate='all', validatecommand=(vcmd, '%P'))
        self.blueChangeEntry.grid(row=2, column=1)
        self.lightChangeLabel = Label(self.parameterOperationsLabel, text="Light")
        self.lightChangeEntry = Entry(self.parameterOperationsLabel, validate='all', validatecommand=(vcmd, '%P'))
        # LabelFrame for filters
        self.filterLabel = LabelFrame(self.frame, text="Filters", padx=10, pady=10, labelanchor="nw")
        self.filterLabel.grid(row=6, column=0, sticky="WE")
        # RadioButtons for filters
        self.filterType = StringVar(value="0")
        # self.filterType.set("0")
        self.switchState = StringVar(value="on")
        self.optimizationSwitch = ctk.CTkSwitch(self.filterLabel, text="Optimization", variable=self.switchState, onvalue="on", offvalue="off", button_color="black")  # progress_color="blue"
        self.optimizationSwitch.grid(row=0, column=0, sticky="WE")
        self.filterAverage = Radiobutton(self.filterLabel, text="Average filter", value="0", variable=self.filterType)
        self.filterAverage.grid(row=1, column=0, sticky="W")
        self.filterMedian = Radiobutton(self.filterLabel, text="Median filter", value="1", variable=self.filterType)
        self.filterMedian.grid(row=2, column=0, sticky="W")
        self.filterSobel = Radiobutton(self.filterLabel, text="Sobel filter", value="2", variable=self.filterType)
        self.filterSobel.grid(row=3, column=0, sticky="W")
        self.filterHighPassSharpening = Radiobutton(self.filterLabel, text="High pass sharpening filter", value="3", variable=self.filterType)
        self.filterHighPassSharpening.grid(row=4, column=0, sticky="W")
        self.filterGaussianBlur = Radiobutton(self.filterLabel, text="Gaussian Blur filter", value="4", variable=self.filterType)
        self.filterGaussianBlur.grid(row=5, column=0, sticky="W")
        self.filterSubmitButton = Button(self.filterLabel, text="Apply filter", command=self.applyFilter)
        self.filterSubmitButton.grid(row=6, column=0, sticky="WE")

        self.imageSpace = Canvas(self.root, bg="white")
        self.imageSpace.pack(fill="both", expand=True)
        self.image = None
        self.imageId = None
        self.movedX = 0
        self.movedY = 0
        self.originalImage = None
        self.pixels = None

    def validateEntryRGB(self, P):
        pattern = r'^-?\d*(\.\d*)?$'
        if re.match(pattern, P) is not None:
            return True
        else:
            return False

    def onRadioButtonSelect(self):
        self.updateParameterLabels(self.operationType.get())

    def updateParameterLabels(self, value):
        self.redChangeLabel.grid_forget()
        self.redChangeEntry.grid_forget()
        self.greenChangeLabel.grid_forget()
        self.greenChangeEntry.grid_forget()
        self.blueChangeLabel.grid_forget()
        self.blueChangeEntry.grid_forget()
        self.lightChangeLabel.grid_forget()
        self.lightChangeEntry.grid_forget()
        if value in ['+', '-', '*', '/']:
            self.parameterOperationsLabel.grid(row=7, column=0, sticky="WE")
            self.redChangeLabel.grid(row=0, column=0, sticky="W")
            self.redChangeEntry.grid(row=0, column=1)
            self.greenChangeLabel.grid(row=1, column=0, sticky="W")
            self.greenChangeEntry.grid(row=1, column=1)
            self.blueChangeLabel.grid(row=2, column=0, sticky="W")
            self.blueChangeEntry.grid(row=2, column=1)
        elif value == 'lightness':
            self.parameterOperationsLabel.grid(row=7, column=0, sticky="WE")
            self.lightChangeLabel.grid(row=0, column=0, sticky="W")
            self.lightChangeEntry.grid(row=0, column=1)
        elif value == 'grayAverage' or value == 'grayAdjust':
            self.parameterOperationsLabel.grid_forget()
        else:
            raise Exception("Nie ma takiej opcji")

    def applyFilter(self):
        print(f"Zastosowano filtr: {self.filterType.get()} optymalizacja jest {self.switchState.get()}")
        if self.filterType.get() == '0':
            self.averageFilter() if self.switchState.get() == "off" else self.averageFilterOptimized()
        elif self.filterType.get() == '1':
            self.medianFilter() if self.switchState.get() == "off" else self.medianFilterOptimized()
        elif self.filterType.get() == '2':
            self.sobelFilter()
        elif self.filterType.get() == '3':
            self.highPassSharpeningFilter()
        elif self.filterType.get() == '4':
            self.gaussianBlurFilter()
        else:
            raise Exception(f"Nie ma takiego filtra {self.filterType.get()}")

    def averageFilter(self):
        self.measureTime("START")
        if self.image:
            # mask = np.array([[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]])
            height, width, _ = self.pixels.shape
            smoothed_pixels = deepcopy(self.pixels)
            for y in range(0, height):
                for x in range(0, width):
                    for c in range(3):  # Loop over R, G, and B channels
                        if 0 < y < height - 1 and 0 < x < width - 1:  # srodek
                            # smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x - 1:x + 2, c], weights=mask)
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x - 1:x + 2, c])
                            # print(smoothed_pixels[y - 1:y + 2, x - 1:x + 2, c])
                        elif 0 < y < height - 1 and 0 < x:  # krawedz prawa
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x - 1:x + 1, c])
                        elif 0 < y < height - 1 and x < width - 1:  # krawedz lewa
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x:x + 2, c])
                        elif 0 < y and 0 < x < width - 1:  # dol
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x - 1:x + 2, c])
                        elif y < height - 1 and 0 < x < width - 1:  # gora
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x - 1:x + 2, c])
                        elif x == 0 and y == 0:  # lewy gorny rog
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x:x + 2, c])
                        elif x == width - 1 and y == 0:  # prawy gorny rog
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x:x + 1, c])
                        elif x == 0 and y == height - 1:  # lewy dolny rog
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x:x + 2, c])
                        elif x == width - 1 and y == height - 1:  # prawy dolny rog
                            smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x - 1:x + 1, c])
                        else:
                            print("Jest tylko jeden pixel")
            self.limitPixelsAndShowImage(smoothed_pixels, True)
            # smoothed_pixels = np.clip(smoothed_pixels, 0, 255).astype(np.uint8)
            # self.pixels = smoothed_pixels
            # self.image = Image.fromarray(self.pixels)
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def averageFilterOptimized(self):
        self.measureTime("START")
        if self.image:
            # filtrowanie krawedzi
            height, width, _ = self.pixels.shape
            smoothed_pixels = deepcopy(self.pixels)
            for y in range(0, height):
                for x in range(0, width):
                    if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                        for c in range(3):  # Loop over R, G, and B channels
                            if 0 < y < height - 1 and 0 < x:  # krawedz prawa
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x - 1:x + 1, c])
                            elif 0 < y < height - 1 and x < width - 1:  # krawedz lewa
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 2, x:x + 2, c])
                            elif 0 < y and 0 < x < width - 1:  # dol
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x - 1:x + 2, c])
                            elif y < height - 1 and 0 < x < width - 1:  # gora
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x - 1:x + 2, c])
                            elif x == 0 and y == 0:  # lewy gorny rog
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x:x + 2, c])
                            elif x == width - 1 and y == 0:  # prawy gorny rog
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y:y + 2, x:x + 1, c])
                            elif x == 0 and y == height - 1:  # lewy dolny rog
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x:x + 2, c])
                            elif x == width - 1 and y == height - 1:  # prawy dolny rog
                                smoothed_pixels[y, x, c] = np.average(self.pixels[y - 1:y + 1, x - 1:x + 1, c])
            if self.pixels.shape < (3, 3, 3):
                print("Nie mozna nalozyc maski jesli wymiar obrazu jest ponizej 3x3")
                return
            # wyciecie wartosci czerwonych, zielonych i niebieskich pixeli osobno
            reds, greens, blues = self.pixels[:, :, 0], self.pixels[:, :, 1], self.pixels[:, :, 2]
            # stworzenie macierz 3x3 z sasiadujacych wartosci dla kazdej grupy
            redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (3, 3)), np.lib.stride_tricks.sliding_window_view(greens, (3, 3)), np.lib.stride_tricks.sliding_window_view(blues, (3, 3))
            # wyliczenie mediany z kazdej macierzy
            averagesOfRedSquares, averagesOfGreenSquares, averagesOfBlueSquares = np.average(redSquares, axis=(2, 3)), np.average(greenSquares, axis=(2, 3)), np.average(blueSquares, axis=(2, 3))
            # przypisanie median do srodowych wartosci w macierzach
            self.pixels[:, :, 0][1:-1, 1:-1], self.pixels[:, :, 1][1:-1, 1:-1], self.pixels[:, :, 2][1:-1, 1:-1] = averagesOfRedSquares, averagesOfGreenSquares, averagesOfBlueSquares
            # dodanie krawedzi fo pixeli
            for y in range(0, height):
                for x in range(0, width):
                    if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                        for c in range(3):
                            self.pixels[y, x, c] = smoothed_pixels[y, x, c]
            # ograniczenie pixeli do wartosci od 0 do 255 oraz narysowanie obrazka
            self.limitPixelsAndShowImage(self.pixels, True)
            # limitedPixels = np.clip(self.pixels, 0, 255).astype(np.uint8)
            # self.image = Image.fromarray(np.uint8(limitedPixels))
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def medianFilter(self):
        self.measureTime("START")
        if self.image:
            height, width, _ = self.pixels.shape
            smoothed_pixels = deepcopy(self.pixels)
            for y in range(0, height):
                for x in range(0, width):
                    for c in range(3):  # Loop over R, G, and B channels
                        if 0 < y < height-1 and 0 < x < width-1:  # srodek
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x - 1:x + 2, c])
                        elif 0 < y < height-1 and 0 < x:  # krawedz prawa
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x - 1:x + 1, c])
                        elif 0 < y < height-1 and x < width-1:  # krawedz lewa
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x:x + 2, c])
                        elif 0 < y and 0 < x < width-1:  # dol
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 1, x - 1:x + 2, c])
                        elif y < height-1 and 0 < x < width-1:  # gora
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x - 1:x + 2, c])
                        elif x == 0 and y == 0:  # lewy gorny rog
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x:x + 2, c])
                        elif x == width-1 and y == 0:  # prawy gorny rog
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x:x + 1, c])
                        elif x == 0 and y == height-1:  # lewy dolny rog
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y-1:y + 1, x:x + 2, c])
                        elif x == width-1 and y == height-1:  # prawy dolny rog
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y-1:y + 1, x-1:x + 1, c])
                        else:
                            print("Jest tylko jeden pixel")
            self.limitPixelsAndShowImage(smoothed_pixels, True)
            # smoothed_pixels = np.clip(smoothed_pixels, 0, 255).astype(np.uint8)
            # self.pixels = smoothed_pixels
            # self.image = Image.fromarray(self.pixels)
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def medianFilterOptimized(self):
        self.measureTime("START")
        if self.image:
            # filtrowanie krawedzi
            height, width, _ = self.pixels.shape
            smoothed_pixels = deepcopy(self.pixels)
            for y in range(0, height):
                for x in range(0, width):
                    if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                        for c in range(3):  # Loop over R, G, and B channels
                            if 0 < y < height - 1 and 0 < x:  # krawedz prawa
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x - 1:x + 1, c])
                            elif 0 < y < height - 1 and x < width - 1:  # krawedz lewa
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x:x + 2, c])
                            elif 0 < y and 0 < x < width - 1:  # dol
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 1, x - 1:x + 2, c])
                            elif y < height - 1 and 0 < x < width - 1:  # gora
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x - 1:x + 2, c])
                            elif x == 0 and y == 0:  # lewy gorny rog
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x:x + 2, c])
                            elif x == width - 1 and y == 0:  # prawy gorny rog
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y:y + 2, x:x + 1, c])
                            elif x == 0 and y == height - 1:  # lewy dolny rog
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 1, x:x + 2, c])
                            elif x == width - 1 and y == height - 1:  # prawy dolny rog
                                smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 1, x - 1:x + 1, c])
            if self.pixels.shape < (3, 3, 3):
                print("Nie mozna nalozyc maski jesli wymiar obrazu jest ponizej 3x3")
                return
            # wyciecie wartosci czerwonych, zielonych i niebieskich pixeli osobno
            reds, greens, blues = self.pixels[:, :, 0], self.pixels[:, :, 1], self.pixels[:, :, 2]
            # stworzenie macierz 3x3 z sasiadujacych wartosci dla kazdej grupy
            redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (3, 3)), np.lib.stride_tricks.sliding_window_view(greens, (3, 3)), np.lib.stride_tricks.sliding_window_view(blues, (3, 3))
            # wyliczenie mediany z kazdej macierzy
            mediansOfRedSquares, mediansOfGreenSquares, mediansOfBlueSquares = np.median(redSquares, axis=(2, 3)), np.median(greenSquares, axis=(2, 3)), np.median(blueSquares, axis=(2, 3))
            # przypisanie median do srodowych wartosci w macierzach
            self.pixels[:, :, 0][1:-1, 1:-1], self.pixels[:, :, 1][1:-1, 1:-1], self.pixels[:, :, 2][1:-1, 1:-1] = mediansOfRedSquares, mediansOfGreenSquares, mediansOfBlueSquares
            #dodanie krawedzi fo pixeli
            for y in range(0, height):
                for x in range(0, width):
                    if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                        for c in range(3):
                            self.pixels[y, x, c] = smoothed_pixels[y, x, c]
            self.limitPixelsAndShowImage(self.pixels, True)
            # ograniczenie pixeli do wartosci od 0 do 255 oraz narysowanie obrazka
            # limitedPixels = np.clip(self.pixels, 0, 255).astype(np.uint8)
            # self.image = Image.fromarray(np.uint8(limitedPixels))
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def sobelFilter(self):
        pass

    def highPassSharpeningFilter(self):
        pass

    def gaussianBlurFilter(self):
        pass

    def doPointTransformation(self):
        print(f"Wykonał: {self.operationType.get()}")
        if self.operationType.get() in ['+', '-', '*', '/']:
            self.simpleRGBOperation(self.operationType.get())
        elif self.operationType.get() == 'grayAverage':
            self.greyConversion(False)
        elif self.operationType.get() == 'grayAdjust':
            self.greyConversion(True)
        elif self.operationType.get() == 'lightness':
            self.changeLightness()
        else:
            print("Nie ma takiej operacji")

    def convertRGBtoHSV(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_color = max(r, g, b)
        min_color = min(r, g, b)
        # Calculate the hue
        if max_color == min_color:
            h = 0  # No hue
        elif max_color == r:
            h = (60 * ((g - b) / (max_color - min_color)) + 360) % 360
        elif max_color == g:
            h = (60 * ((b - r) / (max_color - min_color)) + 120) % 360
        else:  # max_color == b
            h = (60 * ((r - g) / (max_color - min_color)) + 240) % 360
        # Calculate the saturation
        if max_color == 0:
            s = 0
        else:
            s = (max_color - min_color) / max_color * 100
        # Calculate the value
        v = max_color * 100
        return h, s, v

    def convertHSVtoRGB(self, h, s, v):
        s /= 100
        v /= 100
        c = v * s
        x = c * (1-abs((h/60) % 2 - 1))
        m = v - c
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x
        else:
            raise Exception("H poza zakresem")
        r, g, b = round((r+m)*255), round((g+m)*255), round((b+m)*255)
        return r, g, b

    def changeLightness(self):
        self.measureTime("START")
        if self.image:
            reds = self.pixels[:, :, 0]
            greens = self.pixels[:, :, 1]
            blues = self.pixels[:, :, 2]
            h, s, v = np.vectorize(self.convertRGBtoHSV)(reds, greens, blues)
            v *= max(0, min(255, float(self.lightChangeEntry.get())))
            r, g, b = np.vectorize(self.convertHSVtoRGB)(h, s, v)
            self.pixels[:, :, 0] = r
            self.pixels[:, :, 1] = g
            self.pixels[:, :, 2] = b
            self.limitPixelsAndShowImage(self.pixels, False)
            # limitedPixels = np.clip(self.pixels, 0, 255).astype(np.uint8)
            # self.image = Image.fromarray(np.uint8(limitedPixels))
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")
        print("SKONCZYL")

    def greyConversion(self, adjusted=False):
        self.measureTime("START")
        if self.image:
            # Zrobienie sredniej z wyswietlanych pixeli na ekranie
            if adjusted:
                averages = 0.299 * self.pixels[:, :, 0] + 0.587 * self.pixels[:, :, 1] + 0.114 * self.pixels[:, :, 2]
                self.pixels[:, :, 0] = averages
                self.pixels[:, :, 1] = averages
                self.pixels[:, :, 2] = averages
            else:
                averages = (self.pixels[:, :, 0] + self.pixels[:, :, 1] + self.pixels[:, :, 2]) / 3
                self.pixels[:, :, 0] = averages
                self.pixels[:, :, 1] = averages
                self.pixels[:, :, 2] = averages
            self.limitPixelsAndShowImage(self.pixels, False)
            # limitedPixels = np.clip(self.pixels, 0, 255).astype(np.uint8)
            # self.image = Image.fromarray(np.uint8(limitedPixels))
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def simpleRGBOperation(self, operator):
        self.measureTime("START")
        if self.image:
            try:
                red_change = float(self.redChangeEntry.get())
            except:
                red_change = None
            try:
                green_change = float(self.greenChangeEntry.get())
            except:
                green_change = None
            try:
                blue_change = float(self.blueChangeEntry.get())
            except:
                blue_change = None

            if red_change is None and green_change is None and blue_change is None:
                print("SAME NONE")
                return
            elif (red_change and red_change < 0 or green_change and green_change < 0 or blue_change and blue_change < 0) and (operator == '/' or operator == '*'):
                print("Nie ma sensu mnożyć lub dzielić przez ujemne wartosci")
                return
            elif (red_change and red_change == 0 or green_change and green_change == 0 or blue_change and blue_change == 0) and operator == '/':
                print("Nie mozna dzielic przez 0")
                return
            if operator == '+':
                self.pixels[:, :, 0] = self.pixels[:, :, 0] + red_change if red_change is not None else self.pixels[:, :, 0]
                self.pixels[:, :, 1] = self.pixels[:, :, 1] + green_change if green_change is not None else self.pixels[:, :, 1]
                self.pixels[:, :, 2] = self.pixels[:, :, 2] + blue_change if blue_change is not None else self.pixels[:, :, 2]
            elif operator == '-':
                self.pixels[:, :, 0] = self.pixels[:, :, 0] - red_change if red_change is not None else self.pixels[:, :, 0]
                self.pixels[:, :, 1] = self.pixels[:, :, 1] - green_change if green_change is not None else self.pixels[:, :, 1]
                self.pixels[:, :, 2] = self.pixels[:, :, 2] - blue_change if blue_change is not None else self.pixels[:, :, 2]
            elif operator == '*':
                self.pixels[:, :, 0] = self.pixels[:, :, 0] * red_change if red_change is not None else self.pixels[:, :, 0]
                self.pixels[:, :, 1] = self.pixels[:, :, 1] * green_change if green_change is not None else self.pixels[:, :, 1]
                self.pixels[:, :, 2] = self.pixels[:, :, 2] * blue_change if blue_change is not None else self.pixels[:, :, 2]
            elif operator == '/':
                if red_change:
                    self.pixels[:, :, 0] = self.pixels[:, :, 0] / red_change
                if green_change:
                    self.pixels[:, :, 1] = self.pixels[:, :, 1] / green_change
                if blue_change:
                    self.pixels[:, :, 2] = self.pixels[:, :, 2] / blue_change
            else:
                raise Exception(f"Nie właściwy operator. Nie ma operatora: {operator}")
            self.limitPixelsAndShowImage(self.pixels, False)
            # limitedPixels = np.clip(self.pixels, 0, 255).astype(np.uint8)
            # print(limitedPixels)
            #
            # self.image = Image.fromarray(np.uint8(limitedPixels))
            # self.tk_image = ImageTk.PhotoImage(self.image)
            # self.show_image()
        self.measureTime("END")

    def limitPixelsAndShowImage(self, pixels=None, limitPixels=False):
        if pixels is not None:
            limitedPixels = np.clip(pixels, 0, 255)
        else:
            limitedPixels = np.clip(self.pixels, 0, 255)
        if limitPixels:
            self.pixels = limitedPixels
        self.image = Image.fromarray(limitedPixels.astype(np.uint8))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.show_image()

    def update_pixel_info_label(self, x, y, pixel_rgb):
        if pixel_rgb is not None:
            r, g, b = pixel_rgb
            for entry, value in zip(
                    [self.pixelXEntry, self.pixelYEntry, self.pixelRedEntry, self.pixelGreenEntry, self.pixelBlueEntry], [x, y, r, g, b]):
                entry.config(state="normal")
                entry.delete(0, 'end')
                entry.insert(0, str(value))
                entry.config(state="disabled")
        else:
            for entry in self.pixelXEntry, self.pixelYEntry, self.pixelRedEntry, self.pixelGreenEntry, self.pixelBlueEntry:
                entry.config(state="normal")
                entry.delete(0, 'end')
                entry.config(state="disabled")

    def settingsAfterLoad(self):
        if self.imageId is not None:
            self.imageSpace.delete(self.imageId)
            self.movedX, self.movedY = 0, 0
        self.imageId = self.imageSpace.create_image(self.movedX, self.movedY, anchor="nw", image=self.tk_image)
        self.imageSpace.bind("<Motion>", self.on_mouse_move)
        self.imageSpace.bind("<Enter>", self.changeCursor)
        self.imageSpace.bind("<Leave>", self.changeCursorBack)
        self.bind_keyboard_events()
        self.bind_mouse_drag_events()
        self.zoom_settings()

    def show_image(self):
        if self.imageId:
            self.imageSpace.delete(self.imageId)
            self.imageId = None
            self.imageSpace.imagetk = None
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # # Use self.text object to set proper coordinates
        self.imageId = self.imageSpace.create_image(self.movedX, self.movedY, anchor='nw', image=imagetk)

        # self.imageId = self.imageSpace.create_image(self.imageSpace.coords(self.text), anchor='nw', image=imagetk)
        self.imageSpace.lower(self.imageId)
        self.imageSpace.imagetk = imagetk
        # self.movedX = 0
        # self.movedY = 0

    def loadJPG(self):
        filePath = askopenfilename()
        if filePath == '':
            return
        self.image = Image.open(filePath)
        self.pixels = np.array(self.image, dtype=np.int32)
        self.originalImage = deepcopy(self.image)
        if self.image is None:
            return
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.settingsAfterLoad()

    def reloadOriginalJPG(self):
        if self.originalImage:
            self.image = deepcopy(self.originalImage)
            self.pixels = np.array(self.image, dtype=np.int32)
            if self.image is None:
                return
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.settingsAfterLoad()

    def saveJPG(self):
        if self.image:
            file_path = asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.image.save(file_path, "JPEG")
                print(f"Image saved as {file_path}")

    # przesuwanie obrazków myszką
    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def drag_image(self, event):
        if hasattr(self, 'last_x') and hasattr(self, 'last_y'):
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.move_image(event, dx, dy, False)
            self.last_x = event.x
            self.last_y = event.y

    def stop_drag(self, event):
        if hasattr(self, 'last_x') and hasattr(self, 'last_y'):
            del self.last_x
            del self.last_y

    def bind_mouse_drag_events(self):
        self.imageSpace.bind("<ButtonPress-1>", self.start_drag)
        self.imageSpace.bind("<B1-Motion>", self.drag_image)
        self.imageSpace.bind("<ButtonRelease-1>", self.stop_drag)
    # zmiana kursora
    def changeCursor(self, event):
        self.imageSpace.config(cursor="cross_reverse")  # best option "pirate" XD

    def changeCursorBack(self, event):
        self.imageSpace.config(cursor="")

    def zoom_settings(self):
        self.root.bind("<MouseWheel>", self.wheel)
        self.imscale = 1.0
        self.delta = 0.75
        self.text = self.imageSpace.create_text(0, 0, anchor='nw', text='')
        self.show_image()
        self.imageSpace.configure(scrollregion=self.imageSpace.bbox('all'))

    def wheel(self, event):
        scale = 1.0
        if event.delta == -120:
            scale *= self.delta
            self.imscale *= self.delta
        if event.delta == 120:
            scale /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.imageSpace.canvasx(event.x)
        y = self.imageSpace.canvasy(event.y)
        self.imageSpace.scale(self.imageId, x, y, scale, scale)
        self.show_image()

    def move_image(self, event, dx, dy, scaleMoving=False):
        if self.imageId is not None:
            if scaleMoving:
                dx *= self.imscale*2
                dy *= self.imscale*2
            self.movedX += dx
            self.movedY += dy
            self.imageSpace.move(self.imageId, dx, dy)

    def bind_keyboard_events(self):
        self.root.bind("<Left>", lambda event: self.move_image(event, dx=10, dy=0, scaleMoving=True))
        self.root.bind("<Right>", lambda event: self.move_image(event, dx=-10, dy=0, scaleMoving=True))
        self.root.bind("<Up>", lambda event: self.move_image(event, dx=0, dy=10, scaleMoving=True))
        self.root.bind("<Down>", lambda event: self.move_image(event, dx=0, dy=-10, scaleMoving=True))

    def on_mouse_move(self, event):
        # image_coords = self.imageSpace.coords(self.imageId)
        # print(f"{image_coords} {self.image.width} {self.image.height}")
        # print(f"f{self.image}")
        if self.image is not None:
            x, y = event.x-self.movedX, event.y-self.movedY
            # print(f"x={event.x} mX={self.movedX}  y={event.y} mY={self.movedY} IX={self.image.width}  IY={self.image.height}")
            # image_x, image_y = self.imageSpace.coords(self.imageId)
            # print(f"Ob = {image_x} {image_y}")
            if (0 <= x < self.image.width * self.imscale) and (0 <= y < self.image.height * self.imscale):
                pixel_rgb = self.get_pixel_color(int(x/self.imscale), int(y/self.imscale))
                self.update_pixel_info_label(int(x/self.imscale), int(y/self.imscale), pixel_rgb)
            elif self.pixelXEntry.get():
                self.update_pixel_info_label(None, None, None)
    
    def get_pixel_color(self, x, y):
        if self.image is not None:
            try:
                pixel = self.image.getpixel((x, y))
                return pixel
            except Exception as e:
                print(f"Error getting pixel color: {e}")
        return None

    def measureTime(self, startEnd):
        if startEnd.lower() == "start":
            self.start_time = time.time()
        elif startEnd.lower() == "end":
            self.end_time = time.time()
            execution_time = self.end_time - self.start_time
            print(f"Czas wykonania funkcji: {execution_time} sekundy")
