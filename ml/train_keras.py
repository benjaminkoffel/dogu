from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential, model_from_yaml
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras import backend as K

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D( 32, kernel_size=(3, 3), strides=(2, 2), activation='elu', input_shape=input_shape))
model.add(Conv2D( 32, kernel_size=(3, 3), strides=(1, 1), activation='elu', input_shape=input_shape))
model.add(Conv2D( 64, kernel_size=(3, 3), strides=(2, 2), activation='elu', input_shape=input_shape))
model.add(Conv2D( 64, kernel_size=(3, 3), strides=(1, 1), activation='elu', input_shape=input_shape))
model.add(Conv2D(128, kernel_size=(3, 3), strides=(1, 1), activation='elu', input_shape=input_shape))
model.add(GlobalAveragePooling2D())
model.add(Dense(num_classes, activation='sigmoid'))
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
with open('model.yaml', 'w') as f:
    f.write(model.to_yaml())
model.save_weights('model.h5')
print('LOSS: {} ACCURACY: {}'.format(score[0], score[1]))

with open('model.yaml', 'r') as f:
    model = model_from_yaml(f.read())
model.load_weights('model.h5')
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
score = model.evaluate(x_test, y_test, verbose=0)
print('LOSS: {} ACCURACY: {}'.format(score[0], score[1]))
