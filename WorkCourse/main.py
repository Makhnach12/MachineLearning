from analyze_video import videoAnalyze, data2BboxList, \
    bboxPredictAnalyze, cutBboxFromVideo, videoCheck, checkData


def main():
    # cutBboxFromVideo('ch01_20200703110241.mp4',
    #          'result_annotations_ch01_20200703110241.csv')
    # videoCheck('ch01_20200703110241_part_1.mp4',
    #          'ch01_20200703110241_part_1.csv')
    checkData('result_annotations_ch01_20200703110241.csv', 'ch01_20200703110241_part_1.csv')
    # count_IOU('result_annotations_ch01_20200703110241.csv')
    # calculate_iou([0, 0, 0, 0], [1311, 522, 1322, 531])
    # videoAnalyze('ch01_20200703110241.mp4',
    #              'result_annotations_ch01_20200703110241.csv')


    # videoAnalyze('ch01_20200703110241.mp4', 'result_annotations_ch01_20200703110241.csv')


if __name__ == "__main__":
    main()
