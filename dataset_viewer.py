import os
from pathlib import Path
import argparse

import cv2
import numpy as np


def add_information(image: cv2.UMat , inform: dict) -> cv2.UMat:
    """Adding information on image inplace

    Returns:
        UMat: image with information
    """
    
    title = "info:"
    start_point = [10, 20]

    cv2.putText(image, title, start_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, lineType = cv2.LINE_AA)
    
    size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
    
    start_point[0] += size[0] + 5
    
    for key in inform:
        line = f"{key}:{inform[key]}"
        cv2.putText(image, line, start_point, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,255,0), 1, 
                    lineType = cv2.LINE_AA)
        
        textsize = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

        gap = textsize[1] + 5
        
        start_point[1] += gap
    
    return image

def yolobbox2bbox(x:int , y:int, w:int, h:int) -> tuple[int, int, int, int]:
    """Converter for YOLO bboxes (xywh) to standart bboxes (xyxy)

    Returns:
        tuple: finction is return x1, y1 (left up) and x2, y2 (right low) of bbox.
    """
    
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    
    return x1, y1, x2, y2

def contour2bbox(contour_row):
    return min(contour_row[0::2]), min(contour_row[1::2]), max(contour_row[0::2]), max(contour_row[1::2])

def dataset_viewer(srcl = "./labels", srci = "./images", window_size:tuple[int, int] = (640, 480)):

    srci = Path(srci)
    srcl = Path(srcl)
    
    names = sorted([name.name.replace(".txt", "") for name in os.scandir(srcl)])
    lenght = len(names)

    index = 0
    
    info = {
        "usage": "q - exit, d - delete image, c - clear annotionion",
        "name": f"{names[index]} ({index + 1}/{lenght})", 
        "resolution": None,
    }
    
    colors = {}
    
    while True:
        
        if index < 0:
            index = lenght - 1
        elif index >= lenght:
            index = 0
        
        info["name"] = f"{names[index]} ({index + 1}/{lenght})"
        
        name = names[index]
        lbl = srcl.joinpath(name+".txt").absolute()
        img = srci.joinpath(name+".jpg").absolute()
        
        sh = cv2.imread(img)
        info["resolution"] = sh.shape[0:2]
        sh = cv2.resize(sh, window_size)
        
        for line in open(lbl, "r"):
            cls, *annotation = map(float, line.split(" "))
            
            if cls not in colors:
                colors[cls] = np.random.randint(0, 256, 3).tolist()
            
            if len(annotation) == 4:
                x, y, w, h = annotation
                x1, y1, x2, y2 = yolobbox2bbox(x, y, w, h)
            
            elif len(annotation) > 4:
                x1, y1, x2, y2 = contour2bbox(annotation)
            

            hight, wheight, c = sh.shape
            
            x1, x2 = x1*wheight, x2*wheight
            y1, y2 = y1*hight, y2*hight
            
            sh = cv2.rectangle(sh, (int(x1), int(y1)), (int(x2), int(y2)), colors[cls], 3)
        
        add_information(sh, info)
        cv2.imshow("VIEWER", sh)

        key = cv2.waitKey()
        
        if key == ord('d'):
            os.remove(lbl)
            os.remove(img)
            lenght -= 1
            del names[index]
        
        elif key == ord('c'):
            open(lbl, 'w').close()
        
        elif key == ord('['):
            index -= 1
        elif key == ord(']'):
            index += 1
            
        elif key == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", "-i", help="Path to image folder", required=True)
    parser.add_argument("--labels", "-l", help="Path to label folder", required=True)
    parser.add_argument("--window_size", "-w", help="Size for programm window", nargs=2, default = [640, 420])
    args = parser.parse_args()
    ds_viewer(srci=args.images, srcl=args.labels, window_size=tuple(map(int, args.window_size)))