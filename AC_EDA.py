import string
import pandas as pd

# 'r' in front converts normal string into a raw string
df = pd.read_csv(r"C:\Users\cvhs3\Desktop\Python_files\Assassin's Creed Project\AC_stats\AC_vgsales.csv")
print(df)

# dropping all rows with empty columns ranging from 'Critic_Score' to 'Global_Score'
df2 = df.dropna(subset=['Critic_Score', 'User_Score', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales',
                        'Global_Sales'], how='all').reset_index(drop=True)
# replacing 'Global_Sales' values as sum of all sales
df2['Global_Sales'] = df2.loc[:, 'NA_Sales':'Other_Sales'].sum(axis=1)
pd.options.mode.chained_assignment = None # disables SettingWithCopyWarning
print(df2)

# ******************* Sprinkle ********************* #
# checking if there are special characters in 'Name' column
alphabet = string.ascii_letters+string.punctuation
print(alphabet)
print(f"Are there special characters in any AC game?: {df2.Name.str.strip(alphabet).astype(bool).any()}")

# revealing game names with accented characters
accented = df2.Name.str.encode('ascii', errors='ignore') != df2.Name.str.encode('ascii', errors='replace')
print(f"\nAC games with accented characters: \n{df2[accented]['Name'].unique()}\n")
# ********************** End *********************** #

#############################
# Exploratory Data Analysis #
#############################

# top values in the dataset

