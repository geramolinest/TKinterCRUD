import pandas as pd

data = pd.read_csv("/home/anon23/Documentos/python-ml-course/datasets/titanic/titanic3.csv")
for row in range(len(data)):
    for i in range(len(data.columns.tolist())):
        print(data.iloc[row][i])