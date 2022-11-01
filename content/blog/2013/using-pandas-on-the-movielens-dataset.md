Title: Using pandas on the MovieLens dataset
Date: 2013-10-26 3:00
Slug: using-pandas-on-the-movielens-dataset
Tags: python, pandas, sql, tutorial, data science
Description: Part three of a three part introduction to the pandas library for Python. It is geared towards SQL users, but is useful for anyone wanting to get started with pandas.

_UPDATE: If you're interested in learning pandas from a SQL perspective and would prefer to watch a video, you can find video of my 2014 PyData NYC talk [here](http://reda.io/sql2pandas)._

_This is part three of a three part introduction to [pandas](http://pandas.pydata.org), a Python library for data analysis. The tutorial is primarily geared towards SQL users, but is useful for anyone wanting to get started with the library._

- [Part 1: Intro to pandas data structures](/2013/10/26/intro-to-pandas-data-structures/), covers the basics of the library's two main data structures - Series and DataFrames.
- [Part 2: Working with DataFrames](/2013/10/26/working-with-pandas-dataframes/), dives a bit deeper into the functionality of DataFrames. It shows how to inspect, select, filter, merge, combine, and group your data.
- [Part 3: Using pandas with the MovieLens dataset](/2013/10/26/using-pandas-on-the-movielens-dataset/), applies the learnings of the first two parts in order to answer a few basic analysis questions about the MovieLens ratings data.

## Using pandas on the MovieLens dataset

To show pandas in a more "applied" sense, let's use it to answer some questions about the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. Recall that we've already read our data into DataFrames and merged it.

```python
# pass in column names for each CSV
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols,
                    encoding='latin-1')

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols,
                      encoding='latin-1')

# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
movies = pd.read_csv('ml-100k/u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')

# create one merged DataFrame
movie_ratings = pd.merge(movies, ratings)
lens = pd.merge(movie_ratings, users)
```

### What are the 25 most rated movies?

```python
most_rated = lens.groupby('title').size().sort_values(ascending=False)[:25]
most_rated
```
```output
title
Star Wars (1977)                             583
Contact (1997)                               509
Fargo (1996)                                 508
Return of the Jedi (1983)                    507
Liar Liar (1997)                             485
English Patient, The (1996)                  481
Scream (1996)                                478
Toy Story (1995)                             452
Air Force One (1997)                         431
Independence Day (ID4) (1996)                429
Raiders of the Lost Ark (1981)               420
Godfather, The (1972)                        413
Pulp Fiction (1994)                          394
Twelve Monkeys (1995)                        392
Silence of the Lambs, The (1991)             390
Jerry Maguire (1996)                         384
Chasing Amy (1997)                           379
Rock, The (1996)                             378
Empire Strikes Back, The (1980)              367
Star Trek: First Contact (1996)              365
Back to the Future (1985)                    350
Titanic (1997)                               350
Mission: Impossible (1996)                   344
Fugitive, The (1993)                         336
Indiana Jones and the Last Crusade (1989)    331
dtype: int64
```

There's a lot going on in the code above, but it's very idomatic. We're splitting the DataFrame into groups by movie title and applying the `size` method to get the count of records in each group. Then we order our results in descending order and limit the output to the top 25 using Python's slicing syntax.

In SQL, this would be equivalent to:

```sql
SELECT title, count(1)
FROM lens
GROUP BY title
ORDER BY 2 DESC
LIMIT 25;
```

Alternatively, pandas has a nifty `value_counts` method - yes, this is simpler - the goal above was to show a basic `groupby` example.

```python
lens.title.value_counts()[:25]
```
```output
Star Wars (1977)                             583
Contact (1997)                               509
Fargo (1996)                                 508
Return of the Jedi (1983)                    507
Liar Liar (1997)                             485
English Patient, The (1996)                  481
Scream (1996)                                478
Toy Story (1995)                             452
Air Force One (1997)                         431
Independence Day (ID4) (1996)                429
Raiders of the Lost Ark (1981)               420
Godfather, The (1972)                        413
Pulp Fiction (1994)                          394
Twelve Monkeys (1995)                        392
Silence of the Lambs, The (1991)             390
Jerry Maguire (1996)                         384
Chasing Amy (1997)                           379
Rock, The (1996)                             378
Empire Strikes Back, The (1980)              367
Star Trek: First Contact (1996)              365
Titanic (1997)                               350
Back to the Future (1985)                    350
Mission: Impossible (1996)                   344
Fugitive, The (1993)                         336
Indiana Jones and the Last Crusade (1989)    331
Name: title, dtype: int64
```

### Which movies are most highly rated?

```python
movie_stats = lens.groupby('title').agg({'rating': [np.size, np.mean]})
movie_stats.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">rating</th>
    </tr>
    <tr>
      <th></th>
      <th>size</th>
      <th>mean</th>
    </tr>
    <tr>
      <th>title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>'Til There Was You (1997)</th>
      <td>9</td>
      <td>2.333333</td>
    </tr>
    <tr>
      <th>1-900 (1994)</th>
      <td>5</td>
      <td>2.600000</td>
    </tr>
    <tr>
      <th>101 Dalmatians (1996)</th>
      <td>109</td>
      <td>2.908257</td>
    </tr>
    <tr>
      <th>12 Angry Men (1957)</th>
      <td>125</td>
      <td>4.344000</td>
    </tr>
    <tr>
      <th>187 (1997)</th>
      <td>41</td>
      <td>3.024390</td>
    </tr>
  </tbody>
</table>

We can use the `agg` method to pass a dictionary specifying the columns to aggregate (as keys) and a list of functions we'd like to apply.

Let's sort the resulting DataFrame so that we can see which movies have the highest average score.

```python
# sort by rating average
movie_stats.sort_values([('rating', 'mean')], ascending=False).head()
```
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">rating</th>
    </tr>
    <tr>
      <th></th>
      <th>size</th>
      <th>mean</th>
    </tr>
    <tr>
      <th>title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>They Made Me a Criminal (1939)</th>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>Marlene Dietrich: Shadow and Light (1996)</th>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>Saint of Fort Washington, The (1993)</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>Someone Else's America (1995)</th>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>Star Kid (1997)</th>
      <td>3</td>
      <td>5</td>
    </tr>
  </tbody>
</table>

Because `movie_stats` is a DataFrame, we use the `sort` method - only Series objects use `order`. Additionally, because our columns are now a [MultiIndex](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced), we need to pass in a tuple specifying how to sort.

The above movies are rated so rarely that we can't count them as quality films. Let's only look at movies that have been rated at least 100 times.

```python
atleast_100 = movie_stats['rating']['size'] >= 100
movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:15]
```
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">rating</th>
    </tr>
    <tr>
      <th></th>
      <th>size</th>
      <th>mean</th>
    </tr>
    <tr>
      <th>title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Close Shave, A (1995)</th>
      <td>112</td>
      <td>4.491071</td>
    </tr>
    <tr>
      <th>Schindler's List (1993)</th>
      <td>298</td>
      <td>4.466443</td>
    </tr>
    <tr>
      <th>Wrong Trousers, The (1993)</th>
      <td>118</td>
      <td>4.466102</td>
    </tr>
    <tr>
      <th>Casablanca (1942)</th>
      <td>243</td>
      <td>4.456790</td>
    </tr>
    <tr>
      <th>Shawshank Redemption, The (1994)</th>
      <td>283</td>
      <td>4.445230</td>
    </tr>
    <tr>
      <th>Rear Window (1954)</th>
      <td>209</td>
      <td>4.387560</td>
    </tr>
    <tr>
      <th>Usual Suspects, The (1995)</th>
      <td>267</td>
      <td>4.385768</td>
    </tr>
    <tr>
      <th>Star Wars (1977)</th>
      <td>583</td>
      <td>4.358491</td>
    </tr>
    <tr>
      <th>12 Angry Men (1957)</th>
      <td>125</td>
      <td>4.344000</td>
    </tr>
    <tr>
      <th>Citizen Kane (1941)</th>
      <td>198</td>
      <td>4.292929</td>
    </tr>
    <tr>
      <th>To Kill a Mockingbird (1962)</th>
      <td>219</td>
      <td>4.292237</td>
    </tr>
    <tr>
      <th>One Flew Over the Cuckoo's Nest (1975)</th>
      <td>264</td>
      <td>4.291667</td>
    </tr>
    <tr>
      <th>Silence of the Lambs, The (1991)</th>
      <td>390</td>
      <td>4.289744</td>
    </tr>
    <tr>
      <th>North by Northwest (1959)</th>
      <td>179</td>
      <td>4.284916</td>
    </tr>
    <tr>
      <th>Godfather, The (1972)</th>
      <td>413</td>
      <td>4.283293</td>
    </tr>
  </tbody>
</table>

Those results look realistic. Notice that we used boolean indexing to filter our `movie_stats` frame.

We broke this question down into many parts, so here's the Python needed to get the 15 movies with the highest average rating, requiring that they had at least 100 ratings:

```python
movie_stats = lens.groupby('title').agg({'rating': [np.size, np.mean]})
atleast_100 = movie_stats['rating'].size >= 100
movie_stats[atleast_100].sort_values([('rating', 'mean')], ascending=False)[:15]
```

The SQL equivalent would be:

```sql
SELECT title, COUNT(1) size, AVG(rating) mean
FROM lens
GROUP BY title
HAVING COUNT(1) >= 100
ORDER BY 3 DESC
LIMIT 15;
```

### Limiting our population going forward

Going forward, let's only look at the 50 most rated movies. Let's make a Series of movies that meet this threshold so we can use it for filtering later.

```python
most_50 = lens.groupby('movie_id').size().sort_values(ascending=False)[:50]
```

The SQL to match this would be:

```sql
CREATE TABLE most_50 AS (
    SELECT movie_id, COUNT(1)
    FROM lens
    GROUP BY movie_id
    ORDER BY 2 DESC
    LIMIT 50
);
```

This table would then allow us to use EXISTS, IN, or JOIN whenever we wanted to filter our results. Here's an example using EXISTS:

```sql
SELECT *
FROM lens
WHERE EXISTS (SELECT 1 FROM most_50 WHERE lens.movie_id = most_50.movie_id);
```

### Which movies are most controversial amongst different ages?

Let's look at how these movies are viewed across different age groups. First, let's look at how age is distributed amongst our users.

```python
users.age.plot.hist(bins=30)
plt.title("Distribution of users' ages")
plt.ylabel('count of users')
plt.xlabel('age');
```

![Distribution of user ages](/images/pandas-movielens-age-histogram.png)

pandas' integration with [matplotlib](https://matplotlib.org/index.html) makes basic graphing of Series/DataFrames trivial. In this case, just call hist on the column to produce a histogram. We can also use [matplotlib.pyplot](https://matplotlib.org/stable/tutorials/introductory/pyplot.html) to customize our graph a bit (always label your axes).

### Binning our users

I don't think it'd be very useful to compare individual ages - let's bin our users into age groups using `pandas.cut`.

```python

labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
lens['age_group'] = pd.cut(lens.age, range(0, 81, 10), right=False, labels=labels)
lens[['age', 'age_group']].drop_duplicates()[:10]
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>age_group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>60</td>
      <td>60-69</td>
    </tr>
    <tr>
      <th>397</th>
      <td>21</td>
      <td>20-29</td>
    </tr>
    <tr>
      <th>459</th>
      <td>33</td>
      <td>30-39</td>
    </tr>
    <tr>
      <th>524</th>
      <td>30</td>
      <td>30-39</td>
    </tr>
    <tr>
      <th>782</th>
      <td>23</td>
      <td>20-29</td>
    </tr>
    <tr>
      <th>995</th>
      <td>29</td>
      <td>20-29</td>
    </tr>
    <tr>
      <th>1229</th>
      <td>26</td>
      <td>20-29</td>
    </tr>
    <tr>
      <th>1664</th>
      <td>31</td>
      <td>30-39</td>
    </tr>
    <tr>
      <th>1942</th>
      <td>24</td>
      <td>20-29</td>
    </tr>
    <tr>
      <th>2270</th>
      <td>32</td>
      <td>30-39</td>
    </tr>
  </tbody>
</table>

`pandas.cut` allows you to bin numeric data. In the above lines, we first created labels to name our bins, then split our users into eight bins of ten years (0-9, 10-19, 20-29, etc.). Our use of `right=False` told the function that we wanted the bins to be exclusive of the max age in the bin (e.g. a 30 year old user gets the 30s label).

