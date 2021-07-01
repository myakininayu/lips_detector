import cv2

# Подключить каскад для поиска губ
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

# Если каскад не был найден
if mouth_cascade.empty():
    raise IOError('Unable to load the mouth cascade classifier xml file')

# Подключение камеры
cap = cv2.VideoCapture(0)

# Цикл для постоянного считывания с камеры
while True:
    ret, frame = cap.read()
    # Перевод изображения в чб формат
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Распознание губ
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)

    # Отрисовать рамку
    # Для каждых губ
    for (x, y, w, h) in mouth_rects:
        # Задать рамку
        y = int(y - 0.15 * h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Показать кадр
    cv2.imshow('Mouth Detector', frame)

    # Закрытие окна при нажатии Esc
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()

