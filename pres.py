import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np

fp = "/Users/eab06/Desktop/WJB/PythonProjects/2020 Polling Error/Pres/cb_2019_us_state_5m (1)/cb_2019_us_state_5m.shp"

map_df = gpd.read_file(fp)

df = pd.read_csv("/Users/eab06/Desktop/WJB/PythonProjects/2020 Polling Error/Pres/polls_bias_pres.csv")

merged = map_df.set_index('NAME').join(df.set_index('State'))

variable = "d_bias_with_omit"
vmin, vmax = -15, 15


fig, ax = plt.subplots(1, figsize=(10, 6))
merged.plot(column=variable, cmap='RdBu', norm=plt.Normalize(vmin=vmin, vmax=vmax), linewidth=1, ax=ax, edgecolor='0.8', missing_kwds = dict(color = "xkcd:dark gray",))

# add nebraska CD votes
norm = matplotlib.colors.Normalize(vmin=-15,vmax=15)
red_blue = cm.get_cmap('RdBu')
for i in range(3):
    margin = df[df['State'] == f"NE-{i+1}"].iloc[0]['d_bias_with_omit']
    print(margin, type(margin), margin=='nan')
    color = 'xkcd:dark gray' if str(margin) == 'nan' else red_blue(norm(margin))
    rectangle = plt.Rectangle((-101 + 1.2*i, 41), 1, 1, fc=color, ec='0.8')
    plt.gca().add_patch(rectangle)


# maine
for i in range(2):
    margin = df[df['State'] == f"ME-{i+1}"].iloc[0]['d_bias_with_omit']
    color = 'xkcd:dark gray' if str(margin) == 'nan' else red_blue(norm(margin))
    rectangle = plt.Rectangle((-70.2 + 1.2*i, 45), 1, 1, fc=color, ec='0.8')
    plt.gca().add_patch(rectangle)


# finally, show it all
sm = plt.cm.ScalarMappable(cmap='RdBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))

leg = fig.colorbar(sm)

plt.title("Error in forecasting the 2020 USA presidential election")
plt.xlim(-125, -67)
plt.ylim(25, 50)
plt.axis("off")

leg.set_label('Polling error towards Biden (pp.)', rotation=270)

ak_error = df[df['State'] == "Alaska"].iloc[0]['d_bias_with_omit']
hi_error = df[df['State'] == "Hawaii"].iloc[0]['d_bias_with_omit']
plt.text(-125, 20, f"""
    Compares final 538 polls-plus forecast
    to results as they come in. At time of
    writing (10:20 CST, Nov 4), AK, AZ, GA,
    NC, NV, and PA are too close to call.

    Not shown: 
    AK: {round(ak_error, 1)}%, HI: {round(hi_error, 1)}% (both to Biden).
""", fontsize=6)
plt.show()