Now we can now compare ratings across age groups.

```python
lens.groupby('age_group').agg({'rating': [np.size, np.mean]})
```
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">rating</th>
    </tr>
    <tr>
      <th></th>
      <th>size</th>
      <th>mean</th>
    </tr>
    <tr>
      <th>age_group</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0-9</th>
      <td>43</td>
      <td>3.767442</td>
    </tr>
    <tr>
      <th>10-19</th>
      <td>8181</td>
      <td>3.486126</td>
    </tr>
    <tr>
      <th>20-29</th>
      <td>39535</td>
      <td>3.467333</td>
    </tr>
    <tr>
      <th>30-39</th>
      <td>25696</td>
      <td>3.554444</td>
    </tr>
    <tr>
      <th>40-49</th>
      <td>15021</td>
      <td>3.591772</td>
    </tr>
    <tr>
      <th>50-59</th>
      <td>8704</td>
      <td>3.635800</td>
    </tr>
    <tr>
      <th>60-69</th>
      <td>2623</td>
      <td>3.648875</td>
    </tr>
    <tr>
      <th>70-79</th>
      <td>197</td>
      <td>3.649746</td>
    </tr>
  </tbody>
</table>

Young users seem a bit more critical than other age groups. Let's look at how the 50 most rated movies are viewed across each age group. We can use the `most_50` Series we created earlier for filtering.

