from WorkCourse.analyze_video import videoAnalyze


def main():
    # cut_bbox('ch01_20200703110241.mp4',
    #          'result_annotations_ch01_20200703110241.csv')
    # count_IOU('result_annotations_ch01_20200703110241.csv')
    # calculate_iou([0, 0, 0, 0], [1311, 522, 1322, 531])
    videoAnalyze('ch01_20200703110241.mp4',
                 'result_annotations_ch01_20200703110241.csv')


if __name__ == "__main__":
    main()
