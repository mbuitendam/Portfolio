import pandas

data = pandas.read_csv("weather_data.csv")
#print(data["temp"])

data_dict = data.to_dict()
#print(data_dict)

data_list = data["temp"].to_list()

#print(data["temp"].max())


# Long way 
total = 0
for num in data_list:
    total += num  
average = total / len(data_list)
#print(average)

print(data[data.temp == data.temp.max()])

monday = data[data.day == "Monday"]
print(monday.condition)