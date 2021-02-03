import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img

# Define image properties
FAST_RUN = False
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3
batch_size = 15

# Get test files
test_filenames = os.listdir("./datasets/test1/")
test_df = pd.DataFrame({
    'filename': test_filenames
})
nb_samples = test_df.shape[0]

test_gen = ImageDataGenerator(rescale=1. / 255)
test_generator = test_gen.flow_from_dataframe(
    test_df,
    "./datasets/test1/",
    x_col='filename',
    y_col=None,
    class_mode=None,
    target_size=IMAGE_SIZE,
    batch_size=batch_size,
    shuffle=False
)

# Load model
# model = load_model('model.h5')
model = load_model('../assets/model_50-epochs.h5')

# summarize model.
model.summary()

# Prediction
predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples / batch_size))
test_df['category'] = np.argmax(predict, axis=-1)

# Convert labels
label_map = {0: "dog", 1: "cat"}
test_df['category'] = test_df['category'].replace(label_map)

test_df['category'] = test_df['category'].replace({'dog': 1, 'cat': 0})

# Display result in graph for dogs and cats
test_df['category'].value_counts().plot.bar()

# See results
sample_test = test_df.head(18)
sample_test.head()
plt.figure(figsize=(12, 24))
for index, row in sample_test.iterrows():
    filename = row['filename']
    category = row['category']
    img = load_img("./datasets/test1/" + filename, target_size=IMAGE_SIZE)
    plt.subplot(6, 3, index + 1)
    plt.imshow(img)
    plt.xlabel(filename + '(' + "{}".format(category) + ')')
plt.tight_layout()
plt.show()

# Save results
submission_df = test_df.copy()
submission_df['id'] = submission_df['filename'].str.split('.').str[0]
submission_df['label'] = submission_df['category']
submission_df.drop(['filename', 'category'], axis=1, inplace=True)
submission_df.to_csv('submission.csv', index=False)
