import os
import numpy as np

import cv2 as cv

import tensorflow as tf

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Input, Conv2D, Dense, Activation, Add, Multiply, Lambda, Concatenate
from tensorflow.keras.models import Model

from .lib import common
from .lib.layers import Squeeze, Excitation, SpatialAttention, ChannelAttention 

from . import base


def se_block(inputs, name):
    
    s = Squeeze(pooling='attention', in_activation='tanh', scores_activation='softmax', name=name + '_squeezed')(inputs)
    e = Excitation(decay=0.5, in_activation='relu', out_activation='sigmoid', name=name + '_excited')(s)
    x = Multiply()([inputs, e])
    x = Squeeze(pooling='average', name=name + '_squeezed2')(x)
    
    return x

def dual_attention_block(features_map, target_key):
    
    x = SpatialAttention(name=f'spatial_attn_{target_key}')(features_map)
    x = se_block(x, name=f'spatial_se_block_{target_key}')
    
    y = ChannelAttention(name=f'channel_attn_{target_key}')(features_map)
    y = se_block(y, name=f'channel_se_block_{target_key}')
    
    features = Add(name=f'features_{target_key}')([x, y])
    
    return x


def build_chexpert_dual_attention(latent_dim=256, name='chexpert-dual-attention'):
    
    # ------------------------------------------------------------------------------------------------------------

    backbone = EfficientNetB0(input_shape=Config.backbone_input_shape, weights=None, include_top=False)

    # ------------------------------------------------------------------------------------------------------------
    
    inputs_images = Input(shape=Config.model_input_shape, name='image')
    
    rgb = Conv2D(filters=3, kernel_size=(1, 1), padding='same', strides=1, name='to_rgb')(inputs_images)
    
    features_map = backbone(rgb)
    features_map = Dense(latent_dim, name='features_map')(features_map)
    
    # ------------------------------------------------------------------------------------------------------------
       
    scores = []
    labels = []
  
    for i, target_key in enumerate(Config.observations):
        
        dim = 1 if target_key == 'no_finding' else 4
        
        features = dual_attention_block(features_map, target_key=target_key)
        features = Lambda(lambda tensor: tf.squeeze(tensor, axis=1))(features)
        
        # target score
        si = Dense(1, name=f's{i}')(features)
        si = Activation('sigmoid', name=f'{target_key}_score')(si)
        scores.append(si)
        
        if target_key != 'no_finding':
            
            yi = Dense(dim, name=f'y{i}')(features)
            yi = Activation('softmax')(yi)
            yi = Multiply(name=f'{target_key}_label')([yi, si])
            labels.append(yi)
    
    scores = Concatenate(axis=1, name='scores')(scores)
    labels = Concatenate(axis=1, name='labels')(labels)
    
    # ------------------------------------------------------------------------------------------------------------
    
    inputs = [inputs_images]
    outputs = [scores, labels]
    
    model = Model(inputs=inputs, outputs=outputs, name=name)
    
    # ------------------------------------------------------------------------------------------------------------

    return model

class Config:

    """
    not mentioned/applicable : probability of ith observation is not considered at all
    negative: good indicator
    uncertain: ???
    positive: bad indicator
    """

    # -----------------------------------------------------------------------------------------------------------------------------------
    
    observations = ['no_finding', 'enlarged_cardiomediastinum', 'cardiomegaly', 'lung_opacity', 'lung_lesion', 'edema', 'consolidation', 
                    'pneumonia', 'atelectasis', 'pneumothorax', 'pleural_effusion', 'pleural_other', 'fracture', 'support_devices']
    
    # -----------------------------------------------------------------------------------------------------------------------------------

    model_input_shape = (384, 384, 3)
    backbone_input_shape = (384, 384, 3)

    # -----------------------------------------------------------------------------------------------------------------------------------
    
    classes_map = {0: 'not mentioned', 1: 'negative', 2: 'uncertain', 3: 'positive'}
    gender_map = {0: 'n/a', 1: 'male', 2: 'female'}

    # -----------------------------------------------------------------------------------------------------------------------------------
    
    threshold = 0.5

    # -----------------------------------------------------------------------------------------------------------------------------------

    # decode_fn = {'image': decode}
    # chexpert_reader = TFRecordReader(dtypes=dtypes, decode_fn=decode_fn)

    
