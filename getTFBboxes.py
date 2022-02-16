import torch
from PIL import Image
import numpy as np

class GetTFBBoxes():
    def __init__(self, modelDir, labelMapPath):
        self.modelDir = modelDir
        self.labelMapPath = labelMapPath
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')
        

    def load_image_into_numpy_array(self, path):
    
        return np.array(Image.open(path))

    def getBBoxData(self, imgPath):

        tfBoxes = []

        image = Image.open(imgPath)
        results = self.model(image).pandas().xyxy[]

        for i in range(len(results)):
            boxes = results[i]['boxes']
            labels = results[i]['labels']
            scores = results[i]['scores']
            for box, label, score in zip(boxes, labels, scores):
                tfBoxes.append([label.item(), box[0].item(), box[1].item(), box[2].item(), box[3].item(), score.item()])

        return results.pandas().xyxy[0].confidence[0]

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(results.pop('num_detections'))
        results = {key: value[0, :num_detections].numpy()
                        for key, value in results.items()}
        results['num_detections'] = num_detections
        #print("Detection num " + str(detections['num_detections']))

        # detection_classes should be ints.
        results['detection_classes'] = results['detection_classes'].astype(np.int64)

        for j in range(len(results['detection_scores'])):
            if(results['detection_scores'][j] > .98):
                (ymin, xmin, ymax, xmax) = tuple(results['detection_boxes'][j])
                detectionName = self.labelMapPath[int(results['detection_classes'][j]) - 1]
                tfBoxes.append((detectionName, xmin, xmax, ymin, ymax))

        return tfBoxes