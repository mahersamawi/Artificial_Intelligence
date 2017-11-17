import math
from matplotlib import pyplot as plt

training_labels_array = []
training_images_array = []
label_counts = [0 for i in range(10)]
priors = [0 for i in range(10)]
num_images = 0

# below are the laplace constants we tried; seems like 0.01 is best one as the bigger it gets the worse
# the accuracy gets

# constants | accuracy 
# 0.1 | 75.2
# 0.01 | 75.4
# 0.2 | 75.1
# 0.001 | 75.4
# 0.5 | 75
# 1 | 74.7
# 5 | 74.8
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
confusion_matrix = [[0 for i in range(10)] for j in range(10)]


while image_index < num_images:
    current_label = int(training_labels_array[image_index])
    current_image = get_image(image_index)
    label_counts[current_label] += 1
    for i in range(28):
        line = current_image[i]
        for j in range(28):
            pixel = line[j]
            if pixel != ' ':
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
                if pixel != ' ':
                    class_prob[class_index] += math.log(totals[class_index][row][col])
                else:
                    class_prob[class_index] += math.log(1 - totals[class_index][row][col])
    image_index += 1
    output = class_prob.index(max(class_prob))
    test_output.append(output)
    total_test_labels[expected_label] += 1
    if output == expected_label:
        num_correct += 1
        test_label_output[expected_label] += 1
    else:
        confusion_matrix[output][expected_label] += 1
        #print("Misidentified: |" + str(output) + "|" + str(expected_label) + "|")

for i in range(len(test_label_output)):
    test_label_output[i] /= total_test_labels[i]
    print("Label " + str(i) + " Accuracy: " + str(test_label_output[i]))

print("Number correct: " + str(num_correct))
print("Percentage correct: " + str(num_correct/num_test_images))

for i in range(len(confusion_matrix)):
    for j in range(len(confusion_matrix[i])):
        confusion_matrix[i][j] = round(confusion_matrix[i][j] / total_test_labels[i], 3)

print("Confusion Matrix")

for i in confusion_matrix:
    print(i)
    # print(max(i))
    # print(i.index((max(i))))


def plot_likelihood(c_val, c_arr):
    for row in range(len(totals[c_val])):
        for col in range(len(totals[c_val][row])):
            val = math.log(totals[c_val][row][col])
            c_arr[row][col] = val
    plt.figure()
    plt.imshow(c_arr, cmap='rainbow', interpolation='nearest')
    plt.colorbar()
    plt.savefig('./output_figures/likelihood_for_' + str(c_val) + '.png', dpi=100)


def plot_odds_ratio(c_val1, c_val2, c_arr):
    for row in range(len(totals[c_val1])):
        for col in range(len(totals[c_val1][row])):
            val1 = totals[c_val1][row][col]
            val2 = totals[c_val2][row][col]
            c_arr[row][col] = math.log(val1 / val2)
    plt.figure()        
    plt.imshow(c_arr, cmap='rainbow', interpolation='nearest', vmin=-3, vmax=1.5)
    plt.colorbar()
    plt.savefig('./output_figures/odds_ratio_for_' + str(c_val1) + "_over_" + str(c_val2) + '.png', dpi=100)


c1 = [9, 3, 9, 8]
c2 = [4, 5, 7, 5]
# highest_confusion_values for the pairs = [23, 22, 21, 19.4]
c1_arr = [[0 for i in range(28)] for j in range(28)]
c2_arr = [[0 for i in range(28)] for j in range(28)]
odds_arr = [[0 for i in range(28)] for j in range(28)]
for i in range(4):
    plot_likelihood(c1[i], c1_arr)
    plot_likelihood(c2[i], c2_arr)
    plot_odds_ratio(c1[i], c2[i], odds_arr)


