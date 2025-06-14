# -*- coding: utf-8 -*-
"""fyp_test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xd_-1uojR1rbulB692mk4c-NdqiAoMBB

# LIBRARY IMPORT
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import librosa
import librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import IPython
import tensorflow.keras.layers as L
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical  # Fixed import
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
import re
import itertools
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
from feature_extraction import add_noise, shifting, pitching, stretching, extract_features, get_features

import os
from tkinter import Tk, Button, Label, filedialog
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io
import base64
import json

"""# RAVDESS FILE"""

Ravdess_Path = '/content/drive/MyDrive/FYP/Ravdess/audio_speech_actors_01-24'
ravdess=[]
for directory in os.listdir(Ravdess_Path):
    actors=os.listdir(os.path.join(Ravdess_Path,directory))
    for wav in actors:
        emotion=wav.partition('.wav')[0].split('-')
        emotion_number=int(emotion[2])
        ravdess.append((emotion_number,os.path.join(Ravdess_Path,directory,wav)))
Ravdess_df=pd.DataFrame.from_dict(ravdess)
Ravdess_df.rename(columns={0:'Emotion',1:'File_Path'},inplace=True)
Ravdess_df['Emotion'].replace({1:'neutral', 2:'neutral', 3:'happy', 4:'sad', 5:'angry', 6:'fear', 7:'disgust', 8:'surprise'},inplace=True)
Ravdess_df.head()

Ravdess_df['Emotion'].unique()

main_df=pd.concat([Ravdess_df],axis=0)
main_df.shape

main_df.head(15)

main_df.tail(15)

plt.figure(figsize=(12,6))
plt.title('Emotions Counts')
emotions=sns.countplot(x='Emotion',data=main_df,palette='Set2')
emotions.set_xticklabels(emotions.get_xticklabels(),rotation=45)
plt.show()

emotion_names=main_df['Emotion'].unique()

colors={'disgust':'#804E2D','happy':'#F19C0E','sad':'#478FB8','neutral':'#4CB847','fear':'#7D55AA','angry':'#C00808','surprise':'#EE00FF'}

def wave_plot(data,sr,emotion,color):
    plt.figure(figsize=(12,5))
    plt.title(f'{emotion} emotion for waveplot',size=17)
    librosa.display.waveshow(y=data,sr=sr,color=color)

def spectogram(data,sr,emotion):
    audio=librosa.stft(data)
    audio_db=librosa.amplitude_to_db(abs(audio))
    plt.figure(figsize=(12,5))
    plt.title(f'{emotion} emotion for spectogram',size=17)
    librosa.display.specshow(audio_db,sr=sr,x_axis='time',y_axis='hz')

audio_path=[]
for emotion in emotion_names:
    path=np.array(main_df['File_Path'][main_df['Emotion']==emotion])[1]
    data,sr=librosa.load(path)
    wave_plot(data,sr,emotion,colors[emotion])
    spectogram(data,sr,emotion)
    audio_path.append(path)

print('Neutral Audio Sample\n')
IPython.display.Audio(audio_path[0])

print('Surprise Audio Sample\n')
IPython.display.Audio(audio_path[1])

print('Happy Audio Sample\n')
IPython.display.Audio(audio_path[2])

print('Fear Audio Sample\n')
IPython.display.Audio(audio_path[3])

print('Sad Audio Sample\n')
IPython.display.Audio(audio_path[4])

print('Angry Audio Sample\n')
IPython.display.Audio(audio_path[5])

print('Disgust Audio Sample\n')
IPython.display.Audio(audio_path[6])

"""# DATA AUGMENTATION

"""

def add_noise(data,random=False,rate=0.035,threshold=0.075):
    if random:
        rate=np.random.random()*threshold
    noise=rate*np.random.uniform()*np.amax(data)
    augmented_data=data+noise*np.random.normal(size=data.shape[0])
    return augmented_data

def shifting(data,rate=1000):
    augmented_data=int(np.random.uniform(low=-5,high=5)*rate)
    augmented_data=np.roll(data,augmented_data)
    return augmented_data

def pitching(data,sr,pitch_factor=0.7,random=False):
    if random:
        pitch_factor=np.random.random() * pitch_factor
    return librosa.effects.pitch_shift(y=data,sr=sr,n_steps=pitch_factor)

def stretching(data,rate=0.8):
    return librosa.effects.time_stretch(y=data,rate=rate)

data,sr=librosa.load(audio_path[6])

