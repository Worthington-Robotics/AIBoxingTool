import tensorflow as tf
from PIL import Image
import numpy as np

class GetTFBBoxes():
    def __init__(self, modelDir, labelMapPath):
        self.modelDir = modelDir
        self.labelMapPath = labelMapPath
        self.detect_fn = tf.saved_model.load(self.modelDir)
        

    def load_image_into_numpy_array(self, path):
    
        return np.array(Image.open(path))

    def getBBoxData(self, imgPath):

        tfBoxes = []

        image = Image.open(imgPath)

        image_np = self.load_image_into_numpy_array(imgPath)

        # image_np = np.array(np.random.random_sample((3, 300, 300)), dtype=np.float32)

        input_tensor = tf.convert_to_tensor(image_np, name='input_0')

        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # input_tensor = np.expand_dims(image_np, 0)
        detections = self.detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                        for key, value in detections.items()}
        detections['num_detections'] = num_detections
        #print("Detection num " + str(detections['num_detections']))

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        for j in range(len(detections['detection_scores'])):
            if(detections['detection_scores'][j] > .98):
                (ymin, xmin, ymax, xmax) = tuple(detections['detection_boxes'][j])
                detectionName = self.labelMapPath[int(detections['detection_classes'][j]) - 1]
                tfBoxes.append((detectionName, xmin, xmax, ymin, ymax))

        return tfBoxes

# if __name__ == "__main__":
#     PATH_TO_MODEL_DIR = "C:/Users/markc/Documents/Vision Stuff/TrainedModel/200k_odd" + "/saved_model"
#     PATH_TO_LABEL_MAP = "C:/Users/markc/Documents/Vision Stuff/Tensorflow/workspace/training_demo/annotations/label_map.pbtxt"
#     IMG_DIR = 'C:/Users/markc/Documents/33' + '/20210209_162428_Burst04.jpg'
#     test = GetTFBBoxes(PATH_TO_MODEL_DIR, PATH_TO_LABEL_MAP, IMG_DIR)
#     print(test.getBBoxData())
                