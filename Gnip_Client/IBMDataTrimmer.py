with open('output.csv', 'rb') as csvfile:
    counter_1 = 0.0
    counter_2 = 0.0
    counter_3 = 0.0
    counter_4 = 0.0
    counter_5 = 0.0
    total_counter = 0
    i = 0
    for row in csvfile:
        res = row.split(',')

        counter_1 += float(res[1])
        counter_2 += float(res[2])
        counter_3 += float(res[3])
        counter_4 += float(res[4])
        counter_5 += float(res[5])
        total_counter += 1

        if total_counter == 1000:
            # print("Counter: " + str(i) + " Anger: " + str(counter_1/1000) + ", Disgust: " + str(counter_2/1000) + ", Fear: " + str(counter_3/1000) + ", Joy: " + str(counter_4/1000) + ", Sadness: " + str(counter_5/1000))
            print(str(i) + "," + str(counter_1/1000) + "," + str(counter_2/1000) + "," + str(counter_3/1000) + "," + str(counter_4/1000) + "," + str(counter_5/1000))
            counter_1 = 0.0
            counter_2 = 0.0
            counter_3 = 0.0
            counter_4 = 0.0
            counter_5 = 0.0
            i += 1
            total_counter = 0