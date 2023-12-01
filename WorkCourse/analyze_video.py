from moviepy.editor import VideoFileClip
import pandas as pd
import numpy as np
import os
from datetime import timedelta
from PIL import Image
from typing import Optional

from WorkCourse.IOU import calculate_iou


def format_timedelta(td: timedelta) -> str:
    """Функция для редактирования названий кадров"""
    result: str = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + " 00".replace(":", "-")
    ms = round(int(ms) / 10000)
    return f"{result}. {ms: 02}".replace(":", "-")


def cutBbox(video_file, datatable_file) -> None:
    """Функция вырезает bbox из видео по заданной таблице datatable"""
    data = pd.read_csv(datatable_file)
    video_clip: VideoFileClip = VideoFileClip(video_file)
    filename, _ = os.path.splitext(video_file)
    if not os.path.isdir(filename):
        os.mkdir(filename)
    step: float = 1 / video_clip.fps
    for i, current_frame in enumerate(data['frame']):
        frame_duration_formatted: str = format_timedelta(
            timedelta(seconds=current_frame * step)).replace("", "-")
        frame_filename: str = os.path.join(filename,
                                           f"frame {frame_duration_formatted}.jpg")
        video_clip.save_frame(frame_filename, current_frame * step)
        img: Image = Image.open(frame_filename)
        img_crop: Image = img.crop((data['x'][i], data['y'][i],
                                    data['x'][i] + data['w'][i],
                                    data['y'][i] + data['h'][i]))
        img_crop.save(frame_filename, quality=100)


def saveBbox(video_clip: VideoFileClip, bbox: list[int], filename: str,
             timeClip: float) -> None:
    """Функция сохраняет bbox из видео в нужную папку"""
    frame_duration_formatted: str = format_timedelta(
        timedelta(seconds=timeClip)).replace("", "-")
    frame_filename: str = os.path.join(filename,
                                       f"frame {frame_duration_formatted}.jpg")
    video_clip.save_frame(frame_filename, timeClip)
    img: Image = Image.open(frame_filename)
    img_crop: Image = img.crop(tuple(bbox))
    img_crop.save(frame_filename, quality=100)


def data2BboxList(data) -> list[list[int]]:
    """Функция для перевода данных таблицы в лист с координатами bbox"""
    all_Bboxes: list[list[int]] = list()
    for i in range(len(data)):
        bbox: list[int] = [data['x'].iloc[i], data['y'].iloc[i],
                           data['x'].iloc[i] + data['w'].iloc[i],
                           data['y'].iloc[i] + data['h'].iloc[i]]
        all_Bboxes.append(bbox)
    return all_Bboxes


def bboxPredictAnalyze(bboxPredict: list[int], bboxesReal: list[list[int]]) \
        -> Optional[list[int]]:
    """Функция сравнивает по IOU bbox который вернул детектор с каждым
    bbox из разметки кадра и возвращает True если нашла два похожих"""
    for bboxReal in bboxesReal:
        # TODO: подумать насколько должны совпадать bbox
        if calculate_iou(bboxPredict, bboxReal) >= 0.7:
            return bboxReal
    return None


def videoAnalyze(video_file, datatable_file) -> None:
    """Функция сохраняет bbox в зависимости от результатов сравнения"""
    data = pd.read_csv(datatable_file)
    video_clip: VideoFileClip = VideoFileClip(video_file)
    GoodPredictsFileName: str = 'GoodPredicts'
    BadPredictsFileName: str = 'BadPredicts'
    if not os.path.isdir(GoodPredictsFileName):
        os.mkdir(GoodPredictsFileName)
    if not os.path.isdir(BadPredictsFileName):
        os.mkdir(BadPredictsFileName)
    step: float = 1 / video_clip.fps
    for currDuration in np.arange(0, video_clip.duration, step):
        if int(currDuration * video_clip.fps) in list(data['frame']):
            dataFrame = data[data['frame'] == int(currDuration *
                                                  video_clip.fps)]
            bboxList: list[list[int]] = data2BboxList(dataFrame)
            copiedList = bboxList[0].copy()
            for i in range(len(bboxList)):
                copiedList[i] += 10
            bbox: Optional[list[int]] = bboxPredictAnalyze(copiedList, bboxList)
            # TODO: вместо copiedList должен быть predict детектора
            if bbox:
                saveBbox(video_clip, bbox, GoodPredictsFileName,
                         currDuration)
            else:
                saveBbox(video_clip, copiedList, BadPredictsFileName,
                         currDuration)
