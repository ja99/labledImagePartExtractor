import datetime
import glob
import json
import pprint
from tqdm import tqdm

from PIL import Image, ImageDraw, ImageFilter

MIN_SIZE = 80


counter = 0
for path in tqdm(glob.iglob(f'ULM_Bounding_Boxes_Blurred/ULM/img/*.jpg', recursive=True)):
    img = Image.open(path)

    label_path = str(path.replace("img", "ann").replace(".jpg", ".jpg.json"))
    lables: dict
    with open(label_path, "r") as f:
        lables = json.load(f)

    for obj in lables["objects"]:
        if not obj["tags"] == []:
            continue

        class_label = obj["classTitle"]
        points = obj["points"]["exterior"]

        if points[1][0] - points[0][0] < MIN_SIZE or points[1][1] - points[0][1] < MIN_SIZE:
            continue

        img_obj = img.copy()
        img_obj = img_obj.crop((points[0][0], points[0][1], points[1][0], points[1][1]))

        img_obj.save(f"output/{class_label}___{counter}.png", quality=100)
        counter += 1
