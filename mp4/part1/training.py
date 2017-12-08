import math
import random

def get_image(current_index, list_with_image):
    current_image = []
    for i in range(28):
        image_line = list_with_image[current_index * 28 + i]
        current_image.append(image_line)
    return current_image


def get_file(file_name):
    arr = []
    file_name = "./../digitdata/" + file_name
    with open(file_name) as text_file:
        for line in text_file:
            arr.append(line.rstrip('\n'))
    return arr


def classify(current_image):
    dot_products_list = []
    for class_label in range(10):
        dot_product = 0
        for row in range(28):
            for col in range(28):
                if current_image[row][col] != ' ':
                    dot_product += (weights[class_label][row][col])
        dot_products_list.append(dot_product + bias)
    return dot_products_list.index((max(dot_products_list)))


def check_prediction(classified_label, correct_label, current_image):
    if int(classified_label) != int(correct_label):
        # updated both weights
        for class_label in range(10):
            for row in range(28):
                for col in range(28):
                    if current_image[row][col] != ' ':
                        weights[correct_label][row][col] += alpha
                        weights[classified_label][row][col] -= alpha


def get_training_accuracy(current_run):
    total_correct_training = 0
    for i in range(len(final_results)):
        if int(final_results[i]) == int(training_labels_array[i]):
            total_correct_training += 1

    print("Overall correct on training data for epoch " + str(current_run) + ": " + str(total_correct_training / num_images))


# variables to mess around with (besides training image order)
bias = 1 # is this bias?

decay_rate = 0
# decay_rate = 0 gives 78% for first training epoch, then 86% for every subsequent epoch, and for testing gives 79%
# decay_rate = 1 gives 95%/83.4% for training/testing
# decay_rate = 10 gives 93%/77.6% for training/testing
# decay_rate = 100 gives 92%/81.6% for training/testing
# decay_rate = 1000 gives 92%/81.7% for training/testing

weights = [[[0 for k in range(28)] for j in range(28)] for i in range(10)]

epochs = 6

label_counts = [0 for i in range(10)]
training_labels_array = get_file("traininglabels")
training_images_array = get_file("trainingimages")
num_images = int(len(training_images_array)/28)
image_index = 0
confusion_matrix = [[0 for i in range(10)] for j in range(10)]
current_epoch = 1
alpha = 1
final_results = [0 for i in range(num_images)]
# Training
while current_epoch < epochs:
    image_index_array = [i for i in range(num_images)]
    image_index = random.choice(image_index_array)
    image_index_array.remove(image_index)
    while image_index < num_images-1:
        current_label = int(training_labels_array[image_index])
        current_image = get_image(image_index, training_images_array)
        label_counts[current_label] += 1
        classified_label = classify(current_image)
        final_results[image_index] = classified_label
        # Check if prediction was right
        check_prediction(classified_label, current_label, current_image)
        image_index = random.choice(image_index_array)
        image_index_array.remove(image_index)
    get_training_accuracy(current_epoch)
    #print("Incrementing epoch")
    current_epoch += 1
    alpha = decay_rate / (decay_rate + current_epoch)

get_training_accuracy(current_epoch)

# Testing
test_images_array = get_file("testimages")
test_labels_array = get_file("testlabels")
test_output = []
total_test_labels = [0 for i in range(10)]
test_label_output = [0 for i in range(10)]
image_index = 0
num_correct = 0
num_test_images = int(len(test_labels_array))
final_results_testing = [0 for i in range(num_test_images)]
image_index = 0
while image_index < num_test_images:
    current_label = int(test_labels_array[image_index])
    current_image = get_image(image_index, test_images_array)
    label_counts[current_label] += 1
    classified_label = classify(current_image)
    final_results_testing[image_index] = classified_label
    image_index += 1

total_correct_test = 0
for i in range(len(test_labels_array)):
    expected_label = int(test_labels_array[i])
    output_label = int(final_results_testing[i])
    total_test_labels[expected_label] += 1
    if output_label == expected_label:
        total_correct_test += 1
        test_label_output[expected_label] += 1
    else:
        # Classified incorrectly
        confusion_matrix[expected_label][output_label] += 1

print("Overall correct on test data: " + str(total_correct_test/num_test_images))

for i in range(len(confusion_matrix)):
    for j in range(len(confusion_matrix[i])):
        confusion_matrix[j][i] = format(round(confusion_matrix[j][i] / total_test_labels[i], 3), '.3f')

print("Confusion Matrix")
for i in confusion_matrix:
    print(i)

for i in range(len(test_label_output)):
    test_label_output[i] /= total_test_labels[i]
    print("Label " + str(i) + " Accuracy: " + str(test_label_output[i]))
