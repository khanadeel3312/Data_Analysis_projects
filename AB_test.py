# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/134iNEoYOGZOD1m7n3JKsgQnE02PtUxu6

#Part I - Probability
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
# %matplotlib inline
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)

df= pd.read_csv("ab_data.csv")
df.head(10)

df.shape

df.duplicated().sum()

df.info()

df["group"].value_counts().to_frame()

df["converted"].value_counts(normalize= True).to_frame()*100

df.loc[df["landing_page"]=='new_page']

df.loc[df["landing_page"]=='new_page']

df_landing_page = df.groupby(["landing_page","group"],as_index= False).size()
df_landing_page

df_new_page_and_control = df.loc[(df["landing_page"]== "new_page") &(df["group"]!="treatment")]
len(df_new_page_and_control)

df_new_page_and_treatment = df.loc[(df["landing_page"]== "new_page") &(df["group"]=="treatment")]
len(df_new_page_and_treatment)

df_old_page_and_treatment = df.loc[(df["landing_page"]== "old_page") &(df["group"]!="control")]
len(df_old_page_and_treatment)

df_old_page_and_control = df.loc[(df["landing_page"]== "old_page") &(df["group"]=="control")]
len(df_old_page_and_control)

df2= pd.concat([df_old_page_and_control , df_new_page_and_treatment] , axis=0)
df2

df2.isnull().sum()

df2[((df2['group'] == 'treatment') == (df2['landing_page'] == 'new_page')) == False].shape[0]

df2["user_id"].unique()

df2["user_id"].duplicated().sum()

df2[df2.duplicated(['user_id'], keep=False)]

df2.drop_duplicates(subset ="user_id", inplace = True)
df2["user_id"].duplicated().sum()

df2["converted"].value_counts(normalize=True).to_frame()*100

"""the probalility of an individual converting regardless of the page they receive is 11.9597"""

control_and_converted = df2.loc[(df2["group"]== "control") &(df2["converted"]==1)]
len(control_and_converted)

treatment_and_converted = df2.loc[(df2["group"]== "treatment") &(df2["converted"]==1)]
len(treatment_and_converted)

probility_control_and_converted = (len(control_and_converted) / len(df2))*100
probility_control_and_converted

probility_treatment_and_converted =(len(treatment_and_converted)/len(df2))*100
probility_treatment_and_converted

probility_control= df2["group"].value_counts(normalize=True)*100
probility_control

"""probility of old_page is 49,99 and probility of new_page is 50.00

. Given that an individual was in the control group, what is the probability they converted
"""

(probility_control_and_converted / 49.993806)*100

"""Given that an individual was in the treatment group, what is the probability they converted"""

(probility_treatment_and_converted / 50.006194)*100

""" the probability that an individual received the new page"""

(df2["landing_page"]=="new_page").value_counts(normalize=True)*100

"""need more information because 12.04% that received the old_page were converted. 11.88% that received the new_page were converted. In conclusion, the new_page did not increase the conversion rate.

#Part II - A/B Test

Calculating conversion rates for old and new pages
"""

p_new =df2["converted"].mean()
p_new

"""the number of new individuals in the treatment group"""

n_new = len(df2[df2["group"]== "treatment"])
n_new

"""he number of old individuals in the control group"""

n_old = len(df2[df2["group"]== "control"])
n_old

"""This code generates a random binomial distribution representing the conversion rate for the new page in an A/B test"""

new_page_converted =np.random.binomial(1,p_new,n_new)
new_page_converted.mean()

"""This code generates a random binomial distribution representing the conversion rate for the old page in an A/B test"""

old_page_converted = np.random.binomial(1,p_old,n_old)
old_page_converted.mean()

""" p_new -p_old for the simulated values"""

new_page_converted.mean() - old_page_converted.mean()

"""This code snippet is performing a simulation to calculate the difference in conversion rates between the new page and the old page for 10,000 iterations."""

p_diff = []
for i in range (10000):
    new_page_converted =np.random.binomial(1,p_new,n_new)
    old_page_converted = np.random.binomial(1,p_new,n_old)
    p_diff.append(new_page_converted.mean() - old_page_converted.mean())

p_diff= np.array(p_diff)
plt.hist(p_diff)

"""This code calculates the difference in mean conversion rates between the treatment group and the control group in DataFrame"""

df2_converted_treatmeant = df2.converted.loc[( df2["group"] == "treatment")]

df2_converted_control = df2.converted.loc[( df2["group"] == "control")]

diff_mean= df2_converted_treatmeant.mean()- df2_converted_control.mean()

plt.hist(p_diff)
plt.axvline(diff_mean, color='r', label="observed difference")

"""This code calculates the proportion of simulated differences in conversion rates (stored in the list p_diff) that are greater than the observed difference in conversion rates (diff_mean)."""

(p_diff >  diff_mean).mean()

"""This code calculates the number of rows in DataFrame df2 where both conditions are met: the "converted" column has a value of 1 (indicating a conversion), and the "landing_page" column has a value of "old_page"
"""

len(df2.loc[(df2["converted"] == 1) & (df2["landing_page"] == "old_page")])

import statsmodels.api as sm

convert_old = len(df2.loc[(df2["converted"]== 1) & ( df2["landing_page"]=="old_page")])
convert_new = len(df2.loc[(df2["converted"]== 1) & ( df2["landing_page"]=="new_page")])
n_old =len(df2.loc[df2["landing_page"]=="old_page"])
n_new = len(df2.loc[df2["landing_page"]=="new_page"])

"""This code snippet utilizes the proportions_ztest function from the statsmodels library to conduct a z-test for the difference in proportions between two groups (in this case, the old page and the new page)"""

z_score, p_value = sm.stats.proportions_ztest([convert_old, convert_new], [n_old, n_new],value=None, alternative='smaller')

z_score

p_value

"""we fail to reject the null hypothesis, and we cannot conclude that the new page's conversion rate is significantly different from the old page's conversion rate."""

