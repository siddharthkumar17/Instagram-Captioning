import torch
import matplotlib.pyplot as plt
import numpy as np 
import argparse
import pickle 
import os
from torchvision import transforms 
from build_vocab import Vocabulary
from model import EncoderCNN, DecoderRNN
from PIL import Image

import json

class Caption:
    def __init__(self):
        # Device configuration
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.DEFAULT_OUTPUT_PATH = 'captions.json'
        
    

    def load_image(self, image_path, transform=None):
        image = Image.open(image_path).convert('RGB')
        image.load()
        image = image.resize([224, 224], Image.LANCZOS)
        
        if transform is not None:
            image = transform(image).unsqueeze(0)
        
        return image


    def getCaption(self, imgs, output_path='', vocab_path='data/vocab.pkl', decoder_path = 'models/decoder-5-3000.pkl', encoder_path = 'models/encoder-5-3000.pkl', embed_size = 256, hidden_size = 512, num_layers= 1):
        if(output_path==''):
            output_path=self.DEFAULT_OUTPUT_PATH
        device = self.device
        transform = transforms.Compose([
            transforms.ToTensor(), 
            transforms.Normalize((0.485, 0.456, 0.406), 
                                (0.229, 0.224, 0.225))])
        
        # Load vocabulary wrapper
        with open(vocab_path, 'rb') as f:
            vocab = pickle.load(f)

        # Build models
        encoder = EncoderCNN(embed_size).eval()  # eval mode (batchnorm uses moving mean/variance)
        decoder = DecoderRNN(embed_size, hidden_size, len(vocab), num_layers)
        encoder = encoder.to(device)
        decoder = decoder.to(device)

        # Load the trained model parameters
        encoder.load_state_dict(torch.load(encoder_path))
        decoder.load_state_dict(torch.load(decoder_path))
 
        CAPTIONS = []

        for img in imgs:
            # Prepare an image
            image = self.load_image(img, transform=transform)
            image_tensor = image.to(device)
            
            # Generate an caption from the image
            feature = encoder(image_tensor)
            sampled_ids = decoder.sample(feature)
            sampled_ids = sampled_ids[0].cpu().numpy()          # (1, max_seq_length) -> (max_seq_length)
            
            # Convert word_ids to words
            sampled_caption = []
            for word_id in sampled_ids:
                word = vocab.idx2word[word_id]
                sampled_caption.append(word)
                if word == '<end>':
                    break
            sentence = ' '.join(sampled_caption)
            
            # Print out the image and the generated caption
            CAPTIONS.append(self.prune_caption(sentence))
        
        json_captions = self.writeJSON(imgs, CAPTIONS, output_path=output_path)

        return json_captions

    def prune_caption(self,sentence):
        s = sentence.strip()
        words = s.split(' ', 1)[1].rsplit(' ', 1)[0]
        return ''.join(words)

    
    def writeJSON(self, imgs, captions, output_path=''):
        if(output_path==''):
            output_path=self.DEFAULT_OUTPUT_PATH
            
        j = dict()

        for x in range(len(imgs)):
            j[imgs[x]] = captions[x]
        
        with open(output_path, 'w') as outfile:
            json.dump(j, outfile)
        
        return j