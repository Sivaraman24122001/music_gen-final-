from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow.keras as keras
import os
import librosa
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from pydantic import BaseModel
from typing import List
from tqdm import tqdm
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

app = FastAPI()
labelencoder = LabelEncoder()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

audio_dataset_path='Data/genres_original'
metadata=pd.read_csv('Data/features_30_sec.csv')


def features_extractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast') 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    
    return mfccs_scaled_features

extracted_features=[]
for index_num, row in tqdm(metadata.iterrows()):
    try:
        final_class_labels=row['label']
        file_name= os.path.join(os.path.abspath(audio_dataset_path), final_class_labels+'/', str(row["filename"])) 
        data=features_extractor(file_name)
        extracted_features.append([data, final_class_labels])
    except Exception as e:
        print(f"Error: {e}")
        continue

extracted_features_df=pd.DataFrame(extracted_features, columns=['feature', 'class'])

X=np.array(extracted_features_df['feature'].tolist())
y=np.array(extracted_features_df['class'].tolist())   

labelencoder = LabelEncoder()
y = to_categorical(labelencoder.fit_transform(y))

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

num_labels = y.shape[1]

model=Sequential()
model.add(Dense(1024, input_shape=(40,), activation="relu")) 
model.add(Dropout(0.3))
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(32, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(num_labels, activation="softmax"))

model.compile(loss='categorical_crossentropy',metrics=['accuracy'],optimizer='adam')


class Audio(BaseModel):
    audio_file: bytes

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    audio_file = file.file  # Use file.file to access the file content
    audio, sample_rate = librosa.load(audio_file, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    predicted_label = model.predict(mfccs_scaled_features)
    predicted_label_index = np.argmax(predicted_label, axis=1)
    prediction_class = labelencoder.inverse_transform(predicted_label_index)
    predicted = str(prediction_class)
    
    return {"Music Genre": predicted}  
