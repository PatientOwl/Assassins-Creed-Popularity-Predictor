import pandas as pd
import numpy as np

# 'r' in front converts normal string into a raw string
df = pd.read_csv(r"C:\Users\cvhs3\Desktop\Python_files\Assassin's Creed Project\AC_stats\AC_vgsales.csv")
print(df[:5])

# dropping all rows with empty columns ranging from 'Critic_Score' to 'Global_Score'
df2 = df.dropna(subset=['Critic_Score', 'User_Score', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales',
                        'Global_Sales'], how='all')
# replacing 'Global_Sales' values as sum of all sales
df2['Global_Sales'] = df2.loc[:, 'NA_Sales':'Other_Sales'].sum(axis=1)

print(df2)
