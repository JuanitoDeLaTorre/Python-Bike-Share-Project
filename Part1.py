#given a dictionary n with keys representing the cost in dollars of a firework and values representing the
#potential height of that firework, write a function to return the index of the most cost efficient
#firework as well as the average price (feet/dollar)
n = {
    42: 115,
    30: 85,
    20: 120,
    50: 45
}

def murica(fireworks):

    counter = 0
    returnIndex = 0
    runningAvg = 0.0
    avgArray = []

    for key, val in fireworks.items():

        avgArray.append(val/key)

        if val/key > runningAvg:
            runningAvg = val/key
            returnIndex = counter

        counter += 1

    sum = 0.0
    for val in avgArray:
        sum += val

    totalAvg = sum/len(fireworks)

    return [returnIndex, round(totalAvg, 2)]


print(murica(n))
list = ['hello', 'there']

print(' $ '.join(list))







