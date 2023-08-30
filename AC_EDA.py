import string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from math import ceil

df = pd.read_csv(r"C:\Users\cvhs3\Desktop\Python_files\Assassin's Creed Project\AC_stats\AC_vgsales.csv")
# 'r' in front converts normal string into a raw string

print(df)

# dropping all rows with empty columns ranging from 'Critic_Score' to 'Global_Score'
df2 = df.dropna(subset=['Critic_Score', 'User_Score', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales',
                        'Global_Sales'], how='all').reset_index(drop=True)

# replacing 'Global_Sales' values as sum of all sales
df2['Global_Sales'] = df2.loc[:, 'NA_Sales':'Other_Sales'].sum(axis=1)
pd.options.mode.chained_assignment = None  # disables SettingWithCopyWarning

# ******************* Sprinkle ********************* #
# checking if there are special characters in 'Name' column
alphabet = string.ascii_letters + string.punctuation
print(alphabet)
print(f"Are there special characters in any AC game?: {df2.Name.str.strip(alphabet).astype(bool).any()}")

# revealing game names with accented characters
accented = df2.Name.str.encode('ascii', errors='ignore') != df2.Name.str.encode('ascii', errors='replace')
print(f"\nAC games with accented characters: \n{df2[accented]['Name'].unique()}\n")
# ********************** End *********************** #

'''
************* Exploratory Data Analysis **************
'''
# Top values in the dataset
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

'''Sales vs. critic scores'''
# searching for outliers
fig, ax = plt.subplots(1, 1, figsize=(12, 5))

sns.regplot(x='Critic_Score', y='Global_Sales', data=df2, ci=None, color='#75556c', x_jitter=.02).set(ylim=(0, 17.5))

# cleaning the messy plot line above
sns.regplot(x='Critic_Score', y='Global_Sales', data=df2.loc[df2.Year >= 2007], truncate=True, x_bins=15,
            color='#75556c').set_title('Critic Score to Global Sales Correlation')

# Defining "hits" as those with sales above 1 million sales
dfa = df2
dfa = dfa.copy()
dfb = dfa[['Name', 'Platform', 'Genre', 'Publisher', 'Year', 'Critic_Score', 'Global_Sales']]
dfb = dfb.dropna().reset_index(drop=True)
df3 = dfb[['Platform', 'Genre', 'Publisher', 'Year', 'Critic_Score', 'Global_Sales']]
df3['Hit'] = df3['Global_Sales']
df3.drop('Global_Sales', axis=1, inplace=True)


def hit(sales):
    if sales >= 1:
        return 1
    else:
        return 0


df3['Hit'] = df3['Hit'].apply(lambda x: hit(x))

# Logistic Regression plot
sns.regplot(x='Critic_Score', y='Hit', data=df3, logistic=True, n_boot=500, y_jitter=.04, color='#75556c')\
    .set_title('Logistic Regression Between Critic Scores and Hits (>= 1 mil Sales)')
plt.show()

'''
************* Prediction Modeling ************** 
'''

