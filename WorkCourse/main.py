import pandas as pd

from WorkCourse.analyze_video import videoAnalyze, data2BboxList, \
    bboxPredictAnalyze


def main():
    # cutBboxFromVideo('ch01_20200703110241.mp4',
    #          'result_annotations_ch01_20200703110241.csv')
    # count_IOU('result_annotations_ch01_20200703110241.csv')
    # calculate_iou([0, 0, 0, 0], [1311, 522, 1322, 531])
    # videoAnalyze('ch01_20200703110241.mp4',
    #              'result_annotations_ch01_20200703110241.csv')

    data = pd.read_csv('result_annotations_ch01_20200703110241.csv')
    dataFrame = data[data['frame'] == 3858]
    trueBboxList: list[list[int]] = data2BboxList(dataFrame)
    print(bboxPredictAnalyze([1844, 625, 47, 33],trueBboxList))

    # videoAnalyze2('ch01_20200703110241.mp4')


if __name__ == "__main__":
    main()
