# import pandas as pd
# df_1 = pd.read_csv("./flight_data/1987.csv")
# df_2 = pd.read_csv("./flight_data/1988.csv")

import pandas as pd
df1 = pd.read_csv("./flight_data/1987.csv")
df = pd.concat([df1, pd.read_csv("./flight_data/1988.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1989.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1990.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1991.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1992.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1993.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1994.csv")])
df = pd.concat([df, pd.read_csv("./flight_data/1995.csv")])