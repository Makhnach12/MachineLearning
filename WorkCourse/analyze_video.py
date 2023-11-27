from moviepy.editor import VideoFileClip
import pandas as pd
import os
from datetime import timedelta
from PIL import Image

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


def cut_bbox(video_file, datatable_file) -> None:
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


def count_IOU(datatable1, datatable2=None) -> None:
    """Функция считает IOU для bbox, координаты которых есть в двух таблицах"""
    data = pd.read_csv(datatable1)
    for i in range(len(data)):
        bbox1: list[int] = [data['x'][i], data['y'][i], data['x'][i] + data[
            'w'][i], data['y'][i] + data['h'][i]]
        # TODO: Заменить создание нового bbox2 на работу детектора
        bbox2: list[int] = [data['x'][i] + 1, data['y'][i] + 1, data['x'][i] +
                            1 + data['w'][i], data['y'][i] + 1 + data['h'][i]]
        print(calculate_iou(bbox1, bbox2))