#ORIGINAL AUDIO
plt.figure(figsize=(12,5))
librosa.display.waveshow(y=data, sr=sr, color='#478FB8')  # Use named parameters
plt.title('Waveform')
plt.tight_layout()
plt.show()
IPython.display.Audio(audio_path[6])

#NOISED AUDIO
noised_audio = add_noise(data)
plt.figure(figsize=(12,5))
librosa.display.waveshow(y=noised_audio, sr=sr, color='#EE00FF')  # Use named parameters
plt.title('Waveform')
plt.tight_layout()
plt.show()
IPython.display.Audio(noised_audio, rate=sr)

#STRETCHED AUDIO
stretched_audio = stretching(data)
plt.figure(figsize=(12, 5))
librosa.display.waveshow(y=stretched_audio, sr=sr, color='#EE00FF')
plt.title('Waveform')
plt.tight_layout()
plt.show()
IPython.display.Audio(stretched_audio, rate=sr)

#PITCHED AUDIO
pitched_audio=pitching(data,sr)
plt.figure(figsize=(12,5))
librosa.display.waveshow(y=pitched_audio, sr=sr, color='#EE00FF')
plt.title('Waveform')
plt.tight_layout()
plt.show()
IPython.display.Audio(pitched_audio,rate=sr)

#SHIFTED AUDIO
shifted_audio=shifting(data)
plt.figure(figsize=(12,5))
librosa.display.waveshow(y=shifted_audio,sr=sr,color='#EE00FF')
plt.title('Waveform')
plt.tight_layout()
plt.show()
IPython.display.Audio(shifted_audio,rate=sr)

"""# FEATURE EXTRACTION
USING MFCC
"""

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten:bool=True):
    """Extract Mel-Frequency Cepstral Coefficients feature"""
    mfcc_feat = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, hop_length=hop_length, n_fft=frame_length)
    return np.squeeze(mfcc_feat.T) if not flatten else np.ravel(mfcc_feat.T)

def extract_features(data, sr, frame_length=2048, hop_length=512):
    """Extract only statistical features to ensure consistent dimensions"""
    result = np.array([])

    # Use a fixed number of coefficients
    mfcc_feat = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, hop_length=hop_length, n_fft=frame_length)

    # Calculate statistics for each coefficient (13 coefficients)
    for i in range(mfcc_feat.shape[0]):
        result = np.hstack((result,
                           np.mean(mfcc_feat[i]),
                           np.std(mfcc_feat[i]),
                           np.min(mfcc_feat[i]),
                           np.max(mfcc_feat[i])))

    return result

X,Y=[],[]
for path,emotion,index in zip(main_df.File_Path,main_df.Emotion,range(main_df.File_Path.shape[0])):
    features=get_features(path)
    if index%500==0:
        print(f'{index} audio has been processed')
    for i in features:
        X.append(i)
        Y.append(emotion)
print('Done')

processed_data_path='./processed_data.csv'
extract=pd.DataFrame(X)
extract['Emotion']=Y
extract.to_csv(processed_data_path,index=False)
extract.head(10)

"""#ANALYSING AUDIO FEATURES"""

df=pd.read_csv(processed_data_path)
df.shape

df=df.fillna(0)
print(df.isna().any())
df.shape

df.head(10)

"""#PROCESSING ANALYSED AUDIO FOR TRAINING"""

from keras.utils import to_categorical

X = df.drop(labels='Emotion', axis=1)
Y = df['Emotion']
lb = LabelEncoder()
Y = to_categorical(lb.fit_transform(Y))
print(lb.classes_)
Y

"""#TRAIN, TEST AND VALIDATION SPLITING"""

#Splitting, Training set = 70%, Validation set = 10%, Test set = 20%
X_train,X_test,y_train,y_test=train_test_split(X,Y,random_state=42,test_size=0.2,shuffle=True)
X_train.shape,X_test.shape,y_train.shape,y_test.shape

X_train,X_val,y_train,y_val=train_test_split(X_train,y_train,random_state=42,test_size=0.1,shuffle=True)
X_train.shape, X_test.shape, X_val.shape, y_train.shape,y_test.shape,y_val.shape

#Feature Scaler, prevents features with larger ranges from dominating the learning process
scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
import joblib
joblib.dump(scaler, 'scaler.save')
X_test=scaler.transform(X_test)
X_val=scaler.transform(X_val)
X_train.shape,X_test.shape,X_val.shape,y_train.shape,y_test.shape,y_val.shape

