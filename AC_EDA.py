import string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

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


'''************* Exploratory Data Analysis **************'''
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

# Sales vs. critic scores
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

# following commented code removes all NaN values because scitkit-learn RandomForestClassifier cannot handle missing
# Critic Score values
# dfb = dfb.dropna().reset_index(drop=True)
# so we will use an imputer to predict and fill in missing Critic Scores
missing_mask = dfb.isna()
print(missing_mask)

# converting columns with strings to category dtype
'''
dfb['Name'] = dfb['Name'].astype('category')
dfb['Platform'] = dfb['Platform'].astype('category')
dfb['Genre'] = dfb['Genre'].astype('category')
dfb['Publisher'] = dfb['Publisher'].astype('category')
print(dfb.dtypes)

cat_columns = dfb.select_dtypes(['category']).columns
print(cat_columns)
dfb[cat_columns] = dfb[cat_columns].apply(lambda x: x.cat.codes)
print(dfb)
'''
le = LabelEncoder()

for var in dfb[['Name', 'Platform', 'Genre', 'Publisher']]:
    dfb[var] = le.fit_transform(dfb[var])

print(dfb)

for var in dfb[['Name', 'Platform', 'Genre', 'Publisher']]:
    dfb[var] = le.inverse_transform(dfb[var])

imputer = IterativeImputer(max_iter=10, random_state=100)
imputed_values = imputer.fit_transform(dfb)



dfb[missing_mask] = imputed_values[missing_mask]



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


'''************* Prediction Modeling **************'''
df3_copy = pd.get_dummies(df3)  # getting dummy variables from categorical data
df4 = df3_copy
y = df4['Hit'].values
df4 = df4.drop(['Hit'], axis=1)
X = df4.values

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.50, random_state=2)

# Testing prediction accuracy with random forest classifier
radm = RandomForestClassifier(random_state=2).fit(Xtrain, ytrain)
y_val_1 = radm.predict_proba(Xtest)
print("Validation accuracy: ", sum(pd.DataFrame(y_val_1).idxmax(axis=1).values == ytest)/len(ytest))

# Testing prediction accuracy with linear regression

