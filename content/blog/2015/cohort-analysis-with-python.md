Title: Cohort Analysis with Python
Date: 2015-08-23
Slug: cohort-analysis-with-python
Tags: python, pandas, tutorial, cohort analysis, startup metrics
Description: An intro to cohort analysis, and how to build them with Python and pandas.

Despite having done it countless times, I regularly forget how to build a [cohort analysis](https://en.wikipedia.org/wiki/Cohort_analysis) with Python and [pandas](http://pandas.pydata.org/). I’ve decided it’s a good idea to finally write it out - step by step - so I can refer back to this post later on. Hopefully others find it useful as well.

I’ll start by walking through what cohort analysis is and why it’s commonly used in startups and other growth businesses. Then, we’ll create one from a standard purchase dataset.

## What is cohort analysis?
A cohort is a group of users who share something in common, be it their sign-up date, first purchase month, birth date, acquisition channel, etc. Cohort analysis is the method by which these groups are tracked over time, helping you spot trends, understand repeat behaviors (purchases, engagement, amount spent, etc.), and monitor your customer and revenue retention.

It’s common for cohorts to be created based on a customer’s first usage of the platform, where "usage" is dependent on your business’ key metrics. For Uber or Lyft, usage would be booking a trip through one of their apps. For GrubHub, it’s ordering some food. For AirBnB, it’s booking a stay.

With these companies, a purchase is at their core, be it taking a trip or ordering dinner — their revenues are tied to their users’ purchase behavior.

In others, a purchase is not central to the business model and the business is more interested in "engagement" with the platform. Facebook and Twitter are examples of this - are you visiting their sites every day? Are you performing some action on them - maybe a "like" on Facebook or a "favorite" on a tweet?<sup>1</sup>

When building a cohort analysis, it’s important to consider the relationship between the event or interaction you’re tracking and its relationship to your business model.

## Why is it valuable?
Cohort analysis can be helpful when it comes to understanding your business’ health and "stickiness" - the loyalty of your customers. Stickiness is critical since [it’s far cheaper and easier to keep a current customer than to acquire a new one](https://hbr.org/2014/10/the-value-of-keeping-the-right-customers/). For startups, it’s also a key indicator of [product-market fit](https://en.wikipedia.org/wiki/Product/market_fit).

Additionally, your product evolves over time. New features are added and removed, the design changes, etc. Observing individual groups over time is a starting point to understanding how these changes affect user behavior.

It’s also a good way to visualize your user retention/churn as well as formulating a basic understanding of their lifetime value.

## An example
Imagine we have a dataset like the one below (you can find it [here](http://dmanalytics.org/wp-content/uploads/2014/10/chapter-12-relay-foods.xlsx)):

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OrderId</th>
      <th>OrderDate</th>
      <th>UserId</th>
      <th>TotalCharges</th>
      <th>CommonId</th>
      <th>PupId</th>
      <th>PickupDate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>262</td>
      <td>2009-01-11</td>
      <td>47</td>
      <td>50.67</td>
      <td>TRQKD</td>
      <td>2</td>
      <td>2009-01-12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>278</td>
      <td>2009-01-20</td>
      <td>47</td>
      <td>26.60</td>
      <td>4HH2S</td>
      <td>3</td>
      <td>2009-01-20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>294</td>
      <td>2009-02-03</td>
      <td>47</td>
      <td>38.71</td>
      <td>3TRDC</td>
      <td>2</td>
      <td>2009-02-04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>301</td>
      <td>2009-02-06</td>
      <td>47</td>
      <td>53.38</td>
      <td>NGAZJ</td>
      <td>2</td>
      <td>2009-02-09</td>
    </tr>
    <tr>
      <th>4</th>
      <td>302</td>
      <td>2009-02-06</td>
      <td>47</td>
      <td>14.28</td>
      <td>FFYHD</td>
      <td>2</td>
      <td>2009-02-09</td>
    </tr>
  </tbody>
</table>

Pretty standard purchase data with IDs for the order and user, as well as the order date and purchase amount.

We want to go from the data above to something like this:

![example cohort chart](/images/cohort-example.png)

Here’s how we get there.

## Code

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2

%matplotlib inline

df = pd.read_excel('/Users/gjreda/Dropbox/datasets/relay-foods.xlsx')
df.head(3)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OrderId</th>
      <th>OrderDate</th>
      <th>UserId</th>
      <th>TotalCharges</th>
      <th>CommonId</th>
      <th>PupId</th>
      <th>PickupDate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>262</td>
      <td>2009-01-11</td>
      <td>47</td>
      <td>50.67</td>
      <td>TRQKD</td>
      <td>2</td>
      <td>2009-01-12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>278</td>
      <td>2009-01-20</td>
      <td>47</td>
      <td>26.60</td>
      <td>4HH2S</td>
      <td>3</td>
      <td>2009-01-20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>294</td>
      <td>2009-02-03</td>
      <td>47</td>
      <td>38.71</td>
      <td>3TRDC</td>
      <td>2</td>
      <td>2009-02-04</td>
    </tr>
  </tbody>
</table>

### 1. Create a period column based on the OrderDate

Since we're doing monthly cohorts, we'll be looking at the total monthly behavior of our users. Therefore, we don't want granular OrderDate data (right now).

```python
df['OrderPeriod'] = df.OrderDate.apply(lambda x: x.strftime('%Y-%m'))
df.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OrderId</th>
      <th>OrderDate</th>
      <th>UserId</th>
      <th>TotalCharges</th>
      <th>CommonId</th>
      <th>PupId</th>
      <th>PickupDate</th>
      <th>OrderPeriod</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>262</td>
      <td>2009-01-11</td>
      <td>47</td>
      <td>50.67</td>
      <td>TRQKD</td>
      <td>2</td>
      <td>2009-01-12</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>278</td>
      <td>2009-01-20</td>
      <td>47</td>
      <td>26.60</td>
      <td>4HH2S</td>
      <td>3</td>
      <td>2009-01-20</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>294</td>
      <td>2009-02-03</td>
      <td>47</td>
      <td>38.71</td>
      <td>3TRDC</td>
      <td>2</td>
      <td>2009-02-04</td>
      <td>2009-02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>301</td>
      <td>2009-02-06</td>
      <td>47</td>
      <td>53.38</td>
      <td>NGAZJ</td>
      <td>2</td>
      <td>2009-02-09</td>
      <td>2009-02</td>
    </tr>
    <tr>
      <th>4</th>
      <td>302</td>
      <td>2009-02-06</td>
      <td>47</td>
      <td>14.28</td>
      <td>FFYHD</td>
      <td>2</td>
      <td>2009-02-09</td>
      <td>2009-02</td>
    </tr>
  </tbody>
</table>

### 2. Determine the user's cohort group (based on their first order)

Create a new column called `CohortGroup`, which is the year and month in which the user's first purchase occurred.

```python
df.set_index('UserId', inplace=True)

df['CohortGroup'] = df.groupby(level=0)['OrderDate'].min().apply(lambda x: x.strftime('%Y-%m'))
df.reset_index(inplace=True)
df.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UserId</th>
      <th>OrderId</th>
      <th>OrderDate</th>
      <th>TotalCharges</th>
      <th>CommonId</th>
      <th>PupId</th>
      <th>PickupDate</th>
      <th>OrderPeriod</th>
      <th>CohortGroup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>47</td>
      <td>262</td>
      <td>2009-01-11</td>
      <td>50.67</td>
      <td>TRQKD</td>
      <td>2</td>
      <td>2009-01-12</td>
      <td>2009-01</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>47</td>
      <td>278</td>
      <td>2009-01-20</td>
      <td>26.60</td>
      <td>4HH2S</td>
      <td>3</td>
      <td>2009-01-20</td>
      <td>2009-01</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>47</td>
      <td>294</td>
      <td>2009-02-03</td>
      <td>38.71</td>
      <td>3TRDC</td>
      <td>2</td>
      <td>2009-02-04</td>
      <td>2009-02</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>47</td>
      <td>301</td>
      <td>2009-02-06</td>
      <td>53.38</td>
      <td>NGAZJ</td>
      <td>2</td>
      <td>2009-02-09</td>
      <td>2009-02</td>
      <td>2009-01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>47</td>
      <td>302</td>
      <td>2009-02-06</td>
      <td>14.28</td>
      <td>FFYHD</td>
      <td>2</td>
      <td>2009-02-09</td>
      <td>2009-02</td>
      <td>2009-01</td>
    </tr>
  </tbody>
</table>

### 3. Rollup data by CohortGroup & OrderPeriod

Since we're looking at monthly cohorts, we need to aggregate users, orders, and amount spent by the CohortGroup within the month (OrderPeriod).

```python
grouped = df.groupby(['CohortGroup', 'OrderPeriod'])

# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'UserId': pd.Series.nunique,
                       'OrderId': pd.Series.nunique,
                       'TotalCharges': np.sum})

# make the column names more meaningful
cohorts.rename(columns={'UserId': 'TotalUsers',
                        'OrderId': 'TotalOrders'}, inplace=True)
cohorts.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>TotalOrders</th>
      <th>TotalUsers</th>
      <th>TotalCharges</th>
    </tr>
    <tr>
      <th>CohortGroup</th>
      <th>OrderPeriod</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">2009-01</th>
      <th>2009-01</th>
      <td>30</td>
      <td>22</td>
      <td>1850.255</td>
    </tr>
    <tr>
      <th>2009-02</th>
      <td>25</td>
      <td>8</td>
      <td>1351.065</td>
    </tr>
    <tr>
      <th>2009-03</th>
      <td>26</td>
      <td>10</td>
      <td>1357.360</td>
    </tr>
    <tr>
      <th>2009-04</th>
      <td>28</td>
      <td>9</td>
      <td>1604.500</td>
    </tr>
    <tr>
      <th>2009-05</th>
      <td>26</td>
      <td>10</td>
      <td>1575.625</td>
    </tr>
  </tbody>
</table>

### 4. Label the CohortPeriod for each CohortGroup

We want to look at how each cohort has behaved in the months following their first purchase, so we'll need to index each cohort to their first purchase month. For example, CohortPeriod = 1 will be the cohort's first month, CohortPeriod = 2 is their second, and so on.

This allows us to compare cohorts across various stages of their lifetime.

```python
def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    
    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>TotalOrders</th>
      <th>TotalUsers</th>
      <th>TotalCharges</th>
      <th>CohortPeriod</th>
    </tr>
    <tr>
      <th>CohortGroup</th>
      <th>OrderPeriod</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">2009-01</th>
      <th>2009-01</th>
      <td>30</td>
      <td>22</td>
      <td>1850.255</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2009-02</th>
      <td>25</td>
      <td>8</td>
      <td>1351.065</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2009-03</th>
      <td>26</td>
      <td>10</td>
      <td>1357.360</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2009-04</th>
      <td>28</td>
      <td>9</td>
      <td>1604.500</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2009-05</th>
      <td>26</td>
      <td>10</td>
      <td>1575.625</td>
      <td>5</td>
    </tr>
  </tbody>
</table>

### 5. Make sure we did all that right

Let's test data points from the original DataFrame with their corresponding values in the new cohorts DataFrame to make sure all our data transformations worked as expected. As long as none of these raise an exception, we're good.

```python
x = df[(df.CohortGroup == '2009-01') & (df.OrderPeriod == '2009-01')]
y = cohorts.ix[('2009-01', '2009-01')]

assert(x['UserId'].nunique() == y['TotalUsers'])
assert(x['TotalCharges'].sum().round(2) == y['TotalCharges'].round(2))
assert(x['OrderId'].nunique() == y['TotalOrders'])

x = df[(df.CohortGroup == '2009-01') & (df.OrderPeriod == '2009-09')]
y = cohorts.ix[('2009-01', '2009-09')]

assert(x['UserId'].nunique() == y['TotalUsers'])
assert(x['TotalCharges'].sum().round(2) == y['TotalCharges'].round(2))
assert(x['OrderId'].nunique() == y['TotalOrders'])

x = df[(df.CohortGroup == '2009-05') & (df.OrderPeriod == '2009-09')]
y = cohorts.ix[('2009-05', '2009-09')]

assert(x['UserId'].nunique() == y['TotalUsers'])
assert(x['TotalCharges'].sum().round(2) == y['TotalCharges'].round(2))
assert(x['OrderId'].nunique() == y['TotalOrders'])
```

### User Retention by Cohort Group

We want to look at the percentage change of each CohortGroup over time -- not the absolute change.

To do this, we'll first need to create a pandas Series containing each CohortGroup and its size.

```python
# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
cohort_group_size.head()
```
```output
CohortGroup
2009-01    22
2009-02    15
2009-03    13
2009-04    39
2009-05    50
Name: TotalUsers, dtype: int64
```

Now, we'll need to divide the `TotalUsers` values in `cohorts` by `cohort_group_size`. Since DataFrame operations are performed based on the indices of the objects, we'll use `unstack` on our cohorts DataFrame to create a matrix where each column represents a CohortGroup and each row is the CohortPeriod corresponding to that group.

To illustrate what `unstack` does, recall the first five `TotalUsers` values:

```python
cohorts['TotalUsers'].head()
```
```output
CohortGroup  CohortPeriod
2009-01      1               22
             2                8
             3               10
             4                9
             5               10
Name: TotalUsers, dtype: int64
```

```python
cohorts['TotalUsers'].unstack(0).head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>CohortGroup</th>
      <th>2009-01</th>
      <th>2009-02</th>
      <th>2009-03</th>
      <th>2009-04</th>
      <th>2009-05</th>
      <th>2009-06</th>
      <th>2009-07</th>
      <th>2009-08</th>
      <th>2009-09</th>
      <th>2009-10</th>
      <th>2009-11</th>
      <th>2009-12</th>
      <th>2010-01</th>
      <th>2010-02</th>
      <th>2010-03</th>
    </tr>
    <tr>
      <th>CohortPeriod</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>22</td>
      <td>15</td>
      <td>13</td>
      <td>39</td>
      <td>50</td>
      <td>32</td>
      <td>50</td>
      <td>31</td>
      <td>37</td>
      <td>54</td>
      <td>130</td>
      <td>65</td>
      <td>95</td>
      <td>100</td>
      <td>24</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>3</td>
      <td>4</td>
      <td>13</td>
      <td>13</td>
      <td>15</td>
      <td>23</td>
      <td>11</td>
      <td>15</td>
      <td>17</td>
      <td>32</td>
      <td>17</td>
      <td>50</td>
      <td>19</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10</td>
      <td>5</td>
      <td>5</td>
      <td>10</td>
      <td>12</td>
      <td>9</td>
      <td>13</td>
      <td>9</td>
      <td>14</td>
      <td>12</td>
      <td>26</td>
      <td>18</td>
      <td>26</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9</td>
      <td>1</td>
      <td>4</td>
      <td>13</td>
      <td>5</td>
      <td>6</td>
      <td>10</td>
      <td>7</td>
      <td>8</td>
      <td>13</td>
      <td>29</td>
      <td>7</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>10</td>
      <td>4</td>
      <td>1</td>
      <td>6</td>
      <td>4</td>
      <td>7</td>
      <td>11</td>
      <td>6</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

Now, we can utilize broadcasting to divide each column by the corresponding `cohort_group_size`.

The resulting DataFrame, `user_retention`, contains the percentage of users from the cohort purchasing within the given period. For instance, 38.4% of users in the 2009-03 purchased again in month 3 (which would be May 2009).

```python
user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>CohortGroup</th>
      <th>2009-01</th>
      <th>2009-02</th>
      <th>2009-03</th>
      <th>2009-04</th>
      <th>2009-05</th>
      <th>2009-06</th>
      <th>2009-07</th>
      <th>2009-08</th>
      <th>2009-09</th>
      <th>2009-10</th>
      <th>2009-11</th>
      <th>2009-12</th>
      <th>2010-01</th>
      <th>2010-02</th>
      <th>2010-03</th>
    </tr>
    <tr>
      <th>CohortPeriod</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.00</td>
      <td>1.00000</td>
      <td>1.00</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.00</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.363636</td>
      <td>0.200000</td>
      <td>0.307692</td>
      <td>0.333333</td>
      <td>0.26</td>
      <td>0.46875</td>
      <td>0.46</td>
      <td>0.354839</td>
      <td>0.405405</td>
      <td>0.314815</td>
      <td>0.246154</td>
      <td>0.261538</td>
      <td>0.526316</td>
      <td>0.19</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.454545</td>
      <td>0.333333</td>
      <td>0.384615</td>
      <td>0.256410</td>
      <td>0.24</td>
      <td>0.28125</td>
      <td>0.26</td>
      <td>0.290323</td>
      <td>0.378378</td>
      <td>0.222222</td>
      <td>0.200000</td>
      <td>0.276923</td>
      <td>0.273684</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.409091</td>
      <td>0.066667</td>
      <td>0.307692</td>
      <td>0.333333</td>
      <td>0.10</td>
      <td>0.18750</td>
      <td>0.20</td>
      <td>0.225806</td>
      <td>0.216216</td>
      <td>0.240741</td>
      <td>0.223077</td>
      <td>0.107692</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.454545</td>
      <td>0.266667</td>
      <td>0.076923</td>
      <td>0.153846</td>
      <td>0.08</td>
      <td>0.21875</td>
      <td>0.22</td>
      <td>0.193548</td>
      <td>0.351351</td>
      <td>0.240741</td>
      <td>0.100000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.363636</td>
      <td>0.266667</td>
      <td>0.153846</td>
      <td>0.179487</td>
      <td>0.12</td>
      <td>0.15625</td>
      <td>0.20</td>
      <td>0.258065</td>
      <td>0.243243</td>
      <td>0.129630</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.363636</td>
      <td>0.266667</td>
      <td>0.153846</td>
      <td>0.102564</td>
      <td>0.06</td>
      <td>0.09375</td>
      <td>0.22</td>
      <td>0.129032</td>
      <td>0.216216</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.318182</td>
      <td>0.333333</td>
      <td>0.230769</td>
      <td>0.153846</td>
      <td>0.10</td>
      <td>0.09375</td>
      <td>0.14</td>
      <td>0.129032</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.318182</td>
      <td>0.333333</td>
      <td>0.153846</td>
      <td>0.051282</td>
      <td>0.10</td>
      <td>0.31250</td>
      <td>0.14</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.318182</td>
      <td>0.266667</td>
      <td>0.076923</td>
      <td>0.102564</td>
      <td>0.08</td>
      <td>0.09375</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

Finally, we can plot the cohorts over time in an effort to spot behavioral differences or similarities. Two common cohort charts are line graphs and heatmaps, both of which are shown below.

Notice that the first period of each cohort is 100% -- this is because our cohorts are based on each user's first purchase, meaning everyone in the cohort purchased in month 1.

```python
user_retention[['2009-06', '2009-07', '2009-08']].plot(figsize=(10,5))
plt.title('Cohorts: User Retention')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel('% of Cohort Purchasing');
```
![cohort retention curves](/images/cohort-example.png)

```python
# Creating heatmaps in matplotlib is more difficult than it should be.
# Thankfully, Seaborn makes them easy for us.
# http://stanford.edu/~mwaskom/software/seaborn/

import seaborn as sns
sns.set(style='white')

plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%');
```
![cohort retention heatmap](/images/cohort-retention-heatmap.png)

Unsurprisingly, we can see from the above chart that fewer users tend to purchase as time goes on.

However, we can also see that the 2009-01 cohort is the strongest, which enables us to ask targeted questions about this cohort compared to others -- what other attributes (besides first purchase month) do these users share which might be causing them to stick around? How were the majority of these users acquired? Was there a specific marketing campaign that brought them in? Did they take advantage of a promotion at sign-up? The answers to these questions would inform future marketing and product efforts.

## Further work
User retention is only one way of using cohorts to look at your business — we could have also looked at revenue retention. That is, the percentage of each cohort’s month 1 revenue returning in subsequent periods. User retention is important, but we shouldn’t lose sight of the revenue each cohort is bringing in (and how much of it is returning).

Hopefully you’ve found this post useful. If I’ve missed anything, [let me know](https://twitter.com/gjreda).

## Additional Resources
- [Cohort Analysis](https://en.wikipedia.org/wiki/Cohort_analysis)  on Wikipedia
- [Know Your User Cohorts](http://christophjanz.blogspot.de/2012/05/know-your-user-cohorts.html) by Christoph Janz
- [The Cohort Analysis](http://avc.com/2009/10/the-cohort-analysis/) by Fred Wilson (Union Square Ventures)
- [What exactly is cohort analysis?](http://www.quora.com/What-exactly-is-cohort-analysis) on Quora

<hr class="small" id="footnotes"></hr>
1. While a purchase might not be at the core of these businesses, they still might occur (e.g. "Buy" buttons on tweets are of value to Twitter, but users and engagement are what the platform is about).
