import torch
import torch.nn as nn
import torch.nn.functional as F

class BaseNN(nn.Module):
    '''
        This is a base CNN model.
    '''
    def __init__(self, pitch_class=12, pitch_octave=4):
        super(BaseNN, self).__init__()
        self.pitch_octave = pitch_octave
        self.pitch_class = pitch_class
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(3, 3), padding=(1, 1))
        self.conv2 = nn.Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1))
        self.conv3 = nn.Conv2d(64, 128, kernel_size=(3, 3), padding=(1, 1))
        self.conv4 = nn.Conv2d(128, 128, kernel_size=(3, 3), padding=(1, 1))
        self.conv5 = nn.Conv2d(128, 64, kernel_size=(5, 5), padding=(2, 2))
        self.conv6 = nn.Conv2d(64, 32, kernel_size=(5, 5), padding=(2, 2))
        self.conv7 = nn.Conv2d(32, 1, kernel_size=(5, 5), padding=(2, 2))
        self.fc1   = nn.Linear(420, 256)
        self.fc2   = nn.Linear(256, 128)
        self.fc3   = nn.Linear(128, 128)
        self.fc4   = nn.Linear(128, 128)
        self.fc5   = nn.Linear(128, 2+pitch_class+pitch_octave+2)
        self.drop  = nn.Dropout(0.2)

    def forward(self, x):
        
        # print(f"{x.shape}")
        out = F.relu(self.conv1(x))
        # print(f"{out.shape}")
        out = F.relu(self.conv2(out))
        # print(f"{out.shape}")
        # out = F.max_pool2d(out, 2)
        # print(f"{out.shape}")
        out = F.relu(self.conv3(out))
        # print(f"{out.shape}")
        out = F.relu(self.conv4(out))
        # print(f"{out.shape}")
        out = F.max_pool2d(out, 2)
        out = F.relu(self.conv5(out))
        # print(f"{out.shape}")
        out = F.relu(self.conv6(out))
        # print(f"{out.shape}")
        out = F.relu(self.conv7(out))
        # print(f"{out.shape}")
        out = out.view(x.size(0), -1)
        # print(f"{out.shape}")
        out = F.relu(self.fc1(out))
        # print(f"{out.shape}")
        out = F.relu(self.fc2(out))
        out = F.relu(self.fc3(out))
        out = F.relu(self.fc4(out))
        out = self.drop(out)
        out = self.fc5(out)

        onset_logits = out[:, 0]
        offset_logits = out[:, 1]

        pitch_out = out[:, 2:]
        
        pitch_octave_logits = pitch_out[:, 0:self.pitch_octave+1]
        pitch_class_logits = pitch_out[:, self.pitch_octave+1:]

        
        return onset_logits, offset_logits, pitch_octave_logits, pitch_class_logits