```python
lens.set_index('movie_id', inplace=True)
by_age = lens.loc[most_50.index].groupby(['title', 'age_group'])
by_age.rating.mean().head(15)
```
```output
title                 age_group
Air Force One (1997)  10-19        3.647059
                      20-29        3.666667
                      30-39        3.570000
                      40-49        3.555556
                      50-59        3.750000
                      60-69        3.666667
                      70-79        3.666667
Alien (1979)          10-19        4.111111
                      20-29        4.026087
                      30-39        4.103448
                      40-49        3.833333
                      50-59        4.272727
                      60-69        3.500000
                      70-79        4.000000
Aliens (1986)         10-19        4.050000
Name: rating, dtype: float64
```

Notice that both the title and age group are indexes here, with the average rating value being a Series. This is going to produce a really long list of values.

Wouldn't it be nice to see the data as a table? Each title as a row, each age group as a column, and the average rating in each cell.

Behold! The magic of `unstack`!

```python
by_age.rating.mean().unstack(1).fillna(0)[10:20]
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>age_group</th>
      <th>0-9</th>
      <th>10-19</th>
      <th>20-29</th>
      <th>30-39</th>
      <th>40-49</th>
      <th>50-59</th>
      <th>60-69</th>
      <th>70-79</th>
    </tr>
    <tr>
      <th>title</th>
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
      <th>E.T. the Extra-Terrestrial (1982)</th>
      <td>0</td>
      <td>3.680000</td>
      <td>3.609091</td>
      <td>3.806818</td>
      <td>4.160000</td>
      <td>4.368421</td>
      <td>4.375000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>Empire Strikes Back, The (1980)</th>
      <td>4</td>
      <td>4.642857</td>
      <td>4.311688</td>
      <td>4.052083</td>
      <td>4.100000</td>
      <td>3.909091</td>
      <td>4.250000</td>
      <td>5.000000</td>
    </tr>
    <tr>
      <th>English Patient, The (1996)</th>
      <td>5</td>
      <td>3.739130</td>
      <td>3.571429</td>
      <td>3.621849</td>
      <td>3.634615</td>
      <td>3.774648</td>
      <td>3.904762</td>
      <td>4.500000</td>
    </tr>
    <tr>
      <th>Fargo (1996)</th>
      <td>0</td>
      <td>3.937500</td>
      <td>4.010471</td>
      <td>4.230769</td>
      <td>4.294118</td>
      <td>4.442308</td>
      <td>4.000000</td>
      <td>4.333333</td>
    </tr>
    <tr>
      <th>Forrest Gump (1994)</th>
      <td>5</td>
      <td>4.047619</td>
      <td>3.785714</td>
      <td>3.861702</td>
      <td>3.847826</td>
      <td>4.000000</td>
      <td>3.800000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>Fugitive, The (1993)</th>
      <td>0</td>
      <td>4.320000</td>
      <td>3.969925</td>
      <td>3.981481</td>
      <td>4.190476</td>
      <td>4.240000</td>
      <td>3.666667</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>Full Monty, The (1997)</th>
      <td>0</td>
      <td>3.421053</td>
      <td>4.056818</td>
      <td>3.933333</td>
      <td>3.714286</td>
      <td>4.146341</td>
      <td>4.166667</td>
      <td>3.500000</td>
    </tr>
    <tr>
      <th>Godfather, The (1972)</th>
      <td>0</td>
      <td>4.400000</td>
      <td>4.345070</td>
      <td>4.412844</td>
      <td>3.929412</td>
      <td>4.463415</td>
      <td>4.125000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>Groundhog Day (1993)</th>
      <td>0</td>
      <td>3.476190</td>
      <td>3.798246</td>
      <td>3.786667</td>
      <td>3.851064</td>
      <td>3.571429</td>
      <td>3.571429</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>Independence Day (ID4) (1996)</th>
      <td>0</td>
      <td>3.595238</td>
      <td>3.291429</td>
      <td>3.389381</td>
      <td>3.718750</td>
      <td>3.888889</td>
      <td>2.750000</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>

`unstack`, well, unstacks the specified level of a MultiIndex (by default, `groupby` turns the grouped field into an index - since we grouped by two fields, it became a MultiIndex). We unstacked the second index (remember that Python uses 0-based indexes), and then filled in NULL values with 0.

If we would have used:

```python
by_age.rating.mean().unstack(0).fillna(0)
```

We would have had our age groups as rows and movie titles as columns.

### Which movies do men and women most disagree on?
_EDIT: I realized after writing this question that Wes McKinney basically went through the exact same question in his book. It's a good, yet simple example of pivot_table, so I'm going to leave it here. Seriously though, [go buy the book](https://www.amazon.com/Python-Data-Analysis-Wrangling-Jupyter/dp/109810403X/ref=sr_1_1)._

Think about how you'd have to do this in SQL for a second. You'd have to use a combination of IF/CASE statements with aggregate functions in order to pivot your dataset. Your query would look something like this:

```sql
SELECT title, AVG(IF(sex = 'F', rating, NULL)), AVG(IF(sex = 'M', rating, NULL))
FROM lens
GROUP BY title;
```

Imagine how annoying it'd be if you had to do this on more than two columns.

DataFrame's have a pivot_table method that makes these kinds of operations much easier (and less verbose).

```python
lens.reset_index('movie_id', inplace=True)
pivoted = lens.pivot_table(index=['movie_id', 'title'],
                           columns=['sex'],
                           values='rating',
                           fill_value=0)
