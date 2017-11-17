import math

training_images_array_no = []
training_images_array_yes = []
label_counts = [0 for i in range(2)]
priors = [0 for i in range(2)]
num_images = 0
laplace_constant = 0.1


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
            priors[i] = label_counts[i]/num_images_no
        else:
            priors[i] = label_counts[i] / num_images_yes


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
    print(current_image)
    label_counts[current_label] += 1
    for i in range(25):
        print(len(current_image[i]))
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

get_averages()
print(label_counts)
print(priors)

# Testing part
