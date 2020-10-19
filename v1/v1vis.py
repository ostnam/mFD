import matplotlib
import matplotlib.pyplot
import pandas
import csv

dataframe = pandas.read_csv("flightdata1.csv", sep=",", header="infer")
print(dataframe)
fig, ax = matplotlib.pyplot.subplots()upy