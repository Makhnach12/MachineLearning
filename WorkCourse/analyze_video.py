import pandas as pd
import os
import cv2 as cv
from IOU import calculateIOU

# from detector import DetectorSSD

# переменная для оценивания совпадения bbox по iou
bboxIdentity: float = 0.7


def makeBboxInt(bbox: tuple):
    """Функция округляет значения bbox"""
    return [int(elem) for elem in bbox]


def cutBboxFromVideo(video_file, datatable_file) -> None:
    """Функция вырезает bbox и сохраняет в папку"""
    data = pd.read_csv(datatable_file)
    cap = cv.VideoCapture(video_file)

    fileName: str = 'Results'
    if not os.path.isdir(fileName):
        os.mkdir(fileName)

    idx: int = 0
    frameNumber: int = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frameNumber += 1
        if frameNumber != data['frame'][idx]:
            continue
        # TODO: спросить про отрицательные координаты
        elif data['x'][idx] < 0 or data['y'][idx] < 0:
            idx += 1
            continue
        bbox: list = [data['x'][idx], data['y'][idx],
                      data['w'][idx], data['h'][idx]]
        if ret:
            saveBbox(frame, fileName, bbox, frameNumber)
        idx += 1
    cap.release()
    cv.destroyAllWindows()


def data2BboxList(data) -> list:
    """Функция для перевода данных таблицы в лист с координатами bbox"""
    allBboxes: list = list()
    for i in range(len(data)):
        bbox: list = [data['x'].iloc[i], data['y'].iloc[i],
                      data['w'].iloc[i], data['h'].iloc[i]]
        allBboxes.append(bbox)
    return allBboxes


def bboxPredictAnalyze(bboxPredict: list, bboxesReal: list):
    """Функция сравнивает по IOU bbox который вернул детектор с каждым
    bbox из разметки кадра и возвращает Bbox если нашла два похожих"""
    for bboxReal in bboxesReal:
        # TODO: подумать насколько должны совпадать bbox
        if calculateIOU(bboxPredict, bboxReal) >= bboxIdentity:
            return bboxReal
    return None


def saveBbox(frame, filename, bbox, frameNumber):
    """Функция сохраняет bbox в папке с именем filename"""
    cropped = frame[bbox[1]:bbox[1] + bbox[3],
              bbox[0]:bbox[0] + bbox[2]]
    frameFilename: str = os.path.join(filename, f"frame{frameNumber}.jpg")
    cv.imwrite(frameFilename, cropped)


def saveFrame(frame, filename, bbox, frameNumber):
    """Функция сохраняет bbox в папке с именем filename"""
    frameFilename: str = os.path.join(filename, f"frame{frameNumber}_full.jpg")
    cv.rectangle(frame, (bbox[0], bbox[1]),
                 (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                 color=(0, 255, 0), thickness=3)
    cv.imwrite(frameFilename, frame)


def videoAnalyze(videoFile, datatableFile) -> None:
    """Функция сохраняет bbox в какой-либо из папок BadPredicts |
    GoodPredicts в зависимости от результатов сравнения итоговых данных с
    данными детектора"""
    cap = cv.VideoCapture(videoFile)
    data = pd.read_csv(datatableFile)
    # detector = DetectorSSD(0.5, 0.7)
    GoodPredictsFileName: str = 'GoodPredicts'
    BadPredictsFileName: str = 'BadPredicts'
    if not os.path.isdir(GoodPredictsFileName):
        os.mkdir(GoodPredictsFileName)
    if not os.path.isdir(BadPredictsFileName):
        os.mkdir(BadPredictsFileName)
    frameNumber: int = 1
    while cap.isOpened():

        ret, frame = cap.read()
        # _, bboxList = detector.get_bboxes(frame)
        dataFrame = data[data['frame'] == frameNumber]

        trueBboxList = data2BboxList(dataFrame)
        # TODO: заменить на bboxList
        # copiedList: list[list[int]] = [[1844, 625, 47, 33]]
        bboxList = [[1844, 625, 47, 33]]
        # for bbox in copiedList:

        for bbox in bboxList:
            bboxAns = bboxPredictAnalyze(bbox, trueBboxList)
            if bboxAns:
                saveBbox(frame, GoodPredictsFileName, bboxAns, frameNumber)
                print("Good:", bboxAns, trueBboxList, bboxList)
            else:
                saveBbox(frame, BadPredictsFileName, bbox, frameNumber)
                print("Bad:", bbox, trueBboxList, bboxList)
        frameNumber += 1
    cap.release()
    cv.destroyAllWindows()


def videoCheck(videoFile, datatableFile) -> None:
    cap = cv.VideoCapture(videoFile)
    data = pd.read_csv(datatableFile)
    bboxFileName: str = 'Bbox'
    frameFileName: str = 'Frames'
    if not os.path.isdir(bboxFileName):
        os.mkdir(bboxFileName)
    if not os.path.isdir(frameFileName):
        os.mkdir(frameFileName)
    frameNumber: int = 1
    while cap.isOpened():
        ret, frame = cap.read()
        dataFrame = data[data['frame'] == frameNumber]
        trueBboxList = data2BboxList(dataFrame)
        for bbox in trueBboxList:
            print('yes')
            print(bbox)
            saveBbox(frame, bboxFileName, makeBboxInt(bbox), frameNumber)
            saveFrame(frame, frameFileName, makeBboxInt(bbox), frameNumber)
        frameNumber += 1
    cap.release()
    cv.destroyAllWindows()

def checkData(datatableFile1, datatableFile2):
    data1 = pd.read_csv(datatableFile1)
    data2 = pd.read_csv(datatableFile2)
    for i in range(1, 10000):
        dataFrame1 = data1[data1['frame'] == i]
        dataFrame2 = data2[data2['frame'] == i]
        trueBboxList1 = data2BboxList(dataFrame1)
        trueBboxList2 = data2BboxList(dataFrame2)
        if trueBboxList1 != trueBboxList2:
            print(trueBboxList1, trueBboxList2)
            print('NO')
