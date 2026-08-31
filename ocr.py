import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def ocr_text(image):
    image = np.array(image)
    result = reader.readtext(image, detail=1)
    lines = []

    for box, text, confidence in result:
        x = sum(point[0] for point in box) / 4
        y = sum(point[1] for point in box) / 4

        lines.append((y, x, text))

    lines.sort(key=lambda item: (item[0], item[1]))

    text = " ".join(item[2].strip() for item in lines)

    return(text)