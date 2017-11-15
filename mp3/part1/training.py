trainingimages = "./digitdata/trainingimages"
traininglabels = "./digitdata/traininglabels"

training_labels_array = []
training_images_array = []
label_counts = [0 for i in range(10)]
priors = [0 for i in range(10)]
num_images = 0
laplace_constant = 1

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


with open(traininglabels) as text_file:
    for line in text_file:
        training_labels_array.append(line.rstrip('\n'))


with open(trainingimages) as text_file:
    for line in text_file:
        training_images_array.append(line.rstrip('\n'))


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
print("number images: " + str(num_images))
# for i in range(28):
#     for j in range(28):
#         print(totals[5][i][j], end="")
#     print("")


