import torch
from PIL import Image

class GetBoxes():
    def __init__(self, modelDir):
        self.modelDir = modelDir
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')
        
    def getBoundingData(self, imgPath):
        boxes = []

        image = Image.open(imgPath)
        results = self.model(image).pandas().xyxy

        for i in range(len(results)):
            imgData = results[i]
            
            for j in range(len(imgData.name)):
                if imgData.confidence[j] > .5:
                    label = imgData.name[j]
                    minX = imgData.xmin[j] / image.width
                    minY = imgData.ymin[j] / image.height
                    maxX = imgData.xmax[j] / image.width
                    maxY = imgData.ymax[j] / image.height

                    print([label, minX, minY, maxX, maxY])
                    boxes.append([label, minX, minY, maxX, maxY])

        return boxes