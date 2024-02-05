def reformBbox(bbox: tuple) -> list:
    """Функция переводит bbox из формата x,y,w,h в x,y,x+w,y+h"""
    bboxCopy = [bbox[0], bbox[1], bbox[2], bbox[3]]
    bboxCopy[2] = bboxCopy[2] + bboxCopy[0]
    bboxCopy[3] = bboxCopy[3] + bboxCopy[1]
    return bboxCopy


def calculateIOU(bboxPredict, bboxTrue) -> float:
    """Функция вычисляющая IOU"""
    bboxPredictCopy = reformBbox(bboxPredict)
    bboxTrueCopy = reformBbox(bboxTrue)

    intersectionWidth: int = min(bboxPredictCopy[2], bboxTrueCopy[2]) - max(
        bboxPredictCopy[0], bboxTrueCopy[0])
    intersectionHeight: int = min(bboxPredictCopy[3], bboxTrueCopy[3]) - max(
        bboxPredictCopy[1], bboxTrueCopy[1])

    if intersectionWidth <= 0 or intersectionHeight <= 0:
        return 0

    intersectionArea: int = intersectionWidth * intersectionHeight

    boxPredArea: int = (bboxPredictCopy[2] - bboxPredictCopy[0]) * (
                bboxPredictCopy[3] - bboxPredictCopy[1])
    boxTrueArea: int = (bboxTrueCopy[2] - bboxTrueCopy[0]) * (bboxTrueCopy[3] -
                                                              bboxTrueCopy[1])
    unionArea: int = boxPredArea + boxTrueArea - intersectionArea

    iou: float = intersectionArea / unionArea
    return iou
