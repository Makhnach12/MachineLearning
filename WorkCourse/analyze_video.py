import pandas as pd
import os
import cv2 as cv
from typing import Optional
from WorkCourse.IOU import calculateIOU

# from WorkCourse.detector import DetectorSSD
# переменная для оценивания совпадения bbox по iou
bboxIdentity: float = 0.7


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
        bbox: list[int] = [data['x'][idx], data['y'][idx],
                           data['w'][idx], data['h'][idx]]
        if ret:
            saveBbox(frame, fileName, bbox, frameNumber)
        idx += 1
    cap.release()
    cv.destroyAllWindows()


def data2BboxList(data) -> list[list[int]]:
    """Функция для перевода данных таблицы в лист с координатами bbox"""
    allBboxes: list[list[int]] = list()
    for i in range(len(data)):
        bbox: list[int] = [data['x'].iloc[i], data['y'].iloc[i],
                           data['w'].iloc[i], data['h'].iloc[i]]
        allBboxes.append(bbox)
    return allBboxes


def bboxPredictAnalyze(bboxPredict: list[int], bboxesReal: list[list[int]]) \
        -> Optional[list[int]]:
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
        trueBboxList: list[list[int]] = data2BboxList(dataFrame)
        # TODO: заменить на bboxlist
        copiedList: list[list[int]] = [[1844, 625, 47, 33]]
        for bbox in copiedList:
            bboxAns: Optional[list[int]] = bboxPredictAnalyze(bbox,
                                                              trueBboxList)
            if bboxAns:
                saveBbox(frame, GoodPredictsFileName, bboxAns, frameNumber)
            else:
                saveBbox(frame, BadPredictsFileName, bbox, frameNumber)
        frameNumber += 1
    cap.release()
    cv.destroyAllWindows()
