#%matplotlib inline
#%config InlineBackend.figure_format = 'retina'
import numpy as np
import torch

import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch import nn
from torch import optim
import torch.nn.functional as F

# Custom DataSet
from data import iris
from data import helper

# Get the datasets
iris_data_file = 'data/poker_game_data.txt'
train_ds, test_ds = iris.get_datasets(iris_data_file)

# How many instances have we got?
print('# instances in training set: ', len(train_ds))
print('# instances in testing/validation set: ', len(test_ds))

train_loader = torch.utils.data.DataLoader(dataset=test_ds, batch_size= 1, shuffle=True)
test_loader  = torch.utils.data.DataLoader(dataset=test_ds, batch_size=1, shuffle=True)
dataiter = iter(train_loader)
images, labels = dataiter.next()
m = images.mean()
s = images.std()
#images = (images - m)/s
print(images)
print(labels)

class Network(nn.Module):
    def __init__(self, input_size, output_size, hidden_layers, drop_p=0.5):
        ''' Builds a feedforward network with arbitrary hidden layers.

            Arguments
            ---------
            input_size: integer, size of the input
            output_size: integer, size of the output layer
            hidden_layers: list of integers, the sizes of the hidden layers
            drop_p: float between 0 and 1, dropout probability
        '''
        super().__init__()
        # Add the first layer, input to a hidden layer
        self.hidden_layers = nn.ModuleList([nn.Linear(input_size, hidden_layers[0])])

        # Add a variable number of more hidden layers
        layer_sizes = zip(hidden_layers[:-1], hidden_layers[1:])
        self.hidden_layers.extend([nn.Linear(h1, h2) for h1, h2 in layer_sizes])

        self.output = nn.Linear(hidden_layers[-1], output_size)

        self.dropout = nn.Dropout(p=drop_p)

    def forward(self, x):
        ''' Forward pass through the network, returns the output logits '''

        # Forward through each layer in `hidden_layers`, with ReLU activation and dropout
        for linear in self.hidden_layers:
            x = F.relu(linear(x))
            x = self.dropout(x)

        x = self.output(x)

        return F.log_softmax(x, dim=1)

# Create the network, define the criterion and optimizer
model = Network(10, 10, [128,128,64], drop_p=0.5)
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Grab some data
dataiter = iter(train_loader)
images, labels = dataiter.next()

images.resize_(1, 1,10)

img_idx = 0
ps = model.forward(images[img_idx,:])

img = images[img_idx]
helper.view_classify(ps)

epochs = 20
print_every = 500
steps = 0
for e in range(epochs):
    running_loss = 0
    for images, labels in iter(train_loader):

        #m = images.mean()
        #images = (images - m)/ s
        #print(images)
        #print(labels)
        steps += 1
        # Flatten MNIST images into a 784 long vector
        images.resize_(images.size()[0], 10)

        optimizer.zero_grad()

        # Forward and backward passes
        output = model.forward(images)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        if steps % print_every == 0:
            print("Epoch: {}/{}... ".format(e+1, epochs),
                  "Loss: {:.4f}".format(running_loss/print_every))

            running_loss = 0

print(steps)

images, labels = next(iter(train_loader))

#x = torch.FloatTensor([n])

img = images

# Turn off gradients to speed up this part
with torch.no_grad():
    logits = model.forward(img)

# Output of the network are logits, need to take softmax for probabilities
ps = F.softmax(logits, dim=1)

helper.view_classify(ps)
print(ps)
print(labels)
