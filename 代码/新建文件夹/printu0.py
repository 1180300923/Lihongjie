import pickle
data = pickle.load(open('pickle/web_sequence.pickle', 'rb'))
webpages = data.keys()
print(webpages)

for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        if number == 7 or number == 8:
            print(number)
            print(data[webpage][number])