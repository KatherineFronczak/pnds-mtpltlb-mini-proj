import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
from textwrap import wrap
import scipy.stats as stats

#cleaning county based presidential election data, merging number of votes based on candidate's political party
df_e = pd.read_csv('election.csv')
df_e['Rep Votes']=df_e[['Vote Data.Ben Carson.Number of Votes','Vote Data.Carly Fiorina.Number of Votes','Vote Data.Donald Trump.Number of Votes','Vote Data.Chris Christie.Number of Votes','Vote Data.Jeb Bush.Number of Votes','Vote Data.John Kasich.Number of Votes','Vote Data.Marco Rubio.Number of Votes','Vote Data.Mike Huckabee.Number of Votes','Vote Data.Rand Paul.Number of Votes','Vote Data.Rick Santorum.Number of Votes','Vote Data.Ted Cruz.Number of Votes']].sum(axis=1)
df_e['Dem Votes']=df_e[['Vote Data.Bernie Sanders.Number of Votes','Vote Data.Hillary Clinton.Number of Votes','Vote Data.Martin O\'Malley.Number of Votes']].sum(axis=1)
df_e = df_e[['Location.County','Location.State Abbreviation','Rep Votes','Dem Votes']]
df_e = df_e.where(df_e['Location.State Abbreviation']=='PA').dropna()
df_e = df_e.drop(['Location.State Abbreviation'],axis=1)
df_e['Location.County'] = df_e['Location.County'].str.strip()
df_e = df_e.set_index('Location.County')
df_e.index.rename('County', inplace=True)
df_e['Pct Dem votes'] = (df_e['Dem Votes']/(df_e['Dem Votes']+df_e['Rep Votes']))*100
df_e['Pct Rep votes'] = (df_e['Rep Votes']/(df_e['Dem Votes']+df_e['Rep Votes']))*100

#cleaning county demographic information
df_c = pd.read_csv('county_demographics.csv')
df_c = df_c.where(df_c['State']=='PA').dropna()
df_c['County'] = df_c['County'].replace('County$','',regex=True)
df_c['County'] = df_c['County'].str.strip()
df_c = df_c[['Education.Bachelor\'s Degree or Higher','County']]
df_c = df_c.set_index('County')

#merging the two dataframes based on county
df = pd.merge(df_c, df_e, how='left',left_index=True, right_index=True)
corrR, pvalR=stats.pearsonr(df['Education.Bachelor\'s Degree or Higher'],df['Pct Rep votes'])
corrD, pvalD=stats.pearsonr(df['Education.Bachelor\'s Degree or Higher'],df['Pct Dem votes'])
bR, mR = polyfit(df['Education.Bachelor\'s Degree or Higher'],df['Pct Rep votes'], 1)
bD, mD = polyfit(df['Education.Bachelor\'s Degree or Higher'],df['Pct Dem votes'], 1)

#making scatter plot figure with majority education level vs mahority political party voted for in county
fig = plt.figure()
plt.scatter(df['Education.Bachelor\'s Degree or Higher'], df['Pct Dem votes'], c=df['Education.Bachelor\'s Degree or Higher'],cmap='Blues', label='Democrat Votes')
plt.plot(df['Education.Bachelor\'s Degree or Higher'], bD + mD *df['Education.Bachelor\'s Degree or Higher'], '-',linewidth=1, color='blue', label='Dem Trendline')
plt.scatter(df['Education.Bachelor\'s Degree or Higher'], df['Pct Rep votes'], c=df['Education.Bachelor\'s Degree or Higher'],cmap='Reds', label='Republican Votes')
plt.plot(df['Education.Bachelor\'s Degree or Higher'], bR + mR *df['Education.Bachelor\'s Degree or Higher'], '-', linewidth=1, color='red', label='Rep Trendline')
plt.ylim([0, 100])
plt.yticks(np.arange(0, 100, 10))
plt.xlabel('Percent of population with Bachelor\'s degree of higher')
plt.ylabel('Percent of votes based on political party')

plt.title("\n".join(wrap("Trends between Higher Education and Political Party Voted for in the 2016 Presidential Election by County in Pennsylvania", 50)))
fig.tight_layout()
leg = plt.legend()
leg.legendHandles[2].set_color('blue')
leg.legendHandles[3].set_color('red')


plt.show()
