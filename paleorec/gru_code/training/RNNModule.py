# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:15:01 2021

@author: shrav
"""

import torch
import torch.nn as nn

class RNNModule(nn.Module):
    def __init__(self, n_vocab, seq_size, embedding_size, hidden_size):
        
        super(RNNModule, self).__init__()
        self.seq_size = seq_size
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(n_vocab, embedding_size)
        self.gru = nn.GRU(embedding_size,
                            hidden_size,
                            batch_first=True)
        self.dense = nn.Linear(hidden_size, n_vocab)
    
    def forward(self, x, prev_state):
        embed = self.embedding(x)
        output, state = self.gru(embed, prev_state)
        logits = self.dense(output)

        return logits, state
    
    def zero_state(self, batch_size):
        print('zero_state called')
        return Variable(torch.zeros(1,batch_size,self.hidden_size)