pivoted.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sex</th>
      <th>F</th>
      <th>M</th>
    </tr>
    <tr>
      <th>movie_id</th>
      <th>title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <th>Toy Story (1995)</th>
      <td>3.789916</td>
      <td>3.909910</td>
    </tr>
    <tr>
      <th>2</th>
      <th>GoldenEye (1995)</th>
      <td>3.368421</td>
      <td>3.178571</td>
    </tr>
    <tr>
      <th>3</th>
      <th>Four Rooms (1995)</th>
      <td>2.687500</td>
      <td>3.108108</td>
    </tr>
    <tr>
      <th>4</th>
      <th>Get Shorty (1995)</th>
      <td>3.400000</td>
      <td>3.591463</td>
    </tr>
    <tr>
      <th>5</th>
      <th>Copycat (1995)</th>
      <td>3.772727</td>
      <td>3.140625</td>
    </tr>
  </tbody>
</table>

```python
pivoted['diff'] = pivoted.M - pivoted.F
pivoted.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sex</th>
      <th>F</th>
      <th>M</th>
      <th>diff</th>
    </tr>
    <tr>
      <th>movie_id</th>
      <th>title</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <th>Toy Story (1995)</th>
      <td>3.789916</td>
      <td>3.909910</td>
      <td>0.119994</td>
    </tr>
    <tr>
      <th>2</th>
      <th>GoldenEye (1995)</th>
      <td>3.368421</td>
      <td>3.178571</td>
      <td>-0.189850</td>
    </tr>
    <tr>
      <th>3</th>
      <th>Four Rooms (1995)</th>
      <td>2.687500</td>
      <td>3.108108</td>
      <td>0.420608</td>
    </tr>
    <tr>
      <th>4</th>
      <th>Get Shorty (1995)</th>
      <td>3.400000</td>
      <td>3.591463</td>
      <td>0.191463</td>
    </tr>
    <tr>
      <th>5</th>
      <th>Copycat (1995)</th>
      <td>3.772727</td>
      <td>3.140625</td>
      <td>-0.632102</td>
    </tr>
  </tbody>
</table>

```python
pivoted.reset_index('movie_id', inplace=True)
disagreements = pivoted[pivoted.movie_id.isin(most_50.index)]['diff']
disagreements.sort_values().plot(kind='barh', figsize=[9, 15])
plt.title('Male vs. Female Avg. Ratings\n(Difference > 0 = Favored by Men)')
plt.ylabel('Title')
plt.xlabel('Average Rating Difference');
```

![bar chart of rating difference between men and women](/images/pandas-movielens-rating-differences.png)

Of course men like Terminator more than women. Independence Day though? Really?

### Additional Resources
- [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/)
- [pandas videos from PyCon](https://pyvideo.org/search?models=videos.video&q=pandas)
- [pandas and Python top 10](http://manishamde.github.io/blog/2013/03/07/pandas-and-python-top-10/)
- [Tom Augspurger's Modern pandas series](https://tomaugspurger.github.io/modern-1-intro.html)
  - [Video](https://www.youtube.com/watch?v=otCriSKVV_8&ab_channel=PyData) from Tom's pandas tutorial at PyData Seattle 2015

**Closing**

This is the point where I finally wrap this tutorial up.  Hopefully I've covered the basics well enough to pique your interest and help you get started with the library. If I've missed something critical, feel free to [let me know on Twitter](https://twitter.com/gjreda) or in the comments - I'd love constructive feedback.
