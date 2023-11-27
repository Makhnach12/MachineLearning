def calculate_iou(boxes_pred, boxes_true) -> float:
    """Функция вычисляющая IOU"""
    intersection_width: int = min(boxes_pred[2], boxes_true[2]) - max(
        boxes_pred[0], boxes_true[0])
    intersection_height: int = min(boxes_pred[3], boxes_true[3]) - max(
        boxes_pred[1], boxes_true[1])

    if intersection_width <= 0 or intersection_height <= 0:
        return 0

    intersection_area: int = intersection_width * intersection_height

    box_pred_area: int = (boxes_pred[2] - boxes_pred[0]) * (boxes_pred[3] -
                                                            boxes_pred[1])
    box_true_area: int = (boxes_true[2] - boxes_true[0]) * (boxes_true[3] -
                                                            boxes_true[1])
    union_area: int = box_pred_area + box_true_area - intersection_area

    # Calculate IoU
    iou: float = intersection_area / union_area

    return iou
