import pandas

data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20240227.csv")

count = data["Primary Fur Color"].value_counts()

count.to_csv("countOf_fur.csv")

print(count)