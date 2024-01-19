import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import requests
import base64
import uuid
import json
import time
import cv2
import requests
import platform
import numpy as np
import os
#!pip install roboflow
from roboflow import Roboflow

# if in colab
# from google.colab.patches import cv2.imshow('Image', img)
# ('Image', img)
