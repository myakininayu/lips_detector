import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox as mb
import cv2
import pafy

# Подключить каскад для поиска губ
def connectCascade(cascadeName):
    mouth_cascade = cv2.CascadeClassifier(cascadeName)

    # Если каскад не был найден
    if mouth_cascade.empty():
        raise IOError('Unable to load the mouth cascade classifier xml file')
    return mouth_cascade

# Распознать губы
def findLips(mouth_cascade, frame):
    # Перевод изображения в чб формат
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Распознание губ
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)

    # Отрисовать рамку
    drawFrame(frame, mouth_rects)

    # Показать кадр
    cv2.imshow('Mouth Detector', frame)

# Отрисовать рамку
def drawFrame(frame, mouth_rects):
    # Для каждых губ
    for (x, y, w, h) in mouth_rects:
        # Задать рамку
        y = int(y - 0.15 * h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Закрыть окно при нажатии Esc
def closeWindow():
        c = cv2.waitKey(1)
        if c == 27:
            return True

# Распознание губ на фото
def findLipsOnPhoto(filename):
    try:
        # Подключить каскад для поиска губ
        mouth_cascade = connectCascade('haarcascade_mcs_mouth.xml')

        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Распознание губ
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)

        # Отрисовать рамку
        drawFrame(img, mouth_rects)

        while True:
            # Показать изображение
            cv2.imshow('Mouth Detector', img)

            # Закрытие окна при нажатии Esc
            if (closeWindow()): break


        cv2.destroyAllWindows()
        window.focus()
    except cv2.error:
        errorMsg = mb.showerror(
            title="Сообщение об ошибке",
            message="Некорректное название файла. Возможно, не на латинице.")


# Распознание губ на видео
def findLipsOnVideoFile(filename):
    # Подключить каскад для поиска губ
    mouth_cascade = connectCascade('haarcascade_mcs_mouth.xml')

    cap = cv2.VideoCapture(filename)
    # Пока видео открыто
    while cap.isOpened():
        ret, frame = cap.read()
        findLips(mouth_cascade, frame)

        # Закрытие окна при нажатии Esc
        if(closeWindow()): break

    cap.release()
    cv2.destroyAllWindows()

# Распознание губ на видео с вебкамеры
def findLipsOnVebcam():
    # Подключить каскад для поиска губ
    mouth_cascade = connectCascade('haarcascade_mcs_mouth.xml')

    # Подключение камеры
    cap = cv2.VideoCapture(0)

    # Цикл для постоянного считывания с камеры
    while True:
        ret, frame = cap.read()
        findLips(mouth_cascade, frame)

        # Закрытие окна при нажатии Esc
        if(closeWindow()): break

    cap.release()
    cv2.destroyAllWindows()
    window.focus()

# Распознание губ на видео по ссылке
def findLipsOnVideoLink(url):
    try:
        urlPafy = pafy.new(url)
        videoplay = urlPafy.getbest()

        if(urlPafy == 0):
            print("Ошибка")

        # Подключить каскад для поиска губ
        mouth_cascade = connectCascade('haarcascade_mcs_mouth.xml')

        cap = cv2.VideoCapture(videoplay.url)
        # Пока видео открыто
        while cap.isOpened():
            ret, frame = cap.read()
            findLips(mouth_cascade, frame)

            # Закрытие окна при нажатии Esc
            if(closeWindow()): break

        cap.release()
        cv2.destroyAllWindows()
    except ValueError:
        errorMsg = mb.showerror(
            title="Сообщение об ошибке",
            message="Некорректное URL видео")
        videoLink.delete(0, 'end')


# Получить режим обработки
def getRes():
    if(cb.get() == "Фото"):
        filetypes = (("Изображение", "*.jpg *.gif *.png"), ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        findLipsOnPhoto(filename)
    elif(cb.get() == "Видеофайл"):
        filetypes = (("Видеофайл", "*.avi *.mp4"), ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        findLipsOnVideoFile(filename)
    elif(cb.get() == "Видео с вебкамеры"):
        findLipsOnVebcam()
    elif (cb.get() == "Видео по ссылке"):
        link = videoLink.get()
        findLipsOnVideoLink(link)

def checkValue(event):
    if (cb.get() == "Фото"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видеофайл"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видео с вебкамеры"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видео по ссылке"):
        linkLabel.pack(anchor=tk.N, side='top', pady=10)
        videoLink.pack(anchor=tk.N, side='top', pady=10)


# Создание окна
window = tk.Tk()
window.title('Mouth Detector')              # Задать заголовок окна
window.geometry('400x230')                  # Задать размер окна
window.wm_resizable(False, False)           # Задать запрет на изменение размера окна
window.iconbitmap("lips_icon.ico")          # Задать иконку окна
window.configure(background='#A44343')      # Задать фон окна

# LABEL
label = ttk.Label(window, text="Выберите формат вх.данных:", background="#FFFFFF", font="Courier 13",
                  width=27)
label.pack(anchor=tk.N, side='top', pady=10)

# LABEL ССЫЛКИ
linkLabel = ttk.Label(window, text="Вставьте ссылку:", background="#FFFFFF", font="Courier 13",
                  width=27)

# ПОЛЕ ССЫЛКИ
myFont = ("Courier", 13)
videoLink = tk.Entry(width=27, font=myFont)

# COMBOBOX
cb = ttk.Combobox(window, values=["Фото", "Видеофайл", "Видео с вебкамеры", "Видео по ссылке"],
                  state="readonly", font=myFont, width=25)
cb.current(2)
cb.pack(anchor=tk.N, side='top', pady=10)
cb.bind("<<ComboboxSelected>>", checkValue)

# BUTTON
btn = ttk.Button(window, text="Выбрать", command=getRes, width=44)
btn.pack(anchor=tk.N, side='top', pady=10)

window.mainloop()