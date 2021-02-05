import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import tensorflow as tf


PATH_MODEL_CNN = "../assets/model_50-epochs_final.h5"


# get an image as np.array when a user sends one and prepare it for the NN

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_CHANNELS = 3
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
# to check if the message is an image .jpg, png or jpeg
pic_ext = ['.jpg', '.png', '.jpeg', '.jfif']


def get_image_from_channel_to_predict(message):
    image_is_sent = False
    # check if there is an attachment
    if message.attachments:
        for ext in pic_ext:
            if message.attachments[0].filename.endswith(ext):
                image_is_sent = True
                url = message.attachments[0].url
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                # img_np contains img as an np.array
                img_np = np.array(img)
                #prepare it for the NN
                img_np = cv2.resize(img_np, IMAGE_SIZE)
    if not image_is_sent:
        img_np = np.zeros(1, dtype='int')
    return img_np, image_is_sent


#download image locally to send it if necessary
def download_image_from_channel(message):
    image_extension = ''
    if message.attachments:
        for ext in pic_ext:
            if message.attachments[0].filename.endswith(ext):
                img_data = requests.get(message.attachments[0].url).content
                with open('image_downloaded_by_bot' + ext, 'wb') as handler:
                    image_extension = ext
                    handler.write(img_data)
    return image_extension



#predict the type of the image
model = tf.keras.models.load_model(PATH_MODEL_CNN)

categorie = ["Chat", "Chien", "[IMAGE]: Je suis pas sûr si l'image contient un chat ou un chien"]
def predict_type_image(image):
    #plt.imshow(image)
    #plt.show()
    image = image.reshape(-1, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)
    print(image.shape)
    prediction = model.predict([image])
    print(prediction)

    # par exemple, prediction est de la forme [[0. 1.]]
    # avec 0 -> pas chat et 1 -> chien

    if prediction[0][0] > prediction[0][1] and prediction[0][0] > 0.55:
        return categorie[0], prediction[0][0]
    if prediction[0][1] > prediction[0][0] and prediction[0][1] > 0.55:
        return categorie[1], prediction[0][1]
    else:
        return categorie[2], 0
