import math
import tensorflow as tf
import tensorflow_datasets as tfds

# Configurar el nivel de registro de TensorFlow
tf.get_logger().setLevel('ERROR')

# Cargar el conjunto de datos MNIST
dataset, metadata = tfds.load('mnist', as_supervised=True, with_info=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

# Normalizar las imágenes y convertir las etiquetas a números
def normalize(images, labels):
    images = tf.cast(images, tf.float32)
    images /= 255
    return images, labels

train_dataset = train_dataset.map(normalize)
test_dataset = test_dataset.map(normalize)

# Estructura del modelo
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1), name='input_layer'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(28, activation='relu', name='hidden_layer1'),
    tf.keras.layers.Dense(28, activation='relu', name='hidden_layer2'),
    tf.keras.layers.Dense(10, activation='softmax', name='output_layer')
])

# Compilar el modelo
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Definir tamaño de lote y preprocesamiento adicional
BATCH_SIZE = 32
train_dataset = train_dataset.repeat().shuffle(metadata.splits['train'].num_examples).batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)

# Entrenar el modelo
model.fit(
    train_dataset,
    epochs=5,
    steps_per_epoch=math.ceil(metadata.splits['train'].num_examples / BATCH_SIZE)
)

# Guardar el modelo como archivo .h5
model.save('trained_model.h5')
print("Modelo guardado como trained_model.h5")

# Evaluar el modelo en el conjunto de pruebas
test_loss, test_accuracy = model.evaluate(test_dataset, steps=math.ceil(metadata.splits['test'].num_examples / BATCH_SIZE))
print("Precisión en el conjunto de pruebas:", test_accuracy)




#
# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import logging
#
# import tensorflow as tf
# import tensorflow_datasets as tfds
#
# logger = tf.get_logger()
# logger.setLevel(logging.ERROR)
#
# dataset, metadata = tfds.load('mnist', as_supervised=True, with_info=True)
# train_dataset, test_dataset = dataset['train'], dataset['test']
#
# class_names = metadata.features['label'].names
#
# num_train_examples = metadata.splits['train'].num_examples #60 mil datos train
# num_test_examples = metadata.splits['test'].num_examples #10 mil datos test
#
# #Normalizar: Numeros de 0 a 255, que sean de 0 a 1
# def normalize(images, labels):
#   images = tf.cast(images, tf.float32)
#   images /= 255
#   return images, labels
#
#
# train_dataset = train_dataset.map(normalize)
# test_dataset = test_dataset.map(normalize)
#
# #Estructura de la red
# model = tf.keras.Sequential([
#      tf.keras.layers.Flatten(input_shape=(28,28,1)), #Capa de entrada
#      tf.keras.layers.Dense(28, activation=tf.nn.relu), #Capas oculta
#      tf.keras.layers.Dense(28, activation=tf.nn.relu), #Capas oculta
#      tf.keras.layers.Dense(10, activation=tf.nn.softmax) #para clasificacion
# ])
#
# #Función que compila el modelo
# model.compile(
#     optimizer='adam',
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
#
# #Aprendizaje por lotes de 32 cada lote
# BATCHSIZE = 32
# train_dataset = train_dataset.repeat().shuffle(num_train_examples).batch(BATCHSIZE)
# test_dataset = test_dataset.batch(BATCHSIZE)
#
#
# #Realizar el aprendizaje
# model.fit(
#     train_dataset, epochs=5,
#     steps_per_epoch=math.ceil(num_train_examples/BATCHSIZE)
# )
#
# #Evaluar nuestro modelo ya entrenado, contra el dataset de pruebas
# test_loss, test_accuracy = model.evaluate(
#     test_dataset, steps=math.ceil(num_test_examples/32)
# )
#
# #Imprime los resultados de precisión
# print("Resultado en las pruebas: ", test_accuracy)