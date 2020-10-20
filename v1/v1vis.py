import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv("flightdata.csv", sep=", ", header="infer", index_col=0)
df2 = df[["pitch", "radaralt", "eas"]] # Selecting only the columns we intend to plot
plot = df2.plot(subplots=True, title="Flight data during a landing", color="black" )
plt.savefig("flightdata.png")
