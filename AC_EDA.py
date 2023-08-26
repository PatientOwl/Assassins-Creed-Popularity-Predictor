import string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 'r' in front converts normal string into a raw string
df = pd.read_csv(r"C:\Users\cvhs3\Desktop\Python_files\Assassin's Creed Project\AC_stats\AC_vgsales.csv")
print(df)

# dropping all rows with empty columns ranging from 'Critic_Score' to 'Global_Score'
df2 = df.dropna(subset=['Critic_Score', 'User_Score', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales',
                        'Global_Sales'], how='all').reset_index(drop=True)
# replacing 'Global_Sales' values as sum of all sales
df2['Global_Sales'] = df2.loc[:, 'NA_Sales':'Other_Sales'].sum(axis=1)
pd.options.mode.chained_assignment = None  # disables SettingWithCopyWarning
print(df2)

# ******************* Sprinkle ********************* #
# checking if there are special characters in 'Name' column
alphabet = string.ascii_letters + string.punctuation
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
columns = ['Platform', 'Developer']

for col in columns:
    chart = df2[['Name', col]].groupby([col]).count().sort_values('Name', ascending=False).reset_index()
    sns.set_style('white')
    plt.figure(figsize=(12.4, 5))
    plt.xticks(rotation=90)
    sns.barplot(x=col, y='Name', data=chart, palette=sns.cubehelix_palette((12 if col == 'Developer' else 30),
                                                                           dark=0.3, light=.85, reverse=True)
                ).set_title(('Game Count by ' + col), fontsize=16)
    plt.ylabel('Count', fontsize=14)
    plt.xlabel('')

col_metrics = ['Critic_Score', 'Global_Sales']

for metric in col_metrics:
    chart2 = df2[['Name', metric]].groupby(['Name']).mean().sort_values('Name', ascending=False).reset_index()
    sns.set_style('white')
    plt.figure(figsize=(12.4, 5))
    sns.barplot(x=metric, y='Name', data=chart2, palette=sns.cubehelix_palette((12 if metric == 'Global_Sales' else 30),
                                                                               dark=0.3, light=.85, reverse=True)
                ).set_title(('Game metric by Critic Score' if metric == 'Critic_Score'
                             else 'Game metric by Global Sales'), fontsize=16)
    plt.ylabel('')
    if metric == 'Critic_Score':
        plt.xlabel('Score (out of 10)')
    else:
        plt.xlabel('Sales (in millions)')
    plt.show()
