import math

training_images_array_no = []
training_images_array_yes = []
label_counts = [0 for i in range(2)]
priors = [0 for i in range(2)]
num_images = 0
laplace_constant = 5


def get_file(file_name):
    arr = []
    file_name = "../yesno/" + file_name
    with open(file_name) as text_file:
        for line in text_file:
            arr.append(line.rstrip('\n'))
    return arr


def get_sound(current_index, yes_no):
    # 25 x 10 sounding
    current_sound = []
    for i in range(25):
        if yes_no == "yes":
            sound_line = training_labels_images_yes[current_index * 28 + i]
        else:
            sound_line = training_labels_images_no[current_index * 28 + i]
        current_sound.append(sound_line)

    return current_sound


def get_averages():
    for label in range(2):
        num_labels = label_counts[label]
        for row in range(25):
            for col in range(10):
                totals[label][row][col] += laplace_constant
                totals[label][row][col] /= (num_labels * laplace_constant)

    for i in range(2):
        if i == 0:
            priors[i] = label_counts[i] / (num_images_no + num_images_yes)
        else:
            priors[i] = label_counts[i] / (num_images_no + num_images_yes)


training_labels_images_no = get_file("no_train.txt")
training_labels_images_yes = get_file("yes_train.txt")

num_images_no = (3669 - 1) / 28
num_images_yes = (3921 - 1) / 28


totals = [[[0 for k in range(10)] for j in range(25)] for i in range(2)]

print(num_images_yes)
print(num_images_no)
image_index = 0
# yes bucket
while image_index < num_images_yes:
    current_label = 1
    current_image = get_sound(image_index, "yes")
    label_counts[current_label] += 1
    for i in range(25):
        line = current_image[i]
        for j in range(10):
            pixel = line[j]
            if pixel != ' ':
                totals[current_label][i][j] += 1
    image_index += 1

image_index = 0
# no bucket
while image_index < num_images_no:
    current_label = 0
    current_image = get_sound(image_index, "no")
    label_counts[current_label] += 1
    for i in range(25):
        line = current_image[i]
        for j in range(10):
            pixel = line[j]
            if pixel != ' ':
                totals[current_label][i][j] += 1
    image_index += 1


print(label_counts)
get_averages()
print(priors)
# Testing part

test_images_array_yes = get_file("yes_test.txt")
test_images_array_no = get_file("no_test.txt")

test_output = []
total_test_labels = [0 for i in range(2)]
test_label_output = [0 for i in range(2)]
image_index = 0
num_correct = 0
num_test_images_yes = 1400 / 28
num_test_images_no = 1400 / 28
num_test_images = num_test_images_yes + num_test_images_no
# yes testing
print("Yes testing")
while image_index < num_test_images_yes:
    class_prob = [0 for i in range(2)]
    expected_label = 1
    test_image = []
    for i in range(25):
        image_line = test_images_array_yes[image_index * 28 + i]
        test_image.append(image_line)
    for class_index in range(2):
        class_prob[class_index] = math.log(priors[class_index])
        for row in range(25):
            line = test_image[row]
            for col in range(10):
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
        # confusion_matrix[output][expected_label] += 1
        print("Misidentified: |" + str(output) + "|" + str(expected_label) + "|")

print("No testing")
#  No testing
while image_index < num_test_images_no:
    class_prob = [0 for i in range(2)]
    expected_label = 0
    test_image = []
    for i in range(25):
        image_line = test_images_array_no[image_index * 28 + i]
        test_image.append(image_line)
    for class_index in range(2):
        class_prob[class_index] = math.log(priors[class_index])
        for row in range(25):
            line = test_image[row]
            for col in range(10):
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
        #confusion_matrix[output][expected_label] += 1
        print("Misidentified: |" + str(output) + "|" + str(expected_label) + "|")
for i in range(len(test_label_output)):
    test_label_output[i] /= total_test_labels[i]
    print("Label " + str(i) + " Accuracy: " + str(test_label_output[i]))

print("Number correct: " + str(num_correct))
print("Percentage correct: " + str(num_correct/num_test_images))