class CheXpert002(base.Handler):
    
    model_id = 'chexpert002'
    
    def __init__(self, model_metadata):
        
        super().__init__(model_metadata)

        self.build()
        
        self.set_inputs_desc(keys=["0"], dtypes=[list])
        self.set_outputs_desc(keys=["0"], dtypes=[dict]) # {"tags": ..., "content": []}
        
    def build(self):
        
        weights_path = self.model_metadata['weights_path']
        weights_path = os.path.join(self.working_dir, weights_path)

        assert os.path.exists(weights_path), f'Invalid weights-path={weights_path}'

        self.model = build_chexpert_dual_attention(latent_dim=256, name=None)
        self.model.load_weights(weights_path)
        
    def prepare(self):
                
        assert len(self.intermediate_buffer) < self.buffer_size, 'Corrupted intermediate buffer'

        for buffer_index in self.inputs_buffer:
            
            assert not (buffer_index in self.intermediate_buffer), 'Corrupted intermediate buffer'
            
            self.intermediate_buffer[buffer_index] = {}

            # rename block_index to some predefined key to improve the readability
            self.intermediate_buffer[buffer_index]['image'] = self.inputs_buffer[buffer_index].pop('0')
            
            study_size = len(self.intermediate_buffer[buffer_index]['image'])
            
            for k in range(study_size):
                
                # make sure that image is an Grayscale image            
                if common.is_gray(self.intermediate_buffer[buffer_index]['image'][k]):
                    
                    self.intermediate_buffer[buffer_index]['image'][k]  = cv.cvtColor(self.intermediate_buffer[buffer_index]['image'][k], cv.COLOR_GRAY2RGB)
                
                else:
                
                    self.intermediate_buffer[buffer_index]['image'][k]  = cv.cvtColor(self.intermediate_buffer[buffer_index]['image'][k], cv.COLOR_BGR2RGB)
   

                self.intermediate_buffer[buffer_index]['image'][k] = self.intermediate_buffer[buffer_index]['image'][k].astype('float32')
                
            self.intermediate_buffer[buffer_index]['image'] = np.stack(self.intermediate_buffer[buffer_index]['image'], axis=0)
            
            # TODO: set ith metadata prepared flag  ...
            
    def filter_observations(self, observations_scores, labels_probabilities):

        """
        observations_probabilities: score vectors (i.e., indices is consistent Config.observations)
        labels_probabilities: vectors (one-hot encoding format)
        """

        new_observations = {}

        # no finding probability
        p = observations_scores[0]
        
        if p > Config.threshold:
            
            return {}
        
        for key, pk, pc in zip(Config.observations[1:], observations_scores[1:], labels_probabilities):

            label = pc.argmax(axis=-1)
                            
            if (pk > Config.threshold) and (label == 2 or label == 3):
                
                new_observations[key] = (label, pk)        

        return new_observations
    
    def get_average_certainty(self, observations):
        
        average_certainty = 0.0
        
        if len(observations) == 0:
            
            return average_certainty
         
        uncertain_count = 0
        certain_count = 0
        
        for label, _ in observations.values():
            
            if label == 2:
                
                uncertain_count += 1

            elif label == 3:
                
                certain_count += 1
        
        p = (certain_count / (certain_count + uncertain_count)) if uncertain_count > 0 else certain_count
        
        for _, pk in observations.values():

            average_certainty += (pk * p)
        
        average_certainty /= len(observations)
        
        return average_certainty
    
    def observations_to_tags(self, observations):
        
        tags = []
        
        for key in observations:
            
            tag = key.replace('_', ' ').title()   
            tags.append(tag)
                
        return tags
    
    def make_superimposed_image(self, image):
        
        image = np.expand_dims(image, axis=0)
        
        pooling = self.model.layers[1](image)
        pooling = self.model.layers[2](pooling).numpy()
        pooling = pooling.squeeze(axis=0)
        pooling = pooling.mean(axis=-1)
        pooling = common.normalize_in_range(pooling, 0.0, 255.0, axes=[0, 1]).astype('uint8')

        image = image.squeeze(axis=0)
        pooling = cv.resize(pooling, dsize=tuple(image.shape[:2]))

        if common.is_gray(image):
            
            image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
        
        image = common.normalize_in_range(image, 0.0, 255.0, axes=[0, 1, 2]).astype('uint8')
        
        heatmap = cv.applyColorMap(pooling, cv.COLORMAP_JET)
        superimposed = cv.addWeighted(image, 0.7, heatmap, 0.15, 0)
        
        return superimposed
    
    def write_superimposed(self, superimposed: np.ndarray, filename: str):
        
        file_url = os.path.join(self.working_dir, f'results/{filename}')
        
        cv.imwrite(filename=file_url, img=superimposed)

        assert os.path.exists(file_url), 'Invalid file_url, write_superimposed(...)'
        
        return os.path.abspath(file_url)
    
    def run_inference(self):
        
        superimposed_urls = []
        
        for buffer_index in self.intermediate_buffer:
            
            processed_inputs = self.intermediate_buffer[buffer_index]

            scores, labels = self.model.predict_on_batch(processed_inputs)
            
            scores = scores.mean(axis=0).squeeze()
            labels = labels.mean(axis=0).squeeze()
            
            for k in range(len(processed_inputs['image'])):
                
                superimposed = self.make_superimposed_image(processed_inputs['image'][k])
                
                superimposed_url = self.write_superimposed(superimposed=superimposed, filename=f'{buffer_index}_{k}.png')
                
                superimposed_urls.append(superimposed_url)
            
            self.intermediate_buffer[buffer_index] = (scores, labels, superimposed_urls)
    
    def run_postprocessing(self):

        for buffer_index in self.intermediate_buffer:
            
            (scores, labels, superimposed_urls) = self.intermediate_buffer[buffer_index]
            
            observations = self.filter_observations(observations_scores=scores, labels_probabilities=labels)
            
            tags = self.observations_to_tags(observations=observations)

            average_certainty = self.get_average_certainty(observations)
            average_certainty = str(np.round((average_certainty * 100.0), 2)) + '%'
        
            output = {'type': 'image', 'tags': tags, 'data': superimposed_urls, 
                      'certainty': average_certainty, 'is_stream': False}
            
            self.append_outputs(buffer_index=buffer_index, outputs={'0': output})