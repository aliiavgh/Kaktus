import pandas as pd

data = pd.read_csv('news.csv', sep=";", error_bad_lines=False)
print(data.columns)