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
        self.radioAddition = Radiobutton(self.pointOperationsLabel, text="Addition", value="+", variable=self.operationType, command=self.onOperationSelect)
        self.radioAddition.grid(row=0, column=0, sticky="W", columnspan=2)
        self.radioSubtraction = Radiobutton(self.pointOperationsLabel, text="Subtraction", value="-", variable=self.operationType, command=self.onOperationSelect)
        self.radioSubtraction.grid(row=1, column=0, sticky="W", columnspan=2)
        self.radioMultiplication = Radiobutton(self.pointOperationsLabel, text="Multiplication", value="*", variable=self.operationType, command=self.onOperationSelect)
        self.radioMultiplication.grid(row=2, column=0, sticky="W", columnspan=2)
        self.radioDivision = Radiobutton(self.pointOperationsLabel, text="Division", value="/", variable=self.operationType, command=self.onOperationSelect)
        self.radioDivision.grid(row=3, column=0, sticky="W", columnspan=2)
        self.radioBrightness = Radiobutton(self.pointOperationsLabel, text="Lightness change", value="lightness", variable=self.operationType, command=self.onOperationSelect)
        self.radioBrightness.grid(row=4, column=0, sticky="W", columnspan=2)
        self.radioGrayScale1 = Radiobutton(self.pointOperationsLabel, text="Gray Scale averaged", value="grayAverage", variable=self.operationType, command=self.onOperationSelect)
        self.radioGrayScale1.grid(row=5, column=0, sticky="W", columnspan=2)
        self.radioGrayScale2 = Radiobutton(self.pointOperationsLabel, text="Gray Scale adjusted", value="grayAdjust", variable=self.operationType, command=self.onOperationSelect)
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
        self.switchOptimizedState = StringVar(value="on")
        self.optimizationSwitch = ctk.CTkSwitch(self.filterLabel, text="Optimization", variable=self.switchOptimizedState, onvalue="on", offvalue="off", button_color="black")  # progress_color="blue"
        self.optimizationSwitch.grid(row=0, column=0, sticky="WE")
        self.switchEdgesState = StringVar(value="yes")
        self.edgesSwitch = ctk.CTkSwitch(self.filterLabel, text="Include edges", variable=self.switchEdgesState, onvalue="yes", offvalue="no", button_color="black")  # progress_color="blue"
        self.edgesSwitch.grid(row=1, column=0, sticky="WE")
        self.filterAverage = Radiobutton(self.filterLabel, text="Average filter", value="0", variable=self.filterType, command=self.onFilterSelect)
        self.filterAverage.grid(row=2, column=0, sticky="W")
        self.filterMedian = Radiobutton(self.filterLabel, text="Median filter", value="1", variable=self.filterType, command=self.onFilterSelect)
        self.filterMedian.grid(row=3, column=0, sticky="W")
        self.filterSobel = Radiobutton(self.filterLabel, text="Sobel filter", value="2", variable=self.filterType, command=self.onFilterSelect)
        self.filterSobel.grid(row=4, column=0, sticky="W")
        # label for sobel filter options
        self.sobelOptionsLabel = LabelFrame(self.filterLabel, text="Sobel options", padx=10, pady=10, labelanchor="nw")
        # Options filter Sobel both, horizontal or vertical
        self.sobelOption = StringVar(value="0")
        self.sobelBoth = Radiobutton(self.sobelOptionsLabel, text="Both horizontal and vertical", value="0", variable=self.sobelOption)
        self.sobelBoth.grid(row=0, column=0, sticky="W")
        self.sobelHorizontal = Radiobutton(self.sobelOptionsLabel, text="Horizontal", value="1", variable=self.sobelOption)
        self.sobelHorizontal.grid(row=1, column=0, sticky="W")
        self.sobelVertical = Radiobutton(self.sobelOptionsLabel, text="Vertical", value="2", variable=self.sobelOption)
        self.sobelVertical.grid(row=2, column=0, sticky="W")
        # RadioButtons for filters
        self.filterHighPassSharpening = Radiobutton(self.filterLabel, text="High pass sharpening filter", value="3", variable=self.filterType, command=self.onFilterSelect)
        self.filterHighPassSharpening.grid(row=6, column=0, sticky="W")
        self.filterGaussianBlur = Radiobutton(self.filterLabel, text="Gaussian Blur filter", value="4", variable=self.filterType, command=self.onFilterSelect)
        self.filterGaussianBlur.grid(row=7, column=0, sticky="W")
        self.filterSubmitButton = Button(self.filterLabel, text="Apply filter", command=self.applyFilter)
        self.filterSubmitButton.grid(row=8, column=0, sticky="WE")

        self.imageSpace = Canvas(self.root, bg="white")
        self.imageSpace.pack(fill="both", expand=True)
        self.image = None
        self.imageId = None
        self.movedX = 0
        self.movedY = 0
        self.originalImage = None
        self.pixels = None

        self.hsvPixels = None

    def validateEntryRGB(self, P):
        pattern = r'^-?\d*(\.\d*)?$'
        if re.match(pattern, P) is not None:
            return True
        else:
            return False

    def onOperationSelect(self):
        self.updateParameterLabels(self.operationType.get())

    def onFilterSelect(self):
        if self.filterType.get() == "2":
            self.sobelOptionsLabel.grid(row=5, column=0, sticky="WE")
        else:
            self.sobelOptionsLabel.grid_forget()

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
        self.hsvPixels = None
        includeEdges = True if self.switchEdgesState.get() == "yes" else False
        print(f"Zastosowano filtr: {self.filterType.get()} optymalizacja: {self.switchOptimizedState.get()} uzwglednia krawedzie: {includeEdges}")
        if self.filterType.get() == '0':
            self.averageFilter(padding=includeEdges) if self.switchOptimizedState.get() == "off" else self.averageFilterOptimized(padding=includeEdges)
        elif self.filterType.get() == '1':
            self.medianFilter(padding=includeEdges) if self.switchOptimizedState.get() == "off" else self.medianFilterOptimized(padding=includeEdges)
        elif self.filterType.get() == '2':
            self.sobelFilter(self.sobelOption.get(), padding=includeEdges) if self.switchOptimizedState.get() == "off" else self.sobelFilterOptimized(self.sobelOption.get(), padding=includeEdges)
        elif self.filterType.get() == '3':
            self.highPassSharpeningFilter(padding=includeEdges) if self.switchOptimizedState.get() == "off" else self.highPassSharpeningFilterOptimized(padding=includeEdges)
        elif self.filterType.get() == '4':
            self.gaussianBlurFilter(padding=includeEdges) if self.switchOptimizedState.get() == "off" else self.gaussianBlurFilterOptimized(padding=includeEdges)
        else:
            raise Exception(f"Nie ma takiego filtra {self.filterType.get()}")

    def averageFilter(self, padding=True):
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
                        elif not padding:
                            continue
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
        self.measureTime("END")

    def averageFilterOptimized(self, padding=True):
        self.measureTime("START")
        if self.image:
            # filtrowanie krawedzi
            if padding:
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
            if padding:
                for y in range(0, height):
                    for x in range(0, width):
                        if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                            for c in range(3):
                                self.pixels[y, x, c] = smoothed_pixels[y, x, c]
            # ograniczenie pixeli do wartosci od 0 do 255 oraz narysowanie obrazka
            self.limitPixelsAndShowImage(self.pixels, True)
        self.measureTime("END")

    def medianFilter(self, padding=True):
        self.measureTime("START")
        if self.image:
            height, width, _ = self.pixels.shape
            smoothed_pixels = deepcopy(self.pixels)
            for y in range(0, height):
                for x in range(0, width):
                    for c in range(3):  # Loop over R, G, and B channels
                        if 0 < y < height-1 and 0 < x < width-1:  # srodek
                            smoothed_pixels[y, x, c] = np.median(self.pixels[y - 1:y + 2, x - 1:x + 2, c])
                        elif not padding:
                            continue
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
        self.measureTime("END")

    def medianFilterOptimized(self, padding=True):
        self.measureTime("START")
        if self.image:
            # filtrowanie krawedzi
            if padding:
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
            if padding:
                for y in range(0, height):
                    for x in range(0, width):
                        if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                            for c in range(3):
                                self.pixels[y, x, c] = smoothed_pixels[y, x, c]
            self.limitPixelsAndShowImage(self.pixels, True)
        self.measureTime("END")

    def sobelFilter(self, sobelVariant, padding=True):
        self.measureTime("START")
        if self.image:
            sobelX = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
            sobelY = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            height, width, _ = self.pixels.shape
            sobelPixels = deepcopy(self.pixels)
            if padding:
                pad_size = 3 // 2
                paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                for y in range(height):
                    for x in range(width):
                        for c in range(3):  # Loop over R, G, and B channels
                            if sobelVariant == "0":
                                sobelPixels[y, x, c] = np.sqrt(np.add(np.power(np.sum(paddedImage[y:y+3, x:x+3, c] * sobelX), 2), np.power(np.sum(paddedImage[y:y+3, x:x+3, c] * sobelY), 2)))
                            elif sobelVariant == "1":
                                sobelPixels[y, x, c] = np.sum(paddedImage[y:y+3, x:x+3, c] * sobelY)
                            elif sobelVariant == "2":
                                sobelPixels[y, x, c] = np.sum(paddedImage[y:y+3, x:x+3, c] * sobelX)
                            else:
                                raise Exception("Nie ma takiej opcji Sobela")
            else:
                for y in range(1, height-1):
                    for x in range(1, width-1):
                        for c in range(3):  # Loop over R, G, and B channels
                            if sobelVariant == "0":
                                sobelPixels[y, x, c] = np.sqrt(np.add(np.power(np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * sobelX), 2), np.power(np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * sobelY), 2)))
                            elif sobelVariant == "1":
                                sobelPixels[y, x, c] = np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * sobelY)
                            elif sobelVariant == "2":
                                sobelPixels[y, x, c] = np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * sobelX)
                            else:
                                raise Exception("Nie ma takiej opcji Sobela")
            self.limitPixelsAndShowImage(sobelPixels, True)
        self.measureTime("END")

    def sobelFilterOptimized(self, sobelVariant, padding=True):
        self.measureTime("START")
        if self.image:
            if self.pixels.shape < (3, 3, 3):
                print("Nie mozna nalozyc maski jesli wymiar obrazu jest ponizej 3x3")
                return
            sobelX = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
            sobelY = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            # dodanie obramowania (kopiowanie wartosci granicznych) przy wlaczonym obramowaniu
            if padding:
                pad_size = 3 // 2
                paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                reds, greens, blues = paddedImage[:, :, 0], paddedImage[:, :, 1], paddedImage[:, :, 2]
            else:
                reds, greens, blues = self.pixels[:, :, 0], self.pixels[:, :, 1], self.pixels[:, :, 2]
            # stworzenie macierz 3x3 z sasiadujacych wartosci dla kazdej grupy
            redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (3, 3)), np.lib.stride_tricks.sliding_window_view(greens, (3, 3)), np.lib.stride_tricks.sliding_window_view(blues, (3, 3))
            # sobel z kazdej macierzy
            if sobelVariant == "0":
                sobelsOfRedSquares = np.sqrt(np.add(np.power(np.sum(redSquares * sobelX, axis=(2, 3)), 2), np.power(np.sum(redSquares * sobelY, axis=(2, 3)), 2)))
                sobelsOfGreenSquares = np.sqrt(np.add(np.power(np.sum(greenSquares * sobelX, axis=(2, 3)), 2), np.power(np.sum(greenSquares * sobelY, axis=(2, 3)), 2)))
                sobelsOfBlueSquares = np.sqrt(np.add(np.power(np.sum(blueSquares * sobelX, axis=(2, 3)), 2), np.power(np.sum(blueSquares * sobelY, axis=(2, 3)), 2)))
            elif sobelVariant == "1":
                sobelsOfRedSquares, sobelsOfGreenSquares, sobelsOfBlueSquares = np.sum(redSquares * sobelY, axis=(2, 3)), np.sum(greenSquares * sobelY, axis=(2, 3)), np.sum(blueSquares * sobelY, axis=(2, 3))
            elif sobelVariant == "2":
                sobelsOfRedSquares, sobelsOfGreenSquares, sobelsOfBlueSquares = np.sum(redSquares * sobelX, axis=(2, 3)), np.sum(greenSquares * sobelX, axis=(2, 3)), np.sum(blueSquares * sobelX, axis=(2, 3))
            else:
                raise Exception("Nie ma takiej opcji Sobela")
            # przypisanie sobeli do srodowych wartosci w macierzach
            if padding:
                self.pixels[:, :, 0][:, :], self.pixels[:, :, 1][:, :], self.pixels[:, :, 2][:, :] = sobelsOfRedSquares, sobelsOfGreenSquares, sobelsOfBlueSquares
            else:
                self.pixels[:, :, 0][1:-1, 1:-1], self.pixels[:, :, 1][1:-1, 1:-1], self.pixels[:, :, 2][1:-1, 1:-1] = sobelsOfRedSquares, sobelsOfGreenSquares, sobelsOfBlueSquares
            self.limitPixelsAndShowImage(self.pixels, True)
        self.measureTime("END")

    def highPassSharpeningFilter(self, dim=3, padding=True):
        self.measureTime("START")
        if self.image:
            height, width, _ = self.pixels.shape
            highPassPixels = deepcopy(self.pixels)
            if dim == 3:
                highPassMask = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                # highPassMask = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                if padding:
                    pad_size = 3 // 2
                    paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                    for y in range(height):
                        for x in range(width):
                            for c in range(3):  # Loop over R, G, and B channels
                                    highPassPixels[y, x, c] = np.sum(paddedImage[y:y+3, x:x+3, c] * highPassMask)
                else:
                    for y in range(1, height-1):
                        for x in range(1, width-1):
                            for c in range(3):  # Loop over R, G, and B channels
                                    highPassPixels[y, x, c] = np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * highPassMask)
            elif dim == 5:
                highPassMask = np.array([[-1, -1, -1, -1, -1], [-1, 1, 2, 1, -1], [-1, 2, 5, 2, -1], [-1, 1, 2, 1, -1], [-1, -1, -1, -1, -1]])
                if padding:
                    pad_size = 5 // 2
                    paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                    for y in range(height):
                        for x in range(width):
                            for c in range(3):  # Loop over R, G, and B channels
                                    highPassPixels[y, x, c] = np.sum(paddedImage[y:y+5, x:x+5, c] * highPassMask)
                else:
                    for y in range(2, height-2):
                        for x in range(2, width-2):
                            for c in range(3):  # Loop over R, G, and B channels
                                    highPassPixels[y, x, c] = np.sum(self.pixels[y - 2:y + 3, x - 2:x + 3, c] * highPassMask)
            else:
                raise Exception("Nie ma takiej opcji")
            self.limitPixelsAndShowImage(highPassPixels, True)
        self.measureTime("END")

    def highPassSharpeningFilterOptimized(self, dim=3, padding=True):
        self.measureTime("START")
        if self.image:
            if self.pixels.shape < (dim, dim, 3):
                print("Nie mozna nalozyc maski jesli wymiar obrazu jest ponizej 3x3")
                return
            if dim == 3:
                highPassMask = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                #highPassMask = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            elif dim == 5:
                highPassMask = np.array([[-1, -1, -1, -1, -1], [-1, 1, 2, 1, -1], [-1, 2, 5, 2, -1], [-1, 1, 2, 1, -1], [-1, -1, -1, -1, -1]])
            else:
                raise Exception("Nie ma takiej opcji")
            # wyciecie wartosci czerwonych, zielonych i niebieskich pixeli osobno
            if padding:
                pad_size = dim // 2
                paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                reds, greens, blues = paddedImage[:, :, 0], paddedImage[:, :, 1], paddedImage[:, :, 2]
            else:
                reds, greens, blues = self.pixels[:, :, 0], self.pixels[:, :, 1], self.pixels[:, :, 2]
            # stworzenie macierz dim x dim z sasiadujacych wartosci dla kazdej grupy
            redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (dim, dim)), np.lib.stride_tricks.sliding_window_view(greens, (dim, dim)), np.lib.stride_tricks.sliding_window_view(blues, (dim, dim))
            # wyliczenie highpass z kazdej macierzy
            highpassesOfRedSquares, highpassesOfGreenSquares, highpassesOfBlueSquares = np.sum(redSquares * highPassMask, axis=(2, 3)), np.sum(greenSquares * highPassMask, axis=(2, 3)), np.sum(blueSquares * highPassMask, axis=(2, 3))
            # przypisanie highpass do srodowych wartosci w macierzach
            if padding:
                self.pixels[:, :, 0][:, :], self.pixels[:, :, 1][:, :], self.pixels[:, :, 2][:, :] = highpassesOfRedSquares, highpassesOfGreenSquares, highpassesOfBlueSquares
            else:
                start = int(dim/2)
                end = -1 * start
                self.pixels[:, :, 0][start:end, start:end], self.pixels[:, :, 1][start:end, start:end], self.pixels[:, :, 2][start:end, start:end] = highpassesOfRedSquares, highpassesOfGreenSquares, highpassesOfBlueSquares
            self.limitPixelsAndShowImage(self.pixels, True)
        self.measureTime("END")

    def gaussianBlurFilter(self, dim=5, simplified=True, padding=True):
        self.measureTime("START")
        if self.image:
            height, width, _ = self.pixels.shape
            gaussianBlurPixels = deepcopy(self.pixels)
            if simplified:
                gaussianBlurMask = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
                if padding:
                    pad_size = 3 // 2
                    paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                    for y in range(height):
                        for x in range(width):
                            for c in range(3):  # Loop over R, G, and B channels
                                gaussianBlurPixels[y, x, c] = np.sum(paddedImage[y:y + 3, x:x + 3, c] * gaussianBlurMask / 16)
                else:
                    for y in range(1, height - 1):
                        for x in range(1, width - 1):
                            for c in range(3):  # Loop over R, G, and B channels
                                gaussianBlurPixels[y, x, c] = np.sum(self.pixels[y - 1:y + 2, x - 1:x + 2, c] * gaussianBlurMask / 16)
            # DZIWNIE SIE ZACHOWUJE, przesuwa obraz jakby w lewy gorny rog
            # else:
            #     if dim % 2 == 0:
            #         raise Exception("Size of kernel should be odd")
            #     gaussianBlurMask = np.zeros((dim, dim))
            #     halfDim = int(dim / 2)
            #     sigma = 1.0 #0.84089642
            #     sumGaussElements = 0
            #     for x in range(-1*halfDim, halfDim+1):
            #         for y in range(-1*halfDim, halfDim+1):
            #             # gaussianBlurMask[x, y] = np.exp(-0.5 * np.power((x-mean)/sigma, 2) + np.power((y-mean)/sigma, 2)) / (2 * np.pi * sigma * sigma)
            #             gaussianBlurMask[x+halfDim, y+halfDim] = np.exp((np.power(x-halfDim, 2.0) + np.power(y-halfDim, 2.0)) / (-2 * (sigma * sigma))) / (2 * np.pi * sigma * sigma)
            #             #print(f"X={x+halfDim} Y={y+halfDim} eX={eX} G={gaussianBlurMask[x+halfDim, y+halfDim]}")
            #             sumGaussElements += gaussianBlurMask[x+halfDim, y+halfDim]
            #     #print(f"SUMA = {sumGaussElements}")
            #     #normalizacja
            #     for x in range(dim):
            #         for y in range(dim):
            #             gaussianBlurMask[x, y] = gaussianBlurMask[x, y] / sumGaussElements
            #     print(gaussianBlurMask)
            #     for y in range(halfDim, height - halfDim):
            #         for x in range(halfDim, width - halfDim):
            #             for c in range(3):  # Loop over R, G, and B channels
            #                 gaussianBlurPixels[y, x, c] = np.sum(self.pixels[y - halfDim:y + halfDim+1, x - halfDim:x + halfDim+1, c] * gaussianBlurMask)
            self.limitPixelsAndShowImage(gaussianBlurPixels, True)
        self.measureTime("END")

    def gaussianBlurFilterOptimized(self, dim=3, simplified=True, padding=False):
        self.measureTime("START")
        if self.image:
            if simplified:
                gaussianBlurMask = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
                if padding:
                    pad_size = 3 // 2
                    paddedImage = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
                    reds, greens, blues = paddedImage[:, :, 0], paddedImage[:, :, 1], paddedImage[:, :, 2]
                    redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (3, 3)), np.lib.stride_tricks.sliding_window_view(greens, (3, 3)), np.lib.stride_tricks.sliding_window_view(blues, (3, 3))
                    gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares = np.sum(redSquares * gaussianBlurMask / 16, axis=(2, 3)), np.sum(greenSquares * gaussianBlurMask / 16, axis=(2, 3)), np.sum(blueSquares * gaussianBlurMask / 16, axis=(2, 3))
                    self.pixels[:, :, 0][:, :], self.pixels[:, :, 1][:, :], self.pixels[:, :, 2][:, :] = gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares
                else:
                    reds, greens, blues = self.pixels[:, :, 0], self.pixels[:, :, 1], self.pixels[:, :, 2]
                    redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (3, 3)), np.lib.stride_tricks.sliding_window_view(greens, (3, 3)), np.lib.stride_tricks.sliding_window_view(blues, (3, 3))
                    gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares = np.sum(redSquares * gaussianBlurMask / 16, axis=(2, 3)), np.sum(greenSquares * gaussianBlurMask / 16, axis=(2, 3)), np.sum(blueSquares * gaussianBlurMask / 16, axis=(2, 3))
                    self.pixels[:, :, 0][1:-1, 1:-1], self.pixels[:, :, 1][1:-1, 1:-1], self.pixels[:, :, 2][1:-1, 1:-1] = gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares # without padding
                    print("WYkonalo sie")
            # DZIWNIE SIE ZACHOWUJE, przesuwa obraz jakby w lewy gorny rog
            # else:
            #     if dim % 2 == 0:
            #         raise Exception("Size of kernel should be odd")
            #     # gaussian function
            #     gaussianBlurMask = np.zeros((dim, dim))
            #     halfDim = int(dim / 2)
            #     minusHalfDim = -1 * halfDim
            #     sigma = 0.84089642
            #     sumGaussElements = 0
            #     for x in range(-1 * halfDim, halfDim + 1):
            #         for y in range(-1 * halfDim, halfDim + 1):
            #             gaussianBlurMask[x + halfDim, y + halfDim] = np.exp((np.power(x - halfDim, 2.0) + np.power(y - halfDim, 2.0)) / (-2 * (sigma * sigma))) / (2 * np.pi * sigma * sigma)
            #             sumGaussElements += gaussianBlurMask[x + halfDim, y + halfDim]
            #     # normalization
            #     for x in range(dim):
            #         for y in range(dim):
            #             gaussianBlurMask[x, y] = gaussianBlurMask[x, y] / sumGaussElements
            #     #padding
            #     pad_size = dim // 2
            #     padded_image = np.pad(self.pixels, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
            #     #
            #     reds, greens, blues = padded_image[:, :, 0], padded_image[:, :, 1], padded_image[:, :, 2]
            #     redSquares, greenSquares, blueSquares = np.lib.stride_tricks.sliding_window_view(reds, (dim, dim)), np.lib.stride_tricks.sliding_window_view(greens, (dim, dim)), np.lib.stride_tricks.sliding_window_view(blues, (dim, dim))
            #     gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares = np.sum(redSquares * gaussianBlurMask, axis=(2, 3)), np.sum(greenSquares * gaussianBlurMask, axis=(2, 3)), np.sum(blueSquares * gaussianBlurMask, axis=(2, 3))
            #     self.pixels[:, :, 0][0:, 0:], self.pixels[:, :, 1][0:, 0:], self.pixels[:, :, 2][0:, 0:] = gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares
            #     start = int(dim / 2)  # without padding
            #     end = -1 * start  # without padding
            #     self.pixels[:, :, 0][start:end, start:end], self.pixels[:, :, 1][start:end, start:end], self.pixels[:, :, 2][start:end, start:end] = gaussianBlurOfRedSquares, gaussianBlurOfGreenSquares, gaussianBlurOfBlueSquares  # without padding
            self.limitPixelsAndShowImage(self.pixels, True)
        self.measureTime("END")

    def doPointTransformation(self):
        if self.operationType.get() != 'lightness':
            self.hsvPixels = None
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

    def hsvBackup(self, reds, greens, blues):
        if self.hsvPixels is None:
            h, s, v = np.vectorize(self.convertRGBtoHSV)(reds, greens, blues)
            self.hsvPixels = np.dstack((h, s, v))
            # print(self.hsvPixels)
        return self.hsvPixels[:, :, 0], self.hsvPixels[:, :, 1], self.hsvPixels[:, :, 2]

    def changeLightness(self):
        self.measureTime("START")
        if self.image:
            reds = self.pixels[:, :, 0]
            greens = self.pixels[:, :, 1]
            blues = self.pixels[:, :, 2]
            # h, s, v = np.vectorize(self.convertRGBtoHSV)(reds, greens, blues)
            h, s, v = self.hsvBackup(reds, greens, blues)
            v *= max(0, min(255, float(self.lightChangeEntry.get())))
            r, g, b = np.vectorize(self.convertHSVtoRGB)(h, s, v)
            self.pixels[:, :, 0] = r
            self.pixels[:, :, 1] = g
            self.pixels[:, :, 2] = b
            self.limitPixelsAndShowImage(self.pixels, False)
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
        self.imageSpace.lower(self.imageId)
        self.imageSpace.imagetk = imagetk
        # self.movedX = 0
        # self.movedY = 0

    def loadJPG(self):
        filePath = askopenfilename()
        if filePath == '':
            return
        self.image = Image.open(filePath)
        if self.image is None:
            return
        self.pixels = np.array(self.image, dtype=np.int32)
        self.originalImage = deepcopy(self.image)
        self.hsvPixels = None
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.settingsAfterLoad()

    def reloadOriginalJPG(self):
        if self.originalImage:
            self.image = deepcopy(self.originalImage)
            if self.image is None:
                return
            self.hsvPixels = None
            self.pixels = np.array(self.image, dtype=np.int32)
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
