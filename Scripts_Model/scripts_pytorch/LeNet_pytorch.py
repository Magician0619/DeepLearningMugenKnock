import torch
import torch.nn.functional as F
import numpy as np
from collections import OrderedDict
from easydict import EasyDict
from _main_base import main
import os

#---
# config
#---
cfg = EasyDict()

# class
cfg.CLASS_LABEL = ['akahara', 'madara']
cfg.CLASS_NUM = len(cfg.CLASS_LABEL)

# model
cfg.INPUT_HEIGHT = 32
cfg.INPUT_WIDTH = 32
cfg.INPUT_CHANNEL = 3

cfg.GPU = False
cfg.DEVICE = torch.device("cuda" if cfg.GPU and torch.cuda.is_available() else "cpu")

cfg.MODEL_SAVE_PATH = 'models/LeNet_{}.pt'
cfg.MODEL_SAVE_INTERVAL = 200
cfg.ITERATION = 1000
cfg.MINIBATCH = 8
cfg.OPTIMIZER = torch.optim.SGD
cfg.LEARNING_RATE = 0.01
cfg.MOMENTUM = 0.9
cfg.LOSS_FUNCTION = loss_fn = torch.nn.NLLLoss()

cfg.TRAIN = EasyDict()
cfg.TRAIN.DISPAY_ITERATION_INTERVAL = 50

cfg.TRAIN.DATA_PATH = '../Dataset/train/images/'
cfg.TRAIN.DATA_HORIZONTAL_FLIP = True
cfg.TRAIN.DATA_VERTICAL_FLIP = True
cfg.TRAIN.DATA_ROTATION = False

cfg.TEST = EasyDict()
cfg.TEST.MODEL_PATH = cfg.MODEL_SAVE_PATH.format('final')
cfg.TEST.DATA_PATH = '../Dataset/test/images/'
cfg.TEST.MINIBATCH = 2

# random seed
torch.manual_seed(0)

class LeNet(torch.nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(cfg.INPUT_CHANNEL, 6, kernel_size=5, padding=0)
        self.conv2 = torch.nn.Conv2d(6, 16, kernel_size=5, padding=0)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120)
        self.fc2 = torch.nn.Linear(120, 64)
        self.fc_out = torch.nn.Linear(64, cfg.CLASS_NUM)
        
    def forward(self, x):
        x = self.conv1(x)
        x = F.sigmoid(F.max_pool2d(x, 2))
        x = self.conv2(x)
        x = F.sigmoid(F.max_pool2d(x, 2))
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc_out(x)
        x = F.softmax(x, dim=1)
        return x

# main
if __name__ == '__main__':

    model_save_dir = '/'.join(cfg.MODEL_SAVE_PATH.split('/')[:-1])
    os.makedirs(model_save_dir, exist_ok=True)

    main(cfg, LeNet())