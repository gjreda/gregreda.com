Title: Feature Engineering with Time Gaps
Date: 2020-02-16
Slug: feature-engineering-with-time-gaps
Tags: machine learning, data science, pandas, code snippets
Summary:

<!-- 
Alternative titles?:
- Creating time windowed user features in pandas
- Feature Engineering with time gaps
- Feature engineering with irregular intervals
-->

I tend to forget how to write certain blocks of code when I haven't written them in a while. Here's a common machine learning preprocessing task that falls into that category.

Imagine you have some event logs that capture an entity ID (user, store, ad, etc), timestamp, an event name, and maybe some other details. The data looks something like this:

```
userid	timestamp	event
789	2019-07-18 01:06:00	login
123	2019-07-19 08:30:00	login
789	2019-07-20 02:39:00	login
789	2019-07-20 08:15:00	login
456	2019-07-20 10:05:00	login
123	2019-07-20 14:40:00	login
123	2019-07-20 18:05:00	login
456	2019-07-21 21:11:00	login
789	2019-07-22 10:05:00	login
123	2019-07-23 09:18:00	login
789	2019-07-23 17:35:00	login
123	2019-07-25 16:49:00	login
789	2019-07-26 12:13:00	login
123	2019-07-27 19:56:00	login
```

For the sake of simplicity, let's say we want to build a model predicting whether or not a user will login in tomorrow. Our target is `y = bool(logins)`.

Three features we think will be informative are the user's previous logins, whether they logged in yesterday, and the number of days since their last login. We'll call these features `lifetime_logins`, `logins_yesterday`, and `days_since_last_login`.

Using [pandas](https://pandas.pydata.org/), we aggregate by user and date to get each user's daily count of logins.

```python
df = pd.read_clipboard(parse_dates=['timestamp'])
user_logins = (df.set_index('timestamp')
               .groupby(['userid', pd.Grouper(freq='D')])
               .size()
               .rename('logins'))
# userid  timestamp
# 123     2019-07-19    1
#         2019-07-20    2
#         2019-07-23    1
#         2019-07-25    1
#         2019-07-27    1
# 456     2019-07-20    1
#         2019-07-21    1
# 789     2019-07-18    1
#         2019-07-20    2
#         2019-07-22    1
#         2019-07-23    1
#         2019-07-26    1
# Name: logins, dtype: int64
```

But we're missing critical information. This is when the brain fart happens.

Recall the structure of our logs. Notice they omit records for when the user had no activity. In order to create our features, we need to fill in time gaps for each user and then roll that information forward.

This goal of this post is to help me remember how to do this in the future.

### Filling Time Gaps

First, we need to put each user on a continuous time scale.

```python
# create a continuous DatetimeIndex at a daily level
dates = pd.date_range(df.timestamp.min().date(),
                      df.timestamp.max().date(),
                      freq='1D')

# get unique set of user ids
users = df['userid'].unique()

# create a MultiIndex that is the product (cross-join) of
# users and DatetimeIndexes
idx = pd.MultiIndex.from_product([users, dates], names=['userid', 'timestamp'])

# and reindex our `user_logins` counts by it
user_logins = user_logins.reindex(idx)

# userid  timestamp
# 789     2019-07-18    1.0
#         2019-07-19    NaN
#         2019-07-20    2.0
#         2019-07-21    NaN
#         2019-07-22    1.0
#         2019-07-23    1.0
#         2019-07-24    NaN
#         2019-07-25    NaN
#         2019-07-26    1.0
#         2019-07-27    NaN
```

This gives us a continuous daily time series for each user. You can see what this looks like for user 789 above.

An important thing to note is that `idx` will need to be on the same time scale as the current `DatetimeIndex` in `user_logins`. Because we aggregated at a daily level using `pd.Grouper(freq='D')`, the `MultiIndex` we are using to `reindex` should also be at a daily level.

### Creating Features

Now we're free to create our features. We can zero-fill days each user did not log in. We also need to convert our `user_logins` to a DataFrame, which allows us to create the new feature columns (e.g. `logins_yesterday`).

```python
user_logins = user_logins.fillna(0).to_frame()
user_logins['logins_yesterday'] = user_logins.groupby(level='userid')['logins'].shift(1)
#                    logins  logins_yesterday
# userid timestamp
# 789    2019-07-18     1.0               NaN
#        2019-07-19     0.0               1.0
#        2019-07-20     2.0               0.0
#        2019-07-21     0.0               2.0
#        2019-07-22     1.0               0.0
# 123    2019-07-18     0.0               NaN
#        2019-07-19     1.0               0.0
#        2019-07-20     2.0               1.0
#        2019-07-21     0.0               2.0
#        2019-07-22     0.0               0.0
# 456    2019-07-18     0.0               NaN
#        2019-07-19     0.0               0.0
#        2019-07-20     1.0               0.0
#        2019-07-21     1.0               1.0
#        2019-07-22     0.0               1.0
```

The `lifetime_logins` and `login_streak` features need to be context dependant to avoid data leakage when training our model. Our features need to represent what would have been the correct values _at the time_. We can do this by rolling information forward with `shift`.

```python
user_logins['lifetime_logins'] = (user_logins
                                  .groupby(level='userid')
                                  .logins.cumsum()
                                  .groupby(level='userid').shift(1))
user_logins['days_since_last_login'] = (user_logins
                                        .groupby(level='userid')
                                        .cumsum()
                                        .groupby(['userid', 'logins'])
                                        .cumcount()
                                        .groupby(level='userid').shift(1)
                                        .rename('days_since_last_login'))

#                    logins  logins_yesterday  lifetime_logins  days_since_last_login
# userid timestamp
# 789    2019-07-18     1.0               NaN              NaN                    NaN
#        2019-07-19     0.0               1.0              1.0                    0.0
#        2019-07-20     2.0               0.0              1.0                    1.0
#        2019-07-21     0.0               2.0              3.0                    0.0
#        2019-07-22     1.0               0.0              3.0                    1.0
# 123    2019-07-18     0.0               NaN              NaN                    NaN
#        2019-07-19     1.0               0.0              0.0                    0.0
#        2019-07-20     2.0               1.0              1.0                    0.0
#        2019-07-21     0.0               2.0              3.0                    0.0
#        2019-07-22     0.0               0.0              3.0                    1.0
# 456    2019-07-18     0.0               NaN              NaN                    NaN
#        2019-07-19     0.0               0.0              0.0                    0.0
#        2019-07-20     1.0               0.0              0.0                    1.0
#        2019-07-21     1.0               1.0              1.0                    0.0
#        2019-07-22     0.0               1.0              2.0                    0.0
```

This can also be extended to create rolling features: something like `logins_last_n_days` where `n = [7, 14, 21]`.

```python
for n in [7, 14, 21]: 
    col = 'logins_last_{}_days'.format(n)
    user_logins[col] = (user_logins
                        .groupby(level='userid')
                        .logins
                        .apply(lambda d: d.rolling(n).sum().shift(1)))
```

Hopefully you've found this post helpful. I know my future self will.