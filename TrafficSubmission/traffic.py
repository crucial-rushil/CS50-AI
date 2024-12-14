import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments

    # load_data("/workspaces/42484853/traffic/gtsrb-small")

    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")
    pass

def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    image_list = list()
    image_labels = list()
    full_paths = [os.path.join(data_dir, entry) for entry in os.listdir(data_dir)]
    
    for item in full_paths:
        all_images = [os.path.join(item, picture) for picture in os.listdir(item)]
        for pic in all_images:
            image = cv2.imread(pic)
            img_resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
            image_list.append(img_resized)

            label = item[-2:]
            if label.isdigit() == False:
                image_labels.append(item[-1])
            else:
                image_labels.append(label)


    return (image_list, image_labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

    # at a high level in a CNN we start off by having layers which learn basics (curves, lines shapes) so few filters
    tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

    #we increase the number of filters to learn more features about the image building on top of the next
    tf.keras.layers.Conv2D(64, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

    #we also pool things together to prevent overfitting, and take highest value of the abstractions
    tf.keras.layers.Conv2D(128, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

    #we flatten everything then learn global patterns in the data with one big layer
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256,activation="relu"),

    #prevent overfitting
    tf.keras.layers.Dropout(0.5),

    #condense the information into 43 bins (this is a probablity function which uses softmax)
    tf.keras.layers.Dense(NUM_CATEGORIES,activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
