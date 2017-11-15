import math

training_labels_array = []
training_images_array = []
label_counts = [0 for i in range(10)]
priors = [0 for i in range(10)]
num_images = 0
laplace_constant = 0.1

def get_image(current_index):
    current_image = []
    for i in range(28):
        image_line = training_images_array[current_index * 28 + i]
        current_image.append(image_line)
    return current_image

def get_averages():
    for label in range(10):
        num_labels = label_counts[label]
        for row in range(28):
            for col in range(28):
                totals[label][row][col] += laplace_constant
                totals[label][row][col] /= (num_labels * 2)

    for i in range(10):
        priors[i] = label_counts[i]/num_images

def get_file(file_name):
    arr = []
    file_name = "./digitdata/" + file_name
    with open(file_name) as text_file:
        for line in text_file:
            arr.append(line.rstrip('\n'))
    return arr


training_labels_array = get_file("traininglabels")
training_images_array = get_file("trainingimages")
num_images = len(training_images_array)/28
image_index = 0
totals = [[[0 for k in range(28)] for j in range(28)] for i in range(10)]

while image_index < num_images:
    current_label = int(training_labels_array[image_index])
    current_image = get_image(image_index)
    label_counts[current_label] += 1
    for i in range(28):
        line = current_image[i]
        for j in range(28):
            pixel = line[j]
            if (pixel != ' '):
                totals[current_label][i][j] += 1
    image_index += 1

get_averages()

# Testing
test_images_array = get_file("testimages")
test_labels_array = get_file("testlabels")
test_output = []
total_test_labels = [0 for i in range(10)]
test_label_output = [0 for i in range(10)]
image_index = 0
num_correct = 0
num_test_images = len(test_labels_array)

while image_index < num_test_images:
    class_prob = [0 for i in range(10)]
    expected_label = int(test_labels_array[image_index])
    test_image = []
    for i in range(28):
        image_line = test_images_array[image_index * 28 + i]
        test_image.append(image_line)
    for class_index in range(10):
        class_prob[class_index] = math.log(priors[class_index])
        for row in range(28):
            line = test_image[row]
            for col in range(28):
                pixel = line[col]
                if (pixel != ' '):
                    class_prob[class_index] += math.log(totals[class_index][row][col])
                else:
                    class_prob[class_index] += math.log(1 - totals[class_index][row][col])
    image_index += 1
    output = class_prob.index(max(class_prob))
    test_output.append(output)
    total_test_labels[expected_label] += 1
    if (output == expected_label):
        num_correct += 1
        test_label_output[expected_label] += 1
    else:
        print("Misidentified: |" + str(output) + "|" + str(expected_label) + "|")

for i in range(len(test_label_output)):
    test_label_output[i] /= total_test_labels[i]
    print("Label " + str(i) + " Accuracy: " + str(test_label_output[i]))

print("number correct: " + str(num_correct))
print("percentage correct: " + str(num_correct/num_test_images))