#Adding dimension to the data
#reshape data to fit the 1D CNN
X_train=np.expand_dims(X_train,axis=2)
X_val=np.expand_dims(X_val,axis=2)
X_test=np.expand_dims(X_test,axis=2)
X_train.shape, X_test.shape, X_val.shape

"""#TUNING BEFORE TRAINING


"""

early_stop=EarlyStopping(monitor='val_acc',mode='auto',patience=5,restore_best_weights=True) #prevents overtfitting by stopping the training when the model stops improving
lr_reduction=ReduceLROnPlateau(monitor='val_acc',patience=3,verbose=1,factor=0.5,min_lr=0.00001) #automatically reduce learning rate when the model stops improving

EPOCH=50
BATCH_SIZE=32

"""# TRAINING


*   Conv1D
*   Fixed Parameters (BatchNormalization)
*   Final Output : 7 nodes for each emotion classes
*   Total Params : no. of weights & biases in the model (large dense layer 512 nodes)
*   Trainable params : parameters that will be updated during training through backpropagation, allows network to learn and adjust weights to minimize the loss function
*   Non-train params : fixed parameters that will be not updated during training.
*   Optimizer : Adam


"""

model = tf.keras.Sequential([
    L.Conv1D(512, kernel_size=5, strides=1, padding='same', activation='relu', input_shape=(X_train.shape[1], 1)),
    L.BatchNormalization(),
    L.MaxPool1D(pool_size=5, strides=2, padding='same'),
    L.Conv1D(512, kernel_size=5, strides=1, padding='same', activation='relu'),
    L.BatchNormalization(),
    L.MaxPool1D(pool_size=5, strides=2, padding='same'),
    L.Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu'),
    L.BatchNormalization(),
    L.MaxPool1D(pool_size=5, strides=2, padding='same'),
    L.Conv1D(256, kernel_size=3, strides=1, padding='same', activation='relu'),
    L.BatchNormalization(),
    L.MaxPool1D(pool_size=5, strides=2, padding='same'),
    L.Conv1D(128, kernel_size=3, strides=1, padding='same', activation='relu'),
    L.BatchNormalization(),
    L.MaxPool1D(pool_size=3, strides=2, padding='same'),
    L.Flatten(),
    L.Dense(512, activation='relu'),
    L.BatchNormalization(),
    L.Dense(7, activation='softmax')
])

model.compile(
    optimizer='nadam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

from google.colab import drive
drive.mount('/content/drive')

#Define the callbacks
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=10,
    mode='max',  #set mode to 'max' for accuracy metrics
    restore_best_weights=True
)

lr_reduction = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    patience=3,
    factor=0.2,
    min_lr=1e-6,
    verbose=1
)

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=EPOCH,
    validation_data=(X_val, y_val),
    batch_size=BATCH_SIZE,
    callbacks=[early_stop, lr_reduction]
)

"""* Early stopping callback is working as intended as the model has stopped improving after epoch 30
* Helps to avoid overfitting and learning rate reduction reached the minimum value

# CHARTS 😀

Accuracy Chart ✅
"""

fig=px.line(history.history,y=['accuracy','val_accuracy'],
           labels={'index':'epoch','value':'accuracy'},
           title=f'Epoch accuracy and Validation accuracy')
fig.show()

"""Loss Chart ❎"""

fig=px.line(history.history,y=['loss','val_loss'],
           labels={'index':'epoch','value':'loss'},
           title=f'Epoch loss and Validation loss')
fig.show()

"""# TESTING AND TEST RESULTS 🧮"""

#converting the model's raw predictions into class labels for evaluation
y_pred = model.predict(X_test)
y_pred = np.argmax(y_pred, axis=1)  #array of integers where each integer represents the predicted class
y_pred

y_check=np.argmax(y_test,axis=1)
y_check

loss,accuracy=model.evaluate(X_test,y_test,verbose=0)
print(f'Test Loss: {loss}')
print(f'Test Accuracy: {accuracy}')

"""Accuracy : 83.6%

CONFUSION MATRIX 😫
"""

conf=confusion_matrix(y_check,y_pred)
cm=pd.DataFrame(
    conf,index=[i for i in emotion_names],
    columns=[i for i in emotion_names]
)
plt.figure(figsize=(12,7))
ax=sns.heatmap(cm,annot=True,fmt='d')
ax.set_title(f'confusion matrix for model ')
plt.show()

print(f'Model Confusion Matrix\n',classification_report(y_check,y_pred,target_names=emotion_names))

model_path = "./res_model.keras"
model.save(model_path)

from google.colab import files
files.download('./res_model.keras')
files.download('scaler.save')