import math

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
                    dot_product += weights[class_label][row][col] + b
        dot_products_list.append(dot_product)
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


b = 1
label_counts = [0 for i in range(10)]
training_labels_array = get_file("traininglabels")
training_images_array = get_file("trainingimages")
num_images = int(len(training_images_array)/28)
image_index = 0
weights = [[[0 for k in range(28)] for j in range(28)] for i in range(10)]
confusion_matrix = [[0 for i in range(10)] for j in range(10)]
epochs = 5
current_epoch = 0
alpha = 1
decay_rate = 1000
final_results = [0 for i in range(num_images)]
# Training
while current_epoch < epochs:
    image_index = 0
    while image_index < num_images:
        current_label = int(training_labels_array[image_index])
        current_image = get_image(image_index, training_images_array)
        label_counts[current_label] += 1
        classified_label = classify(current_image)
        final_results[image_index] = classified_label
        # Check if prediction was right
        check_prediction(classified_label, current_label, current_image)
        image_index += 1
    print("Incrementing epoch")
    current_epoch += 1
    alpha = decay_rate / (decay_rate + current_epoch)

total_correct_training = 0
for i in range(len(final_results)):
    if int(final_results[i]) == int(training_labels_array[i]):
        total_correct_training += 1

print("Overall correct on training data: " + str(total_correct_training/num_images))

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
    if int(final_results_testing[i]) == int(test_labels_array[i]):
        total_correct_test += 1

print("Overall correct on test data: " + str(total_correct_test/num_test_images))