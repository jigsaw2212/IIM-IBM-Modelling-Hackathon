import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pdb

CSV_PATH = "/home/ramparkash/Data/StockData/"
FILES = os.listdir(CSV_PATH)
FILES = [CSV_PATH + f for f in FILES]
dat = None

for csv_file in FILES[0:2]:
    df = pd.read_csv(csv_file).set_index('Date')
    df = df.groupby(lambda x: int(x.split('-')[-1])).mean().reset_index()
    if dat is None:
        dat = df
    else:
        dat = pd.concat((dat, df))

print dat

#     min_max_scaler = preprocessing.MinMaxScaler()
#     try:
#         np_scaled = pd.DataFrame(
#             min_max_scaler.fit_transform(df["Close Price"]))
#         means.append(
#             list(np_scaled.rolling(window=50).mean().values.flatten()))
#     except Exception as e:
#         continue

# for m in means:
#     if len(m) > 1000:
#         input_means.append(m[:1000])
# num_clusters = 30


# input_means = np.array(input_means)
# input_means = np.nan_to_num(input_means)
# for i in range(len(input_means)):
#     plt.plot(range(len(input_means[i])), input_means[i])
#     plt.savefig("plots/"+str(i)+'.png')
