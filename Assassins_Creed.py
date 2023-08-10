import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

###################################
# Dataframes for each Excel sheet #
###################################

# importing Excel data
gameRankings = pd.read_excel('AC_stats.xlsx','GameRankings')
metacritic = pd.read_excel('AC_stats.xlsx','Metacritic')
acInfo = pd.read_excel('AC_stats.xlsx','Jogos por ano e plataforma')

############################
# GameRanking correlations #
############################

gameRankings.corr(numeric_only=True)
sns.heatmap(gameRankings.corr(numeric_only=True), annot = True)
plt.rcParams['figure.figsize'] = (25,7)
plt.gcf().subplots_adjust(left=0.145)
plt.gcf().subplots_adjust(bottom=0.183)
plt.show()

##########################
# GameRankings bar chart #
##########################

plt.figure(figsize=(8,5))
plt.barh(gameRankings['Jogo'], gameRankings['Avg_Score'], color='orange')
plt.xlabel('Review Score')
plt.title("All GameRanking Scores of Assassin's Creed Games")
plt.grid(True)
plt.gcf().subplots_adjust(left=0.383)
plt.show()

########################
# Metacritic bar chart #
########################

plt.figure(figsize=(8,5))
plt.barh(metacritic['Jogo'], metacritic['Avg_Score'], color='orange')
plt.xlabel('Review Score')
plt.title("All Metacritic Scores of Assassin's Creed Games")
plt.grid(True)
plt.gcf().subplots_adjust(left=0.385)
plt.show()

####################################################
# Grouped bar graph of GameRankings and Metacritic #
####################################################

# merging GameRankings and Metacritic dataframes together
df = pd.concat([gameRankings, metacritic], axis=1, join='inner')

# finding duplicate column names and adding a .# to the end of them
cols = pd.Series(df.columns)

for dup in cols[cols.duplicated()].unique():
	cols[cols[cols == dup].index.values.tolist()] = [dup + '.' 
	+ str(i) if i != 0 else dup for i in range(sum(cols == dup))]
df.columns = cols

# Renamed 'Avg_Score' and 'Avg_Score.1' to represent GamingRankings & Metacritic
df.rename(columns={'Avg_Score': 'GameRankings', 'Avg_Score.1': 'Metacritic'}, inplace=True)

# dropping unneeded columns
df.drop(df.iloc[:, 1:10], inplace=True, axis=1)
df.drop(df.iloc[:, 2:14], inplace=True, axis=1)

# setting index to 'Jogo'
df.set_index('Jogo', inplace=True)

print(df)

# plotting grouped bar graph
df.plot(kind='barh', figsize=(8,6))
plt.xlabel("Review Score")
plt.ylabel("")
plt.title('Average Review Scores')
plt.legend(loc='upper right')
plt.grid(True)
plt.gcf().subplots_adjust(left=0.337)
plt.show()

###################################################
# Correlation between GameRankings and Metacritic #
###################################################

gameRankings['Avg_Score'].corr(metacritic['Avg_Score'])
sns.heatmap(gameRankings.corr(numeric_only=True), annot = True)
plt.rcParams['figure.figsize'] = (10,6)
plt.show()

######################################################
# Combining all previous graphs into one single page #
######################################################

