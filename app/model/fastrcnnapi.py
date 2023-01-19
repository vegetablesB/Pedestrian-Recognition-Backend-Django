""" pytorch faster rcnn api for pedestrian detection """
import torch
from PIL import Image

from torchvision import transforms, models
from torchvision.models.detection.faster_rcnn import (
    FastRCNNPredictor, FasterRCNN_ResNet50_FPN_Weights
)

import os
import cv2
import time

os.environ['TORCH_HOME'] = '/vol/web/'


class ped():
    api_threshold = 0.7
    trans = []
    trans.append(transforms.ToTensor())
    val_tran = transforms.Compose(trans)
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("GPU")
    else:
        device = torch.device("cpu")

    device = device
    model = models.detection.fasterrcnn_resnet50_fpn(
        weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
    num_classes = 2
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(
        in_features, num_classes)
    pth_path = "model/modelz.mdl"
# model.load_state_dict(torch.load(pth_path, map_location=torch.device('cpu')))
    model.load_state_dict(
        torch.load(pth_path, map_location=torch.device('cpu')))
    # compiled_model = torch.compile(model)
    model.eval()
    model = model
    model.to(device)

    @classmethod
    def fastrcnn_api(self, img):
        # img has to be OpenCV image
        self.model.eval()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        im_pil = self.val_tran(im_pil)
        image = im_pil.to(self.device)
        output = self.model([image])
        scores = output[0]['scores'].detach().cpu().numpy()
        num_people = len(scores[scores > self.api_threshold])
        boxes = output[0]['boxes'].detach().cpu().numpy()
        boxes = boxes[:num_people]
        return boxes, num_people


if __name__ == '__main__':
    test_img = "model/image.jpeg"
    img = cv2.imread(test_img)

    start_time = time.time()
    cped = ped()
    box, num = cped.fastrcnn_api(img)
    init_time = time.time()
    print("init: "+str((init_time - start_time)))

    print(box)
    print(num)
