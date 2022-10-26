Title: Working with DataFrames
Date: 2013-10-26 2:00
Slug: working-with-pandas-dataframes
Tags: python, pandas, sql, tutorial, data science
Description: Part two of a three part introduction to the pandas library for Python. It is geared towards SQL users, but is useful for anyone wanting to get started with pandas.

_UPDATE: If you're interested in learning pandas from a SQL perspective and would prefer to watch a video, you can find video of my 2014 PyData NYC talk [here](http://reda.io/sql2pandas)._

_This is part two of a three part introduction to [pandas](http://pandas.pydata.org), a Python library for data analysis. The tutorial is primarily geared towards SQL users, but is useful for anyone wanting to get started with the library._

- [Part 1: Intro to pandas data structures](/2013/10/26/intro-to-pandas-data-structures/), covers the basics of the library's two main data structures - Series and DataFrames.
- [Part 2: Working with DataFrames](/2013/10/26/working-with-pandas-dataframes/), dives a bit deeper into the functionality of DataFrames. It shows how to inspect, select, filter, merge, combine, and group your data.
- [Part 3: Using pandas with the MovieLens dataset](/2013/10/26/using-pandas-on-the-movielens-dataset/), applies the learnings of the first two parts in order to answer a few basic analysis questions about the MovieLens ratings data.

## Working with DataFrames
Now that we can get data into a DataFrame, we can finally start working with them. pandas has an abundance of functionality, far too much for me to cover in this introduction. I'd encourage anyone interested in diving deeper into the library to check out its [excellent documentation](https://pandas.pydata.org/pandas-docs/stable/). Or just use Google - there are a lot of Stack Overflow questions and blog posts covering specifics of the library.

We'll be using the [MovieLens](https://grouplens.org/datasets/movielens/) dataset in many examples going forward. The dataset contains 100,000 ratings made by 943 users on 1,682 movies.

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
```

### Inspection
```python
movies.info()
```
```output
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1682 entries, 0 to 1681
Data columns (total 5 columns):
movie_id              1682 non-null int64
title                 1682 non-null object
release_date          1681 non-null object
video_release_date    0 non-null float64
imdb_url              1679 non-null object
dtypes: float64(1), int64(1), object(3)
memory usage: 78.8+ KB
```

The output tells a few things about our DataFrame.

1. It's obviously an instance of a DataFrame.
2. Each row was assigned an index of 0 to N-1, where N is the number of rows in the DataFrame. pandas will do this by default if an index is not specified. Don't worry, this can be changed later.
3. There are 1,682 rows (every row must have an index).
4. Our dataset has five total columns, one of which isn't populated at all (video_release_date) and two that are missing some values (release_date and imdb_url).
5. The last datatypes of each column, but not necessarily in the corresponding order to the listed columns. You should use the `dtypes` method to get the datatype for each column.
6. An approximate amount of RAM used to hold the DataFrame. See the `.memory_usage` method

```python
movies.dtypes
```
```output
movie_id                int64
title                  object
release_date           object
video_release_date    float64
imdb_url               object
dtype: object
```

DataFrame's also have a `describe` method, which is great for seeing basic statistics about the dataset's numeric columns. Be careful though, since this will return information on all columns of a numeric datatype.

```python
users.describe()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>943.000000</td>
      <td>943.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>472.000000</td>
      <td>34.051962</td>
    </tr>
    <tr>
      <th>std</th>
      <td>272.364951</td>
      <td>12.192740</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>7.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>236.500000</td>
      <td>25.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>472.000000</td>
      <td>31.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>707.500000</td>
      <td>43.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>943.000000</td>
      <td>73.000000</td>
    </tr>
  </tbody>
</table>

Notice user_id was included since it's numeric. Since this is an ID value, the stats for it don't really matter.

We can quickly see the average age of our users is just above 34 years old, with the youngest being 7 and the oldest being 73. The median age is 31, with the youngest quartile of users being 25 or younger, and the oldest quartile being at least 43.

You've probably noticed that I've used the `head` method regularly throughout this post - by default, `head` displays the first five records of the dataset, while `tail` displays the last five.

```python
movies.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>movie_id</th>
      <th>title</th>
      <th>release_date</th>
      <th>video_release_date</th>
      <th>imdb_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Toy Story (1995)</td>
      <td>01-Jan-1995</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Toy%20Story%2...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>GoldenEye (1995)</td>
      <td>01-Jan-1995</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?GoldenEye%20(...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Four Rooms (1995)</td>
      <td>01-Jan-1995</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Four%20Rooms%...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Get Shorty (1995)</td>
      <td>01-Jan-1995</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Get%20Shorty%...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Copycat (1995)</td>
      <td>01-Jan-1995</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Copycat%20(1995)</td>
    </tr>
  </tbody>
</table>

```python
movies.tail(3)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>movie_id</th>
      <th>title</th>
      <th>release_date</th>
      <th>video_release_date</th>
      <th>imdb_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1679</th>
      <td>1680</td>
      <td>Sliding Doors (1998)</td>
      <td>01-Jan-1998</td>
      <td>NaN</td>
      <td>http://us.imdb.com/Title?Sliding+Doors+(1998)</td>
    </tr>
    <tr>
      <th>1680</th>
      <td>1681</td>
      <td>You So Crazy (1994)</td>
      <td>01-Jan-1994</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?You%20So%20Cr...</td>
    </tr>
    <tr>
      <th>1681</th>
      <td>1682</td>
      <td>Scream of Stone (Schrei aus Stein) (1991)</td>
      <td>08-Mar-1996</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Schrei%20aus%...</td>
    </tr>
  </tbody>
</table>

Alternatively, Python's regular [slicing](https://docs.python.org/release/2.3.5/whatsnew/section-slices.html) syntax works as well.

```python
movies[20:22]
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>movie_id</th>
      <th>title</th>
      <th>release_date</th>
      <th>video_release_date</th>
      <th>imdb_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20</th>
      <td>21</td>
      <td>Muppet Treasure Island (1996)</td>
      <td>16-Feb-1996</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Muppet%20Trea...</td>
    </tr>
    <tr>
      <th>21</th>
      <td>22</td>
      <td>Braveheart (1995)</td>
      <td>16-Feb-1996</td>
      <td>NaN</td>
      <td>http://us.imdb.com/M/title-exact?Braveheart%20...</td>
    </tr>
  </tbody>
</table>

### Selecting
You can think of a DataFrame as a group of Series that share an index (in this case the column headers). This makes it easy to select specific columns.

Selecting a single column from the DataFrame will return a Series object.

```python
users['occupation'].head()
```
```output
0    technician
1         other
2        writer
3    technician
4         other
Name: occupation, dtype: object
```

To select multiple columns, simply pass a list of column names to the DataFrame, the output of which will be a DataFrame.

```python
print(users[['age', 'zip_code']].head())
print('\n')

# can also store in a variable to use later
columns_you_want = ['occupation', 'sex'] 
print(users[columns_you_want].head())
```
```output
   age zip_code
0   24    85711
1   53    94043
2   23    32067
3   24    43537
4   33    15213


   occupation sex
0  technician   M
1       other   F
2      writer   M
3  technician   M
4       other   F
```

Row selection can be done multiple ways, but doing so by an individual index or boolean indexing are typically easiest.

```python
# users older than 25
print(users[users.age > 25].head(3))
print('\n')

# users aged 40 AND male
print(users[(users.age == 40) & (users.sex == 'M')].head(3))
print('\n')

# users younger than 30 OR female
print(users[(users.sex == 'F') | (users.age < 30)].head(3))
```
```output
   user_id  age sex occupation zip_code
1        2   53   F      other    94043
4        5   33   F      other    15213
5        6   42   M  executive    98101


     user_id  age sex  occupation zip_code
18        19   40   M   librarian    02138
82        83   40   M       other    44133
115      116   40   M  healthcare    97232


   user_id  age sex  occupation zip_code
0        1   24   M  technician    85711
1        2   53   F       other    94043
2        3   23   M      writer    32067
```

Since our index is kind of meaningless right now, let's set it to the user_id using the `set_index` method. By default, `set_index` returns a new DataFrame, so you'll have to specify if you'd like the changes to occur in place.

This has confused me in the past, so look carefully at the code and output below.

```python
print(users.set_index('user_id').head())
print('\n')

print(users.head())
print("\n^^^ I didn't actually change the DataFrame. ^^^\n")

with_new_index = users.set_index('user_id')
print(with_new_index.head())
print("\n^^^ set_index actually returns a new DataFrame. ^^^\n")
```
```output
         age sex  occupation zip_code
user_id                              
1         24   M  technician    85711
2         53   F       other    94043
3         23   M      writer    32067
4         24   M  technician    43537
5         33   F       other    15213


   user_id  age sex  occupation zip_code
0        1   24   M  technician    85711
1        2   53   F       other    94043
2        3   23   M      writer    32067
3        4   24   M  technician    43537
4        5   33   F       other    15213

^^^ I didn't actually change the DataFrame. ^^^

         age sex  occupation zip_code
user_id                              
1         24   M  technician    85711
2         53   F       other    94043
3         23   M      writer    32067
4         24   M  technician    43537
5         33   F       other    15213

^^^ set_index actually returns a new DataFrame. ^^^
```

If you want to modify your existing DataFrame, use the `inplace` parameter. Most DataFrame methods return new a DataFrames, while offering an `inplace` parameter. Note that the `inplace` version might not actually be any more efficient (in terms of speed or memory usage) than the regular version.

```python
users.set_index('user_id', inplace=True)
users.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>sex</th>
      <th>occupation</th>
      <th>zip_code</th>
    </tr>
    <tr>
      <th>user_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>24</td>
      <td>M</td>
      <td>technician</td>
      <td>85711</td>
    </tr>
    <tr>
      <th>2</th>
      <td>53</td>
      <td>F</td>
      <td>other</td>
      <td>94043</td>
    </tr>
    <tr>
      <th>3</th>
      <td>23</td>
      <td>M</td>
      <td>writer</td>
      <td>32067</td>
    </tr>
    <tr>
      <th>4</th>
      <td>24</td>
      <td>M</td>
      <td>technician</td>
      <td>43537</td>
    </tr>
    <tr>
      <th>5</th>
      <td>33</td>
      <td>F</td>
      <td>other</td>
      <td>15213</td>
    </tr>
  </tbody>
</table>

Notice that we've lost the default pandas 0-based index and moved the user_id into its place. We can select rows by position using the `iloc` method.

```python
print(users.iloc[99])
print('\n')
print(users.iloc[[1, 50, 300]])
```
```output
age                  36
sex                   M
occupation    executive
zip_code          90254
Name: 100, dtype: object


         age sex occupation zip_code
user_id                             
2         53   F      other    94043
51        28   M   educator    16509
301       24   M    student    55439
```

And we can select rows by label with the `loc` method.

```python
print(users.loc[100])
print('\n')
print(users.loc[[2, 51, 301]])
```
```output
age                  36
sex                   M
occupation    executive
zip_code          90254
Name: 100, dtype: object


         age sex occupation zip_code
user_id                             
2         53   F      other    94043
51        28   M   educator    16509
301       24   M    student    55439
```

If we realize later that we liked the old pandas default index, we can just `reset_index`. The same rules for `inplace` apply.

```python
users.reset_index(inplace=True)
users.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>age</th>
      <th>sex</th>
      <th>occupation</th>
      <th>zip_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>24</td>
      <td>M</td>
      <td>technician</td>
      <td>85711</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>53</td>
      <td>F</td>
      <td>other</td>
      <td>94043</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>23</td>
      <td>M</td>
      <td>writer</td>
      <td>32067</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>24</td>
      <td>M</td>
      <td>technician</td>
      <td>43537</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>33</td>
      <td>F</td>
      <td>other</td>
      <td>15213</td>
    </tr>
  </tbody>
</table>

The simplified rules of indexing are
- Use `loc` for label-based indexing
- Use `iloc` for positional indexing
I've found that I can usually get by with boolean indexing, `loc` and `iloc`, but pandas has a whole host of [other ways to do selection](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html).

### Joining
Throughout an analysis, we'll often need to merge/join datasets as data is typically stored in a [relational](https://en.wikipedia.org/wiki/Relational_database) manner.

Our MovieLens data is a good example of this - a rating requires both a user and a movie, and the datasets are linked together by a key - in this case, the user_id and movie_id. It's possible for a user to be associated with zero or many ratings and movies. Likewise, a movie can be rated zero or many times, by a number of different users.

Like SQL's JOIN clause, `pandas.merge` allows two DataFrames to be joined on one or more keys. The function provides a series of parameters (`on, left_on, right_on, left_index, right_index`) allowing you to specify the columns or indexes on which to join.

By default, `pandas.merge` operates as an inner join, which can be changed using the `how` parameter.

From the function's docstring:
> how : {'left', 'right', 'outer', 'inner'}, default 'inner' 
> - left: use only keys from left frame (SQL: left outer join) 
> - right: use only keys from right frame (SQL: right outer join)
> - outer: use union of keys from both frames (SQL: full outer join)
> - inner: use intersection of keys from both frames (SQL: inner join)

Below are some examples of what each look like.

```python
left_frame = pd.DataFrame({'key': range(5), 
                           'left_value': ['a', 'b', 'c', 'd', 'e']})
right_frame = pd.DataFrame({'key': range(2, 7), 
                           'right_value': ['f', 'g', 'h', 'i', 'j']})
print(left_frame)
print('\n')
print(right_frame)
```
```output
   key left_value
0    0          a
1    1          b
2    2          c
3    3          d
4    4          e


   key right_value
0    2           f
1    3           g
2    4           h
3    5           i
4    6           j
```

#### inner join (default)
```python
pd.merge(left_frame, right_frame, on='key', how='inner')
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>c</td>
      <td>f</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>d</td>
      <td>g</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>e</td>
      <td>h</td>
    </tr>
  </tbody>
</table>

We lose values from both frames since certain keys do not match up. The SQL equivalent is:

```sql
SELECT left_frame.key, left_frame.left_value, right_frame.right_value
FROM left_frame
INNER JOIN right_frame
    ON left_frame.key = right_frame.key;
```

Had our key columns not been named the same, we could have used the `left_on` and `right_on` parameters to specify which fields to join from each frame.

```python
pd.merge(left_frame, right_frame, left_on='left_key', right_on='right_key')
```

Alternatively, if our keys were indexes, we could use the `left_index` or `right_index` parameters, which accept a True/False value. You can mix and match columns and indexes like so:

```python
pd.merge(left_frame, right_frame, left_on='key', right_index=True)
```

#### left outer join

```python
pd.merge(left_frame, right_frame, on='key', how='left')
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>a</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>b</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>c</td>
      <td>f</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>d</td>
      <td>g</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>e</td>
      <td>h</td>
    </tr>
  </tbody>
</table>

We keep everything from the left frame, pulling in the value from the right frame where the keys match up. The right_value is NULL where keys do not match (NaN).

SQL Equivalent:

```sql
SELECT left_frame.key, left_frame.left_value, right_frame.right_value
FROM left_frame
LEFT JOIN right_frame
    ON left_frame.key = right_frame.key;
```

#### right outer join

```python
pd.merge(left_frame, right_frame, on='key', how='right')
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>c</td>
      <td>f</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>d</td>
      <td>g</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>e</td>
      <td>h</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>NaN</td>
      <td>i</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>NaN</td>
      <td>j</td>
    </tr>
  </tbody>
</table>

This time we've kept everything from the right frame with the left_value being NULL where the right frame's key did not find a match.

SQL Equivalent:

```sql
SELECT right_frame.key, left_frame.left_value, right_frame.right_value
FROM left_frame
RIGHT JOIN right_frame
    ON left_frame.key = right_frame.key;
```

#### full outer join
```python
pd.merge(left_frame, right_frame, on='key', how='outer')
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>a</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>b</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>c</td>
      <td>f</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>d</td>
      <td>g</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>e</td>
      <td>h</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>NaN</td>
      <td>i</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>NaN</td>
      <td>j</td>
    </tr>
  </tbody>
</table>

We've kept everything from both frames, regardless of whether or not there was a match on both sides. Where there was not a match, the values corresponding to that key are NULL.

SQL Equivalent (though some databases don't allow FULL JOINs (e.g. MySQL)):

```sql
SELECT IFNULL(left_frame.key, right_frame.key) key
        , left_frame.left_value, right_frame.right_value
FROM left_frame
FULL OUTER JOIN right_frame
    ON left_frame.key = right_frame.key;
```

### Combining

pandas also provides a way to combine DataFrames along an axis - `pandas.concat`. While the function is equivalent to SQL's UNION clause, there's a lot more that can be done with it.

`pandas.concat` takes a list of Series or DataFrames and returns a Series or DataFrame of the concatenated objects. Note that because the function takes list, you can combine many objects at once.

```python
pd.concat([left_frame, right_frame])
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>a</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>b</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>c</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>d</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>e</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>NaN</td>
      <td>f</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>NaN</td>
      <td>g</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>NaN</td>
      <td>h</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>NaN</td>
      <td>i</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>NaN</td>
      <td>j</td>
    </tr>
  </tbody>
</table>

By default, the function will vertically append the objects to one another, combining columns with the same name. We can see above that values not matching up will be NULL.

Additionally, objects can be concatentated side-by-side using the function's axis parameter.

```python
pd.concat([left_frame, right_frame], axis=1)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>left_value</th>
      <th>key</th>
      <th>right_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>a</td>
      <td>2</td>
      <td>f</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>b</td>
      <td>3</td>
      <td>g</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>c</td>
      <td>4</td>
      <td>h</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>d</td>
      <td>5</td>
      <td>i</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>e</td>
      <td>6</td>
      <td>j</td>
    </tr>
  </tbody>
</table>

`pandas.concat` can be used in a variety of ways; however, I've typically only used it to combine Series/DataFrames into one unified object. The [documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#concatenating-objects) has some examples on the ways it can be used.

### Grouping
Grouping in pandas took some time for me to grasp, but it's pretty awesome once it clicks.

pandas `groupby` method draws largely from the [split-apply-combine strategy for data analysis](https://vita.had.co.nz/papers/plyr.html). If you're not familiar with this methodology, I highly suggest you read up on it. It does a great job of illustrating how to properly think through a data problem, which I feel is more important than any technical skill a data analyst/scientist can possess.

When approaching a data analysis problem, you'll often break it apart into manageable pieces, perform some operations on each of the pieces, and then put everything back together again (this is the gist split-apply-combine strategy). pandas `groupby` is great for these problems (R users should check out the [plyr](http://plyr.had.co.nz/) and [dplyr](https://github.com/tidyverse/dplyr) packages).

If you've ever used SQL's GROUP BY or an Excel Pivot Table, you've thought with this mindset, probably without realizing it.

Assume we have a DataFrame and want to get the average for each group - visually, the split-apply-combine method looks like this:
<img src="http://i.imgur.com/yjNkiwL.png" alt="Source: Gratuitously borrowed from [Hadley Wickham's Data Science in R slides](http://courses.had.co.nz/12-oscon/)">

The City of Chicago is kind enough to publish all city employee salaries to its open data portal. Let's go through some basic `groupby` examples using this data.

```bash
!head -n 3 city-of-chicago-salaries.csv
```
```output
Name,Position Title,Department,Employee Annual Salary
"AARON,  ELVIA J",WATER RATE TAKER,WATER MGMNT,$85512.00
"AARON,  JEFFERY M",POLICE OFFICER,POLICE,$75372.00
```

Since the data contains a dollar sign for each salary, python will treat the field as a series of strings. We can use the `converters` parameter to change this when reading in the file.

> converters : dict. optional
> - Dict of functions for converting values in certain columns. Keys can either be integers or column labels

```python
headers = ['name', 'title', 'department', 'salary']
chicago = pd.read_csv('city-of-chicago-salaries.csv', 
                      header=0,
                      names=headers,
                      converters={'salary': lambda x: float(x.replace('$', ''))})
chicago.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>title</th>
      <th>department</th>
      <th>salary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AARON,  ELVIA J</td>
      <td>WATER RATE TAKER</td>
      <td>WATER MGMNT</td>
      <td>85512</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AARON,  JEFFERY M</td>
      <td>POLICE OFFICER</td>
      <td>POLICE</td>
      <td>75372</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AARON,  KIMBERLEI R</td>
      <td>CHIEF CONTRACT EXPEDITER</td>
      <td>GENERAL SERVICES</td>
      <td>80916</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ABAD JR,  VICENTE M</td>
      <td>CIVIL ENGINEER IV</td>
      <td>WATER MGMNT</td>
      <td>99648</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ABBATACOLA,  ROBERT J</td>
      <td>ELECTRICAL MECHANIC</td>
      <td>AVIATION</td>
      <td>89440</td>
    </tr>
  </tbody>
</table>

pandas `groupby` returns a DataFrameGroupBy object which has a variety of methods, many of which are similar to standard SQL aggregate functions.

```python
by_dept = chicago.groupby('department')
by_dept
```
```output
<pandas.core.groupby.DataFrameGroupBy object at 0x1128ca1d0>
```

Calling `count` returns the total number of NOT NULL values within each column. If we were interested in the total number of records in each group, we could use `size`.

```python
print(by_dept.count().head()) # NOT NULL records within each column
print('\n')
print(by_dept.size().tail()) # total records for each department
```
```output
                   name  title  salary
department                            
ADMIN HEARNG         42     42      42
ANIMAL CONTRL        61     61      61
AVIATION           1218   1218    1218
BOARD OF ELECTION   110    110     110
BOARD OF ETHICS       9      9       9


department
PUBLIC LIBRARY     926
STREETS & SAN     2070
TRANSPORTN        1168
TREASURER           25
WATER MGMNT       1857
dtype: int64
```

Summation can be done via `sum`, averaging by `mean`, etc. (if it's a SQL function, chances are it exists in pandas). Oh, and there's median too, something not available in most databases.

```python
print(by_dept.sum()[20:25]) # total salaries of each department
print('\n')
print(by_dept.mean()[20:25]) # average salary of each department
print('\n')
print(by_dept.median()[20:25]) # take that, RDBMS!
```
```output
                       salary
department                   
HUMAN RESOURCES     4850928.0
INSPECTOR GEN       4035150.0
IPRA                7006128.0
LAW                31883920.2
LICENSE APPL COMM     65436.0


                         salary
department                     
HUMAN RESOURCES    71337.176471
INSPECTOR GEN      80703.000000
IPRA               82425.035294
LAW                70853.156000
LICENSE APPL COMM  65436.000000


                   salary
department               
HUMAN RESOURCES     68496
INSPECTOR GEN       76116
IPRA                82524
LAW                 66492
LICENSE APPL COMM   65436
```

Operations can also be done on an individual Series within a grouped object. Say we were curious about the five departments with the most distinct titles - the pandas equivalent to:

```sql
SELECT department, COUNT(DISTINCT title)
FROM chicago
GROUP BY department
ORDER BY 2 DESC
LIMIT 5;
```

pandas is a lot less verbose here ...

```python
by_dept.title.nunique().sort_values(ascending=False)[:5]
```
```output
department
WATER MGMNT    153
TRANSPORTN     150
POLICE         130
AVIATION       125
HEALTH         118
Name: title, dtype: int64
```

### split-apply-combine
The real power of `groupby` comes from it's split-apply-combine ability.

What if we wanted to see the highest paid employee within each department. Given our current dataset, we'd have to do something like this in SQL:

```sql
SELECT *
FROM chicago c
INNER JOIN (
    SELECT department, max(salary) max_salary
    FROM chicago
    GROUP BY department
) m
ON c.department = m.department
AND c.salary = m.max_salary;
```

This would give you the highest paid person in each department, but it would return multiple if there were many equally high paid people within a department.

Alternatively, you could alter the table, add a column, and then write an update statement to populate that column. However, that's not always an option.

_Note: This would be a lot easier in PostgreSQL, T-SQL, and possibly Oracle due to the existence of partition/window/analytic functions. I've chosen to use MySQL syntax throughout this tutorial because of it's popularity. Unfortunately, MySQL doesn't have similar functions._


Using `groupby` we can define a function (which we'll call `ranker`) that will label each record from 1 to N, where N is the number of employees within the department. We can then call `apply` to, well, apply that function to each group (in this case, each department).

```python
def ranker(df):
    """Assigns a rank to each employee based on salary, with 1 being the highest paid.
    Assumes the data is DESC sorted."""
    df['dept_rank'] = np.arange(len(df)) + 1
    return df

chicago.sort_values('salary', ascending=False, inplace=True)
chicago = chicago.groupby('department').apply(ranker)
print(chicago[chicago.dept_rank == 1].head(7))
```
```output
                         name                     title      department  \
18039     MC CARTHY,  GARRY F  SUPERINTENDENT OF POLICE          POLICE   
8004           EMANUEL,  RAHM                     MAYOR  MAYOR'S OFFICE   
25588       SANTIAGO,  JOSE A         FIRE COMMISSIONER            FIRE   
763    ANDOLINO,  ROSEMARIE S  COMMISSIONER OF AVIATION        AVIATION   
4697     CHOUCAIR,  BECHARA N    COMMISSIONER OF HEALTH          HEALTH   
21971      PATTON,  STEPHEN R       CORPORATION COUNSEL             LAW   
12635      HOLT,  ALEXANDRA D                BUDGET DIR   BUDGET & MGMT   

       salary  dept_rank  
18039  260004          1  
8004   216210          1  
25588  202728          1  
763    186576          1  
4697   177156          1  
21971  173664          1  
12635  169992          1  
```

_Move onto part three, [using pandas with the MovieLens dataset](/2013/10/26/using-pandas-on-the-movielens-dataset/)._
