import cv2
import numpy as np
import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def read_image(image_path):
    """Read image with OpenCV, fallback to Pillow for HEIC etc."""
    img = cv2.imread(image_path)
    if img is not None:
        return img
    try:
        pil_img = Image.open(image_path)
        rgb = np.array(pil_img.convert("RGB"))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(
            f"Cannot read the image with OpenCV or Pillow: {image_path}\n"
            f"Pillow error: {e}"
        )


def grade_submission(image_path, answer_key_dict):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = read_image(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubbles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 5000:
            x, y, w, h = cv2.boundingRect(cnt)
            bubbles.append((x, y, w, h))

    bubbles = sorted(bubbles, key=lambda b: (b[1], b[0]))

    rows = []
    current_row = []
    last_y = None
    threshold_y = 15
    for (x, y, w, h) in bubbles:
        if last_y is None or abs(y - last_y) <= threshold_y:
            current_row.append((x, y, w, h))
        else:
            rows.append(sorted(current_row, key=lambda b: b[0]))
            current_row = [(x, y, w, h)]
        last_y = y
    if current_row:
        rows.append(sorted(current_row, key=lambda b: b[0]))

    student_answers = {}
    for q_num, row in enumerate(rows, 1):
        if len(row) < 4:
            continue
        max_filled = -1
        chosen = None
        for i, (x, y, w, h) in enumerate(row[:4]):   # only first 4 bubbles
            roi = thresh[y : y + h, x : x + w]
            filled = cv2.countNonZero(roi)
            if filled > max_filled:
                max_filled = filled
                chosen = ["A", "B", "C", "D"][i]
        student_answers[str(q_num)] = chosen

    correct = 0
    results = []
    for q_num, correct_ans in answer_key_dict.items():
        student_ans = student_answers.get(q_num, "Unanswered")
        is_correct = (student_ans == correct_ans)
        if is_correct:
            correct += 1
        results.append({
            "question": q_num,
            "correct_answer": correct_ans,
            "your_answer": student_ans,
            "correct": is_correct,
        })

    return correct, results, student_answers