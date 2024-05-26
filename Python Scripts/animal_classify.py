import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import applications
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

data = "Data/classifier"

size = 224
batch_size = 32
epochs = 15

# Augmenting data
gen = ImageDataGenerator(rescale=1./255., horizontal_flip=True, validation_split=0.2)

X_train = gen.flow_from_directory(data, target_size=(size, size), batch_size=batch_size, class_mode='categorical', subset="training", color_mode="rgb", shuffle=True, seed=42)
X_test = gen.flow_from_directory(data, target_size=(size, size), batch_size=batch_size, class_mode='categorical', color_mode="rgb", subset="validation", shuffle=True, seed=42)

# Model
base_model = applications.InceptionResNetV2(include_top=False, weights='imagenet', input_shape=(size, size,3))

base_model.trainable = False

model = Sequential([
    base_model,
    BatchNormalization(),
    GlobalAveragePooling2D(),
    Dense(512, activation='relu'),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(6, activation='softmax')
])

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

checkpoint = ModelCheckpoint('animal.keras', monitor='val_loss', mode='min', save_best_only=True)
early = EarlyStopping(patience=10, min_delta=0.001, restore_best_weights=True)

history = model.fit(X_train, validation_data=X_test, epochs=epochs, callbacks=[checkpoint, early])

# Plotting
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(10, 16))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.title(f'\nTraining and Validation Accuracy. \nTrain Accuracy: {str(acc[-1])}\nValidation Accuracy: {str(val_acc[-1])}')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.title(f'Training and Validation Loss. \nTrain Loss: {str(loss[-1])}\nValidation Loss: {str(val_loss[-1])}')
plt.xlabel('epoch')
plt.tight_layout(pad=3.0)
plt.show()

accuracy_score = model.evaluate(X_test)
print("Accuracy: {:.4f}%".format(accuracy_score[1] * 100)) 
print("Loss: ",accuracy_score[0]) 
