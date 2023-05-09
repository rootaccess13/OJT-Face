# import tensorflow as tf
# import numpy as np
# import os
# import argparse

# # Create an argument parser to accept the data directory as a command-line argument
# parser = argparse.ArgumentParser()
# parser.add_argument("--data_path", type=str, required=True, help="path to the data directory containing the images")
# args = parser.parse_args()

# # Get the path to the data directory from the command-line argument
# data_path = args.data_path

# # Define the image size and batch size for training
# img_size = 224
# batch_size = 32

# # Define the training data generator with data augmentation
# train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#     rescale=1./255,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     validation_split=0.2)

# # Create the training data generator from the data directory
# train_generator = train_datagen.flow_from_directory(
#     data_path,
#     target_size=(img_size, img_size),
#     batch_size=batch_size,
#     class_mode='sparse',  # set to "sparse" to generate integer labels
#     subset='training')

# # Create the validation data generator from the data directory
# valid_generator = train_datagen.flow_from_directory(
#     data_path,
#     target_size=(img_size, img_size),
#     batch_size=batch_size,
#     class_mode='sparse',  # set to "sparse" to generate integer labels
#     subset='validation')

# # Create the convolutional neural network with filter 4 
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Conv2D(4, (3, 3), activation='relu', input_shape=(img_size, img_size, 3)),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(4, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(8, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(32, activation='relu'),
#     tf.keras.layers.Dense(2, activation='softmax')
# ])

# # Compile the model with sparse categorical cross-entropy loss and Adam optimizer
# model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# # Train the model on the training data and validate on the validation data
# model.fit(train_generator, epochs=10, validation_data=valid_generator)

# # Save the trained model to a file
# model_path = os.path.join("model", "trained_model.h5")
# model.save(model_path)

# print("Trained model saved to", model_path)

import cv2
import numpy as np
from PIL import Image
import os
# Path for face image database
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");
# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        if imagePath == 'dataset/.DS_Store':
            continue

        PIL_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') 
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

