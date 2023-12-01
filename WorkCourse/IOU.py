def calculate_iou(bboxPredict, bboxesTrue) -> float:
    """Функция вычисляющая IOU"""
    intersection_width: int = min(bboxPredict[2], bboxesTrue[2]) - max(
        bboxPredict[0], bboxesTrue[0])
    intersection_height: int = min(bboxPredict[3], bboxesTrue[3]) - max(
        bboxPredict[1], bboxesTrue[1])

    if intersection_width <= 0 or intersection_height <= 0:
        return 0

    intersection_area: int = intersection_width * intersection_height

    box_pred_area: int = (bboxPredict[2] - bboxPredict[0]) * (bboxPredict[3] -
                                                              bboxPredict[1])
    box_true_area: int = (bboxesTrue[2] - bboxesTrue[0]) * (bboxesTrue[3] -
                                                            bboxesTrue[1])
    union_area: int = box_pred_area + box_true_area - intersection_area

    # Calculate IoU
    iou: float = intersection_area / union_area
    return iou