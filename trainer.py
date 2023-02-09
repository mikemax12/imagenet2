# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1he5ebNgOgznjlYc42qREMX13Lmmvw0Gz
"""

#Currently the Pytorch version 1.0 is stable and we even have better versions (when I recorded the video only 0.4.0 was stable)
#!pip install torch==0.4.0 torchvision
#!pip install torch torchvision
import torch
print ("current pytorch version is: ", torch.__version__)
# we need pillow version of 5.3.0
#pip3 install Pillow==5.3.0
import PIL
print ("current pillow version is: ", PIL.__version__)

import argparse
parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('filename')
args = parser.parse_args()
print(args.filename)
import os
import torchvision
import time
import json
import copy
from PIL import Image
import numpy as np
import torch.nn.functional as F
from torch.autograd import Variable
from torch import nn, optim
from torch.optim import lr_scheduler
from torchvision import transforms, models, datasets
print ("done importing")

"""Getting the flowers data using a URL link"""



"""Unzipping flower_data.tar.gz"""



"""Removing flower_data.tar.gz because we now have the unzipped data"""

train_dir = os.path.join(args.filename, 'train')
valid_dir = os.path.join(args.filename, 'val')
test_dir= os.path.join(args.filename, 'test')


dirs = {'train': train_dir, 
        'valid': valid_dir, 
        'test' : test_dir
       }

"""Setting up the image transforms"""

# add transforms to the data
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomRotation(45),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                            [0.229, 0.224, 0.225])
    ]),
    'valid': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ]),
}

"""Setting up the data loaders"""

# Load the datasets with ImageFolder
image_datasets = {x: datasets.ImageFolder(dirs[x],   transform=data_transforms[x]) for x in ['train']}
# load the data into batches
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=16, shuffle=True) for x in ['train']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train']}

"""Setting up the data loaders"""
'''
# Load the datasets with ImageFolder
train_dataset = torchvision.datasets.ImageFolder(root = train_dir, transform = data_transforms['train'])
test_dataset = torchvision.datasets.ImageFolder(root = test_dir, transform = data_transforms['test'])
val_dataset = torchvision.datasets.ImageFolder(root = valid_dir, transform = data_transforms['valid'])


dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=16, shuffle=True) for x in ['train', 'valid', 'test']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'valid', 'test']}

"""Getting the class labels"""

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(train_dir) if isfile(join(train_dir, f))]
class_names = onlyfiles
print(class_names)
'''

"""Reading the Json file"""



"""Showing a batch of images after applying the transforms on them"""



# choose the model
model = models.resnet18(pretrained=True)
model

model.fc = nn.Linear(512, 1000) #Should change from 512?
model

"""Setting up the directories to read the data"""

#data_dir = 'flower_data'

 
#unfreezing the model parameters

#model.cuda()


if torch.cuda.is_available():
  device= torch.device('cuda:1')
  print("CUDA is avaialble")
else:
  device= torch.device('cpu')
  print("Only CPU")


"""Using pre-trained models ...... To be continued!"""

#training/validating function 
# this part of code is from https://medium.com/@josh_2774/deep-learning-with-pytorch-9574e74d17ad
#I changed minor things for my convinience
def train_model(model, criteria, optimizer, scheduler,    
                                      num_epochs=5, device='cuda:1'):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    
    for epoch in range(1, num_epochs+1):
        print('Epoch {}/{}'.format(epoch, num_epochs ))
        print('-' * 10)
        if torch.cuda.is_available():
            device= torch.device('cuda:1')
            print("CUDA is avaialble")
        else:
            device= torch.device('cpu')
            print("Only CPU")
        # Each epoch has a training and validation phase
        for phase in ['train']:
            if phase == 'train':
                #scheduler.step()
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0
            i = 0
            # Iterate over data.
            print(i)
            print(len(dataloaders[phase]))
            for inputs, labels in dataloaders[phase]:
                i+=1
                if i % 1000 == 0:
                    print(i)
                if i < 10000:
                    break
                #inputs = inputs.to(device)
                #labels = labels.to(device)
                
                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    
                    
                    loss = criteria(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                        
                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                

            epoch_loss = running_loss / dataset_sizes[phase]
            #epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, )) #epoch_acc))

            # deep copy the model
            #if phase == 'valid' and epoch_acc > best_acc:
                #best_acc = epoch_acc
                #best_model_wts = copy.deepcopy(model.state_dict())

        print()
        scheduler.step()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model

criteria = nn.CrossEntropyLoss()
# Observe that all parameters are being optimized
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)
# Number of epochs
eps=5

model = train_model(model, criteria, optimizer, scheduler, eps, 'cuda:1')