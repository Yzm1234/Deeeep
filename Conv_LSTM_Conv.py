import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn
import numpy as np

class Conv_LSTM_Conv(nn.Module):

    def __init__(self, nlayers_LSTM):
        super(Conv_LSTM_Conv, self).__init__()
        self.nlayers_LSTM = nlayers_LSTM
        self.convs1 = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2),
                                    nn.ReLU(), # [??chenfeng] should RELU be used here?
                                    nn.Conv2d(in_channels=16, out_channels=1, kernel_size=5, stride=1, padding=2),
                                    nn.ReLU(),
                                    nn.Softmax2d())
        self.rnn = nn.LSTM(input_size=1, hidden_size=256,
                           num_layers=nlayers_LSTM, bidirectional=True)
        self.convs2 = nn.Sequential(nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=1, padding=2),
                                    nn.ReLU(),
                                    nn.MaxPool2d(kernel_size = 2),
                                    nn.Conv2d(in_channels=32, out_channels=2, kernel_size=5, stride=1, padding=2),
                                    nn.ReLU(),
                                    nn.Conv2d(in_channels=2, out_channels=2, kernel_size=5, stride=1, padding=2),
                                    nn.ReLU())
        self.linear = nn.Sequential(nn.Linear(in_features=256, out_features=1), nn.Softmax())

    def forward(self, inputs): # The input to this network should be a batch of size 64 * 64
        feature_map = self.convs1(inputs) # out shape (16, 16, N)?
        feature_map = torch.reshape(feature_map, (-1,))
        rnn_out = self.rnn(feature_map)[0]
        out = self.convs2(rnn_out)
        predicted_label = self.linear(rnn_out)
        return out, predicted_label

