import math  # For pow and sqrt
import sys
import random
from random import shuffle, uniform
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from flask import request




###_Pre-Processing_###


def ReadData(fileName):
    # Read the file, splitting by lines
    f = open(fileName, 'r')

    lines = f.read().splitlines()
    f.close()

    items = []

    for i in range(1, len(lines)):
        line = lines[i].split(',')
        itemFeatures = []

        for j in range(len(line) - 1):
            v = float(line[j])  # Convert feature value to float
            itemFeatures.append(v)  # Add feature value to list

        items.append(itemFeatures)

    shuffle(items)

    # Saving items graph
    # i = plt.figure(1)
    # for item in items:
    #     x, y = FindMaxMin(item)
    #     plt.scatter(x, y, s=7, c='b')
    # plt.savefig('static/images/items.png')
    # plt.close(i)
    return items


def FindMaxMin(item):
    min = sys.maxsize
    max = -sys.maxsize

    for i in item:
        if i > max:
            max = i
        if i < min:
            min = i

    return max, min


###_Auxiliary Function_###
def FindColMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]
    maxima = [-sys.maxsize - 1 for i in range(n)]

    for item in items:
        for f in range(len(item)):
            if (item[f] < minima[f]):
                minima[f] = item[f]

            if (item[f] > maxima[f]):
                maxima[f] = item[f]

    return minima, maxima


def EuclideanDistance(x, y):
    S = 0  # The sum of the squared differences of the elements
    for i in range(len(x)):
        S += math.pow(x[i] - y[i], 2)

    return math.sqrt(S)  # The square root of the sum


def InitializeMeans(items, k, cMin, cMax):
    # Initialize means to random numbers between
    # the min and max of each column/feature

    f = len(items[0])  # number of features
    means = [[0 for i in range(f)] for j in range(k)]

    for mean in means:
        for i in range(len(mean)):
            # Set value to a random float
            # (adding +-1 to avoid a wide placement of a mean)
            mean[i] = uniform(cMin[i] + 1, cMax[i] - 1)

    return means


def UpdateMean(n, mean, item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m * (n - 1) + item[i]) / float(n)
        mean[i] = round(m, 3)

    return mean


def FindClusters(means, items):
    clusters = [[] for i in range(len(means))]  # Init clusters

    for item in items:
        # Classify item into a cluster
        index = Classify(means, item)

        # Add item to cluster
        clusters[index].append(item)

    return clusters


###_Core Functions_###
def Classify(means, item):
    # Classify item to the mean with minimum distance

    minimum = sys.maxsize
    index = -1

    for i in range(len(means)):
        # Find distance from item to mean
        dis = EuclideanDistance(item, means[i])

        if (dis < minimum):
            minimum = dis
            index = i

    return index


def CalculateMeans(k, items, maxIterations=100000):
    # Find the minima and maxima for columns
    cMin, cMax = FindColMinMax(items)

    # Initialize means at random points
    means = InitializeMeans(items, k, cMin, cMax)

    # Showing graph with initial means and data
    # g = plt.figure(2)
    # for item in items:
    #     x, y = FindMaxMin(item)
    #     plt.scatter(x, y, s=7, c='blue')
    # for mean in means:
    #     x, y = FindMaxMin(mean)
    #     plt.scatter(x, y, marker='*', c='g', s=150)
    # plt.savefig('static/images/initial.png')
    # plt.close(g)
    # plt.show()

    # Initialize clusters, the array to hold
    # the number of items in a class
    clusterSizes = [0 for i in range(len(means))]

    # An array to hold the cluster an item is in
    belongsTo = [0 for i in range(len(items))]

    # Variable for storing total number of iterations
    count = 0

    # Calculate means
    for e in range(maxIterations):
        # If no change of cluster occurs, halt
        noChange = True

        count += 1
        for i in range(len(items)):
            item = items[i]
            # Classify item into a cluster and update the
            # corresponding means.

            index = Classify(means, item)

            clusterSizes[index] += 1
            means[index] = UpdateMean(clusterSizes[index], means[index], item)

            # Item changed cluster
            if (index != belongsTo[i]):
                noChange = False

            belongsTo[i] = index

        # Nothing changed, return
        if (noChange):
            break

    return means, count


###_Main_###
def main():
    items = ReadData('uploads/data.txt')
    # items = ReadData('data.txt')
    output = ''
    features = len(items[0])
    output += "Total Instances : " + str(len(items))
    output += "\nTotal Features : " + str(features)

    k = int(request.form['k'])
    # k = 3
    means, count = CalculateMeans(k, items)
    clusters = FindClusters(means, items)

    output += "\nNumber of Iterations : " + str(count)

    num = 1
    for cluster in clusters:
        output += "\nNumber of instances in Cluster " + str(num) + " : " + str(len(cluster))
        num += 1

    # Displaying mean and clusters
    # h = plt.figure(3)
    # for mean in means:
    #     x, y = FindMaxMin(mean)
    #     plt.scatter(x, y, marker='*', s=150)
    #
    #
    # for cluster in clusters:
    #     color = "%06x" % random.randint(0, 0xFFFFFF)
    #     for i in cluster:
    #         x, y = FindMaxMin(i)
    #         plt.scatter(x, y, s=7, c='#'+color)
    #
    # plt.savefig('static/images/clusters.png')
    # plt.close(h)
    # plt.show()

    # Printing cluster graph
    # x = features - 1
    fig, axs = plt.subplots(features,features, figsize=(10,8))
    for cluster in clusters:
        color = "%06x" % random.randint(0, 0xFFFFFF)
        for c in cluster:
            for i in range(features):
                for j in range(features):
                    # if(i!=j):
                    axs[i,j].scatter(c[i],c[j], s=7,c='#'+color)
                    axs[i,j].set_title('Feature ' + str(i+1) + ' and ' + str(j+1))
                    # else:
                    #     axs[i,j].scatter(c[features-1],c[i],s=7,c='#'+color)
                    #     axs[i,j].set_title('Feature 4 and ' + str(i+1))
    for mean in means:
        for i in range(features):
            for j in range(features):
                axs[i,j].scatter(mean[i],mean[j], marker='*', s=150)


    # Adjusting subplots
    plt.tight_layout()

    # Random int for randomizing file name
    ran = random.randint(1,500)
    plt.savefig('static/images/clusters'+str(ran)+'.png')
    # plt.show()

    # return clusters
    return output, ran
    # print("Total numbers of iterations :")
    # print(count)



    # for c in range(k):
    #     print("Printing cluster {} ".format(c + 1))
    #     print(means[c])
    #     print(clusters[c])
    #     print("")


if __name__ == "__main__":
    main()
