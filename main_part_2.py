"""
main script part 2

RUN THIS ONLY AFTER RUNNING MAIN.PY!

@author: kevi
"""

import algorithms as al
from dot import Dot
import pandas as pd
import numpy as np

# First read in the generated data as a dataframe.
df = pd.read_csv("particle_data.csv")
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
labels = [string for string in df.columns]
df_array = df.to_numpy()

# May use this column a lot since it specifies frame where particle is:
frames = df_array[:, 0]


# Useful function for splicing data:
def get_data(n):
    """

    Parameters
    ----------
    n : integer
        Frame number to get data from.

    Returns
    -------
    data : Numpy Array
        Returns a spliced version of the whole data set involving only the desired frame.

    """
    mask = frames == n
    return df_array[mask, :]


# Initialize the data sets and create overall structure for analysis.
df_0 = get_data(0)
dot_list = []
for row in df_0:
    new_dot = Dot()
    new_dot.add(row)
    dot_list.append(new_dot)

# That wraps up the initial case. Now we need to start iterating and doing actual work.
for i in range(df_array.shape[0] - 1):  # iterates through all subsets of main spreadsheet
    data_slice = get_data(i+1)  # Work with a subset of the data
    for dot in dot_list:  # Try to match particles for each instance in the dot list
        if dot.active is True:
            current = dot.last_entry()

            print("hi")
example = dot_list[0]
print(example.last_entry())
print("yes")



