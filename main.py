import cv2

# Распознание губ на видео с вебкамеры
# Подключить каскад для поиска губ
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
# mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye.xml")

# Если каскад не был найден
if mouth_cascade.empty():
    raise IOError('Unable to load the mouth cascade classifier xml file')

# Подключение камеры
cap = cv2.VideoCapture(0)

# Цикл для постоянного считывания с камеры
while True:
    ret, frame = cap.read()

    # Показать кадр
    cv2.imshow('Mouth Detector', frame)

    # Закрытие окна при нажатии Esc
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
