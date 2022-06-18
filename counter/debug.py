import os
from pathlib import Path

from PIL import ImageDraw, ImageFont


def draw(predictions, image, image_name):
    draw_image = ImageDraw.Draw(image, "RGBA")

    image_width, image_height = image.size
    basedir = str(Path(__file__).parent.parent)
    font = ImageFont.truetype(os.path.join(basedir, "counter/resources/arial.ttf"), 20)
    i = 0
    for prediction in predictions:
        box = prediction.box
        draw_image.rectangle(
            [(box.xmin * image_width, box.ymin * image_height),
             (box.xmax * image_width, box.ymax * image_height)],
            outline='red')
        class_name = prediction.class_name
        draw_image.text(
            (box.xmin * image_width, box.ymin * image_height - font.getsize(class_name)[1]),
            f"{class_name}: {prediction.score}", font=font, fill='black')
        i += 1
    try:
        os.mkdir(os.path.join(basedir, 'tmp/debug'))
    except OSError:
        pass
    image.save(os.path.join(basedir, f"tmp/debug/{image_name}"), "JPEG")
