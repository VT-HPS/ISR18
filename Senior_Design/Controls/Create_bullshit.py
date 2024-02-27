data1 = [18, 16, 14, 12]
data2 = [14, 10, 6, 2, -2, -6, -10, -14]
data_tuples = []

for i in data1:
    for j in data2:
        data_tuples.append((i, j))

print(data_tuples)