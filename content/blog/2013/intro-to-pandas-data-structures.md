Title: Intro to pandas data structures
Date: 2013-10-26 1:00
Slug: intro-to-pandas-data-structures
Tags: python, pandas, sql, tutorial, data science
Description: Part one of a three part introduction to the pandas library. Geared towards SQL users, but is useful for anyone wanting to get started with pandas.

_UPDATE: If you're interested in learning pandas from a SQL perspective and would prefer to watch a video, you can find video of my 2014 PyData NYC talk [here](http://reda.io/sql2pandas)._

[A while back I claimed](/2013/01/23/translating-sql-to-pandas-part1/) I was going to write a couple of posts on translating [pandas](http://pandas.pydata.org) to SQL. I never followed up. However, the other week a couple of coworkers expressed their interest in learning a bit more about it - this seemed like a good reason to revisit the topic.
What follows is a fairly thorough introduction to the library. I chose to break it into three parts as I felt it was too long and daunting as one.

- [Part 1: Intro to pandas data structures](/2013/10/26/intro-to-pandas-data-structures/), covers the basics of the library's two main data structures - Series and DataFrames.
- [Part 2: Working with DataFrames](/2013/10/26/working-with-pandas-dataframes/), dives a bit deeper into the functionality of DataFrames. It shows how to inspect, select, filter, merge, combine, and group your data.
- [Part 3: Using pandas with the MovieLens dataset](/2013/10/26/using-pandas-on-the-movielens-dataset/), applies the learnings of the first two parts in order to answer a few basic analysis questions about the MovieLens ratings data.

If you'd like to follow along, you can find the necessary CSV files [here](https://github.com/gjreda/gregreda.com/tree/master/content/notebooks/data) and the MovieLens dataset [here](http://files.grouplens.org/datasets/movielens/ml-100k.zip).
My goal for this tutorial is to teach the basics of pandas by comparing and contrasting its syntax with SQL. Since all of my coworkers are familiar with SQL, I feel this is the best way to provide a context that can be easily understood by the intended audience.
If you're interested in learning more about the library, pandas author [Wes McKinney](https://twitter.com/wesmckinn) has written [Python for Data Analysis](http://www.amazon.com/gp/product/1449319793/ref=as_li_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1449319793&amp;linkCode=as2&amp;tag=gjreda-20&amp;linkId=MCGW4C4NOBRVV5OC), which covers it in much greater detail.

### What is it?
[pandas](http://pandas.pydata.org/) is an open source [Python](http://www.python.org/) library for data analysis. Python has always been great for prepping and munging data, but it's never been great for analysis - you'd usually end up using [R](http://www.r-project.org/) or loading it into a database and using SQL (or worse, Excel). pandas makes Python great for analysis.

## Data Structures
pandas introduces two new data structures to Python - [Series](http://pandas.pydata.org/pandas-docs/dev/dsintro.html#series) and [DataFrame](http://pandas.pydata.org/pandas-docs/dev/dsintro.html#dataframe), both of which are built on top of [NumPy](http://www.numpy.org/) (this means it's fast).

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)
%matplotlib inline
```

### Series
A Series is a one-dimensional object similar to an array, list, or column in a table. It will assign a labeled index to each item in the Series. By default, each item will receive an index label from 0 to N, where N is the length of the Series minus one.

```python
# create a Series with an arbitrary list
s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'])
s
```
<pre>
0                7
1       Heisenberg
2             3.14
3      -1789710578
4    Happy Eating!
dtype: object
</pre>

Alternatively, you can specify an index to use when creating the Series.

```python
s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'],
              index=['A', 'Z', 'C', 'Y', 'E'])
s
```
<pre>
A                7
Z       Heisenberg
C             3.14
Y      -1789710578
E    Happy Eating!
dtype: object
</pre>

The Series constructor can convert a dictonary as well, using the keys of the dictionary as its index.

```python
d = {'Chicago': 1000, 'New York': 1300, 'Portland': 900, 'San Francisco': 1100,
     'Austin': 450, 'Boston': None}
cities = pd.Series(d)
cities
```
<pre>
Austin            450
Boston            NaN
Chicago          1000
New York         1300
Portland          900
San Francisco    1100
dtype: float64
</pre>

You can use the index to select specific items from the Series ...

```python
cities['Chicago']
```
<pre>
1000.0
</pre>

```python
cities[['Chicago', 'Portland', 'San Francisco']]
```
<pre>
Chicago          1000
Portland          900
San Francisco    1100
dtype: float64
</pre>

Or you can use boolean indexing for selection.

```python
cities[cities < 1000]
```
<pre>
Austin      450
Portland    900
dtype: float64
</pre>

That last one might be a little weird, so let's make it more clear - cities < 1000 returns a Series of True/False values, which we then pass to our Series cities, returning the corresponding True items.

```python
less_than_1000 = cities < 1000
print(less_than_1000)
print('\n')
print(cities[less_than_1000])
```
<pre>
Austin            True
Boston           False
Chicago          False
New York         False
Portland          True
San Francisco    False
dtype: bool


Austin      450
Portland    900
dtype: float64
</pre>

You can also change the values in a Series on the fly.

```python
# changing based on the index
print('Old value:', cities['Chicago'])
cities['Chicago'] = 1400
print('New value:', cities['Chicago'])
```
<pre>
('Old value:', 1000.0)
('New value:', 1400.0)
</pre>


```python
# changing values using boolean logic
print(cities[cities < 1000])
print('\n')
cities[cities < 1000] = 750

print(cities[cities < 1000])
```
<pre>
Austin      450
Portland    900
dtype: float64


Austin      750
Portland    750
dtype: float64
</pre>

What if you aren't sure whether an item is in the Series? You can check using idiomatic Python.

```python
print('Seattle' in cities)
print('San Francisco' in cities)
```
<pre>
False
True
</pre>

Mathematical operations can be done using scalars and functions.

```python
# divide city values by 3
cities / 3
```
<pre>
Austin           250.000000
Boston                  NaN
Chicago          466.666667
New York         433.333333
Portland         250.000000
San Francisco    366.666667
dtype: float64
</pre>

```python
# square city values
np.square(cities)
```
<pre>
Austin            562500
Boston               NaN
Chicago          1960000
New York         1690000
Portland          562500
San Francisco    1210000
dtype: float64
</pre>

You can add two Series together, which returns a union of the two Series with the addition occurring on the shared index values. Values on either Series that did not have a shared index will produce a NULL/NaN (not a number).

```python
print(cities[['Chicago', 'New York', 'Portland']])
print('\n')
print(cities[['Austin', 'New York']])
print('\n')
print(cities[['Chicago', 'New York', 'Portland']] + cities[['Austin', 'New York']])
```
<pre>
Chicago     1400
New York    1300
Portland     750
dtype: float64


Austin       750
New York    1300
dtype: float64


Austin       NaN
Chicago      NaN
New York    2600
Portland     NaN
dtype: float64
</pre>

Notice that because Austin, Chicago, and Portland were not found in both Series, they were returned with NULL/NaN values.

NULL checking can be performed with `isnull` and `notnull`.

```python
# returns a boolean series indicating which values aren't NULL
cities.notnull()
```
<pre>
Austin            True
Boston           False
Chicago           True
New York          True
Portland          True
San Francisco     True
dtype: bool
</pre>

```python
# use boolean logic to grab the NULL cities
print(cities.isnull())
print('\n')
print(cities[cities.isnull()])
```
<pre>
Austin           False
Boston            True
Chicago          False
New York         False
Portland         False
San Francisco    False
dtype: bool


Boston   NaN
dtype: float64
</pre>

## DataFrame
A DataFrame is a tablular data structure comprised of rows and columns, akin to a spreadsheet, database table, or R's data.frame object. You can also think of a DataFrame as a group of Series objects that share an index (the column names).
For the rest of the tutorial, we'll be primarily working with DataFrames.

### Reading Data
To create a DataFrame out of common Python data structures, we can pass a dictionary of lists to the DataFrame constructor.

Using the `columns` parameter allows us to tell the constructor how we'd like the columns ordered. By default, the DataFrame constructor will order the columns alphabetically (though this isn't the case when reading from a file - more on that next).

```python
data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
        'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions', 'Lions', 'Lions'],
        'wins': [11, 8, 10, 15, 11, 6, 10, 4],
        'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
football = pd.DataFrame(data, columns=['year', 'team', 'wins', 'losses'])
football
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>team</th>
      <th>wins</th>
      <th>losses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010</td>
      <td>Bears</td>
      <td>11</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2011</td>
      <td>Bears</td>
      <td>8</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2012</td>
      <td>Bears</td>
      <td>10</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2011</td>
      <td>Packers</td>
      <td>15</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2012</td>
      <td>Packers</td>
      <td>11</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2010</td>
      <td>Lions</td>
      <td>6</td>
      <td>10</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2011</td>
      <td>Lions</td>
      <td>10</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2012</td>
      <td>Lions</td>
      <td>4</td>
      <td>12</td>
    </tr>
  </tbody>
</table>

Much more often, you'll have a dataset you want to read into a DataFrame. Let's go through several common ways of doing so.

#### CSV
Reading a CSV is as simple as calling the read_csv function. By default, the read_csv function expects the column separator to be a comma, but you can change that using the `sep` parameter.

```bash
%cd ~/Dropbox/tutorials/pandas/
```
<pre>
/Users/gjreda/Dropbox (Personal)/tutorials/pandas
</pre>

```bash
# Source: baseball-reference.com/players/r/riverma01.shtml
!head -n 5 mariano-rivera.csv
```
<pre>
Year,Age,Tm,Lg,W,L,W-L%,ERA,G,GS,GF,CG,SHO,SV,IP,H,R,ER,HR,BB,IBB,SO,HBP,BK,WP,BF,ERA+,WHIP,H/9,HR/9,BB/9,SO/9,SO/BB,Awards
1995,25,NYY,AL,5,3,.625,5.51,19,10,2,0,0,0,67.0,71,43,41,11,30,0,51,2,1,0,301,84,1.507,9.5,1.5,4.0,6.9,1.70,
1996,26,NYY,AL,8,3,.727,2.09,61,0,14,0,0,5,107.2,73,25,25,1,34,3,130,2,0,1,425,240,0.994,6.1,0.1,2.8,10.9,3.82,CYA-3MVP-12
1997,27,NYY,AL,6,4,.600,1.88,66,0,56,0,0,43,71.2,65,17,15,5,20,6,68,0,0,2,301,239,1.186,8.2,0.6,2.5,8.5,3.40,ASMVP-25
1998,28,NYY,AL,3,0,1.000,1.91,54,0,49,0,0,36,61.1,48,13,13,3,17,1,36,1,0,0,246,233,1.060,7.0,0.4,2.5,5.3,2.12,
</pre>

```python
from_csv = pd.read_csv('mariano-rivera.csv')
from_csv.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Age</th>
      <th>Tm</th>
      <th>Lg</th>
      <th>W</th>
      <th>L</th>
      <th>W-L%</th>
      <th>ERA</th>
      <th>G</th>
      <th>GS</th>
      <th>GF</th>
      <th>CG</th>
      <th>SHO</th>
      <th>SV</th>
      <th>IP</th>
      <th>H</th>
      <th>R</th>
      <th>ER</th>
      <th>HR</th>
      <th>BB</th>
      <th>IBB</th>
      <th>SO</th>
      <th>HBP</th>
      <th>BK</th>
      <th>WP</th>
      <th>BF</th>
      <th>ERA+</th>
      <th>WHIP</th>
      <th>H/9</th>
      <th>HR/9</th>
      <th>BB/9</th>
      <th>SO/9</th>
      <th>SO/BB</th>
      <th>Awards</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1995</td>
      <td>25</td>
      <td>NYY</td>
      <td>AL</td>
      <td>5</td>
      <td>3</td>
      <td>0.625</td>
      <td>5.51</td>
      <td>19</td>
      <td>10</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>67.0</td>
      <td>71</td>
      <td>43</td>
      <td>41</td>
      <td>11</td>
      <td>30</td>
      <td>0</td>
      <td>51</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>301</td>
      <td>84</td>
      <td>1.507</td>
      <td>9.5</td>
      <td>1.5</td>
      <td>4.0</td>
      <td>6.9</td>
      <td>1.70</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1996</td>
      <td>26</td>
      <td>NYY</td>
      <td>AL</td>
      <td>8</td>
      <td>3</td>
      <td>0.727</td>
      <td>2.09</td>
      <td>61</td>
      <td>0</td>
      <td>14</td>
      <td>0</td>
      <td>0</td>
      <td>5</td>
      <td>107.2</td>
      <td>73</td>
      <td>25</td>
      <td>25</td>
      <td>1</td>
      <td>34</td>
      <td>3</td>
      <td>130</td>
      <td>2</td>
      <td>0</td>
      <td>1</td>
      <td>425</td>
      <td>240</td>
      <td>0.994</td>
      <td>6.1</td>
      <td>0.1</td>
      <td>2.8</td>
      <td>10.9</td>
      <td>3.82</td>
      <td>CYA-3MVP-12</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1997</td>
      <td>27</td>
      <td>NYY</td>
      <td>AL</td>
      <td>6</td>
      <td>4</td>
      <td>0.600</td>
      <td>1.88</td>
      <td>66</td>
      <td>0</td>
      <td>56</td>
      <td>0</td>
      <td>0</td>
      <td>43</td>
      <td>71.2</td>
      <td>65</td>
      <td>17</td>
      <td>15</td>
      <td>5</td>
      <td>20</td>
      <td>6</td>
      <td>68</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>301</td>
      <td>239</td>
      <td>1.186</td>
      <td>8.2</td>
      <td>0.6</td>
      <td>2.5</td>
      <td>8.5</td>
      <td>3.40</td>
      <td>ASMVP-25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1998</td>
      <td>28</td>
      <td>NYY</td>
      <td>AL</td>
      <td>3</td>
      <td>0</td>
      <td>1.000</td>
      <td>1.91</td>
      <td>54</td>
      <td>0</td>
      <td>49</td>
      <td>0</td>
      <td>0</td>
      <td>36</td>
      <td>61.1</td>
      <td>48</td>
      <td>13</td>
      <td>13</td>
      <td>3</td>
      <td>17</td>
      <td>1</td>
      <td>36</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>246</td>
      <td>233</td>
      <td>1.060</td>
      <td>7.0</td>
      <td>0.4</td>
      <td>2.5</td>
      <td>5.3</td>
      <td>2.12</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1999</td>
      <td>29</td>
      <td>NYY</td>
      <td>AL</td>
      <td>4</td>
      <td>3</td>
      <td>0.571</td>
      <td>1.83</td>
      <td>66</td>
      <td>0</td>
      <td>63</td>
      <td>0</td>
      <td>0</td>
      <td>45</td>
      <td>69.0</td>
      <td>43</td>
      <td>15</td>
      <td>14</td>
      <td>2</td>
      <td>18</td>
      <td>3</td>
      <td>52</td>
      <td>3</td>
      <td>1</td>
      <td>2</td>
      <td>268</td>
      <td>257</td>
      <td>0.884</td>
      <td>5.6</td>
      <td>0.3</td>
      <td>2.3</td>
      <td>6.8</td>
      <td>2.89</td>
      <td>ASCYA-3MVP-14</td>
    </tr>
  </tbody>
</table>

Our file had headers, which the function inferred upon reading in the file. Had we wanted to be more explicit, we could have passed `header=None` to the function along with a list of column names to use:

```bash
# Source: pro-football-reference.com/players/M/MannPe00/touchdowns/passing/2012/
!head -n 5 peyton-passing-TDs-2012.csv
```
<pre>
1,1,2012-09-09,DEN,,PIT,W 31-19,3,71,Demaryius Thomas,Trail 7-13,Lead 14-13*
2,1,2012-09-09,DEN,,PIT,W 31-19,4,1,Jacob Tamme,Trail 14-19,Lead 22-19*
3,2,2012-09-17,DEN,@,ATL,L 21-27,2,17,Demaryius Thomas,Trail 0-20,Trail 7-20
4,3,2012-09-23,DEN,,HOU,L 25-31,4,38,Brandon Stokley,Trail 11-31,Trail 18-31
5,3,2012-09-23,DEN,,HOU,L 25-31,4,6,Joel Dreessen,Trail 18-31,Trail 25-31
</pre>

```python
cols = ['num', 'game', 'date', 'team', 'home_away', 'opponent',
        'result', 'quarter', 'distance', 'receiver', 'score_before',
        'score_after']
no_headers = pd.read_csv('peyton-passing-TDs-2012.csv', sep=',', header=None,
                         names=cols)
no_headers.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>num</th>
      <th>game</th>
      <th>date</th>
      <th>team</th>
      <th>home_away</th>
      <th>opponent</th>
      <th>result</th>
      <th>quarter</th>
      <th>distance</th>
      <th>receiver</th>
      <th>score_before</th>
      <th>score_after</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>2012-09-09</td>
      <td>DEN</td>
      <td>NaN</td>
      <td>PIT</td>
      <td>W 31-19</td>
      <td>3</td>
      <td>71</td>
      <td>Demaryius Thomas</td>
      <td>Trail 7-13</td>
      <td>Lead 14-13*</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>2012-09-09</td>
      <td>DEN</td>
      <td>NaN</td>
      <td>PIT</td>
      <td>W 31-19</td>
      <td>4</td>
      <td>1</td>
      <td>Jacob Tamme</td>
      <td>Trail 14-19</td>
      <td>Lead 22-19*</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>2012-09-17</td>
      <td>DEN</td>
      <td>@</td>
      <td>ATL</td>
      <td>L 21-27</td>
      <td>2</td>
      <td>17</td>
      <td>Demaryius Thomas</td>
      <td>Trail 0-20</td>
      <td>Trail 7-20</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>3</td>
      <td>2012-09-23</td>
      <td>DEN</td>
      <td>NaN</td>
      <td>HOU</td>
      <td>L 25-31</td>
      <td>4</td>
      <td>38</td>
      <td>Brandon Stokley</td>
      <td>Trail 11-31</td>
      <td>Trail 18-31</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3</td>
      <td>2012-09-23</td>
      <td>DEN</td>
      <td>NaN</td>
      <td>HOU</td>
      <td>L 25-31</td>
      <td>4</td>
      <td>6</td>
      <td>Joel Dreessen</td>
      <td>Trail 18-31</td>
      <td>Trail 25-31</td>
    </tr>
  </tbody>
</table>

pandas' various reader functions have many parameters allowing you to do things like skipping lines of the file, parsing dates, or specifying how to handle NA/NULL datapoints.

There's also a set of writer functions for writing to a variety of formats (CSVs, HTML tables, JSON). They function exactly as you'd expect and are typically called `to_format`:

```python
my_dataframe.to_csv('path_to_file.csv')
```
[Take a look at the IO documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html) to familiarize yourself with file reading/writing functionality.

#### Excel
Know who hates VBA? Me. I bet you do, too. Thankfully, pandas allows you to read and write Excel files, so you can easily read from Excel, write your code in Python, and then write back out to Excel - no need for VBA.

Reading Excel files requires the [xlrd](https://pypi.org/project/xlrd/) library. You can install it via pip (pip install xlrd).

Let's first write a DataFrame to Excel.

```python
# this is the DataFrame we created from a dictionary earlier
football.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>team</th>
      <th>wins</th>
      <th>losses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010</td>
      <td>Bears</td>
      <td>11</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2011</td>
      <td>Bears</td>
      <td>8</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2012</td>
      <td>Bears</td>
      <td>10</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2011</td>
      <td>Packers</td>
      <td>15</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2012</td>
      <td>Packers</td>
      <td>11</td>
      <td>5</td>
    </tr>
  </tbody>
</table>

```python
# since our index on the football DataFrame is meaningless, let's not write it
football.to_excel('football.xlsx', index=False)
```
```bash
!ls -l *.xlsx
```
<pre>
-rw-r--r--@ 1 gjreda  staff  5665 Mar 26 17:58 football.xlsx
</pre>

```python
# delete the DataFrame
del football
```
```python
# read from Excel
football = pd.read_excel('football.xlsx', 'Sheet1')
football
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>team</th>
      <th>wins</th>
      <th>losses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010</td>
      <td>Bears</td>
      <td>11</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2011</td>
      <td>Bears</td>
      <td>8</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2012</td>
      <td>Bears</td>
      <td>10</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2011</td>
      <td>Packers</td>
      <td>15</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2012</td>
      <td>Packers</td>
      <td>11</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2010</td>
      <td>Lions</td>
      <td>6</td>
      <td>10</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2011</td>
      <td>Lions</td>
      <td>10</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2012</td>
      <td>Lions</td>
      <td>4</td>
      <td>12</td>
    </tr>
  </tbody>
</table>

#### Database
pandas also has some support for [reading/writing DataFrames directly from/to a database](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html). You'll typically just need to pass a connection object or sqlalchemy engine to the `read_sql` or `to_sql` functions within the `pandas.io` module.

Note that `to_sql` executes as a series of INSERT INTO statements and thus trades speed for simplicity. If you're writing a large DataFrame to a database, it might be quicker to write the DataFrame to CSV and load that directly using the database's file import arguments.

```python
from pandas.io import sql
import sqlite3

conn = sqlite3.connect('/Users/gjreda/Dropbox/gregreda.com/_code/towed')
query = "SELECT * FROM towed WHERE make = 'FORD';"

results = sql.read_sql(query, con=conn)
results.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tow_date</th>
      <th>make</th>
      <th>style</th>
      <th>model</th>
      <th>color</th>
      <th>plate</th>
      <th>state</th>
      <th>towed_address</th>
      <th>phone</th>
      <th>inventory</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01/19/2013</td>
      <td>FORD</td>
      <td>LL</td>
      <td></td>
      <td>RED</td>
      <td>N786361</td>
      <td>IL</td>
      <td>400 E. Lower Wacker</td>
      <td>(312) 744-7550</td>
      <td>877040</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01/19/2013</td>
      <td>FORD</td>
      <td>4D</td>
      <td></td>
      <td>GRN</td>
      <td>L307211</td>
      <td>IL</td>
      <td>701 N. Sacramento</td>
      <td>(773) 265-7605</td>
      <td>6738005</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01/19/2013</td>
      <td>FORD</td>
      <td>4D</td>
      <td></td>
      <td>GRY</td>
      <td>P576738</td>
      <td>IL</td>
      <td>701 N. Sacramento</td>
      <td>(773) 265-7605</td>
      <td>6738001</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01/19/2013</td>
      <td>FORD</td>
      <td>LL</td>
      <td></td>
      <td>BLK</td>
      <td>N155890</td>
      <td>IL</td>
      <td>10300 S. Doty</td>
      <td>(773) 568-8495</td>
      <td>2699210</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01/19/2013</td>
      <td>FORD</td>
      <td>LL</td>
      <td></td>
      <td>TAN</td>
      <td>H953638</td>
      <td>IL</td>
      <td>10300 S. Doty</td>
      <td>(773) 568-8495</td>
      <td>2699209</td>
    </tr>
  </tbody>
</table>

#### Clipboard
While the results of a query can be read directly into a DataFrame, I prefer to read the results directly from the clipboard. I'm often tweaking queries in my SQL client ([Sequel Pro](http://www.sequelpro.com/)), so I would rather see the results before I read it into pandas. Once I'm confident I have the data I want, then I'll read it into a DataFrame.

This works just as well with any type of delimited data you've copied to your clipboard. The function does a good job of inferring the delimiter, but you can also use the sep parameter to be explicit.

[Hank Aaron](https://www.baseball-reference.com/players/a/aaronha01.shtml)

<img src="http://i.imgur.com/xiySJ2e.png" alt="hank-aaron-stats-screenshot">

```python
hank = pd.read_clipboard()
hank.head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Age</th>
      <th>Tm</th>
      <th>Lg</th>
      <th>G</th>
      <th>PA</th>
      <th>AB</th>
      <th>R</th>
      <th>H</th>
      <th>2B</th>
      <th>3B</th>
      <th>HR</th>
      <th>RBI</th>
      <th>SB</th>
      <th>CS</th>
      <th>BB</th>
      <th>SO</th>
      <th>BA</th>
      <th>OBP</th>
      <th>SLG</th>
      <th>OPS</th>
      <th>OPS+</th>
      <th>TB</th>
      <th>GDP</th>
      <th>HBP</th>
      <th>SH</th>
      <th>SF</th>
      <th>IBB</th>
      <th>Pos</th>
      <th>Awards</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1954</td>
      <td>20</td>
      <td>MLN</td>
      <td>NL</td>
      <td>122</td>
      <td>509</td>
      <td>468</td>
      <td>58</td>
      <td>131</td>
      <td>27</td>
      <td>6</td>
      <td>13</td>
      <td>69</td>
      <td>2</td>
      <td>2</td>
      <td>28</td>
      <td>39</td>
      <td>0.280</td>
      <td>0.322</td>
      <td>0.447</td>
      <td>0.769</td>
      <td>104</td>
      <td>209</td>
      <td>13</td>
      <td>3</td>
      <td>6</td>
      <td>4</td>
      <td>NaN</td>
      <td>*79</td>
      <td>RoY-4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1955 ★</td>
      <td>21</td>
      <td>MLN</td>
      <td>NL</td>
      <td>153</td>
      <td>665</td>
      <td>602</td>
      <td>105</td>
      <td>189</td>
      <td>37</td>
      <td>9</td>
      <td>27</td>
      <td>106</td>
      <td>3</td>
      <td>1</td>
      <td>49</td>
      <td>61</td>
      <td>0.314</td>
      <td>0.366</td>
      <td>0.540</td>
      <td>0.906</td>
      <td>141</td>
      <td>325</td>
      <td>20</td>
      <td>3</td>
      <td>7</td>
      <td>4</td>
      <td>5</td>
      <td>*974</td>
      <td>AS,MVP-9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1956 ★</td>
      <td>22</td>
      <td>MLN</td>
      <td>NL</td>
      <td>153</td>
      <td>660</td>
      <td>609</td>
      <td>106</td>
      <td>200</td>
      <td>34</td>
      <td>14</td>
      <td>26</td>
      <td>92</td>
      <td>2</td>
      <td>4</td>
      <td>37</td>
      <td>54</td>
      <td>0.328</td>
      <td>0.365</td>
      <td>0.558</td>
      <td>0.923</td>
      <td>151</td>
      <td>340</td>
      <td>21</td>
      <td>2</td>
      <td>5</td>
      <td>7</td>
      <td>6</td>
      <td>*9</td>
      <td>AS,MVP-3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1957 ★</td>
      <td>23</td>
      <td>MLN</td>
      <td>NL</td>
      <td>151</td>
      <td>675</td>
      <td>615</td>
      <td>118</td>
      <td>198</td>
      <td>27</td>
      <td>6</td>
      <td>44</td>
      <td>132</td>
      <td>1</td>
      <td>1</td>
      <td>57</td>
      <td>58</td>
      <td>0.322</td>
      <td>0.378</td>
      <td>0.600</td>
      <td>0.978</td>
      <td>166</td>
      <td>369</td>
      <td>13</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>15</td>
      <td>*98</td>
      <td>AS,MVP-1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1958 ★</td>
      <td>24</td>
      <td>MLN</td>
      <td>NL</td>
      <td>153</td>
      <td>664</td>
      <td>601</td>
      <td>109</td>
      <td>196</td>
      <td>34</td>
      <td>4</td>
      <td>30</td>
      <td>95</td>
      <td>4</td>
      <td>1</td>
      <td>59</td>
      <td>49</td>
      <td>0.326</td>
      <td>0.386</td>
      <td>0.546</td>
      <td>0.931</td>
      <td>152</td>
      <td>328</td>
      <td>21</td>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>16</td>
      <td>*98</td>
      <td>AS,MVP-3,GG</td>
    </tr>
  </tbody>
</table>

#### URL
With `read_table`, we can also read directly from a URL.

Let's use the [best sandwiches data](https://raw.githubusercontent.com/gjreda/best-sandwiches/master/data/best-sandwiches-geocode.tsv) that I [wrote about scraping](/2013/05/06/more-web-scraping-with-python/) a while back.

```python
url = 'https://raw.github.com/gjreda/best-sandwiches/master/data/best-sandwiches-geocode.tsv'

# fetch the text from the URL and read it into a DataFrame
from_url = pd.read_table(url, sep='\t')
from_url.head(3)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rank</th>
      <th>sandwich</th>
      <th>restaurant</th>
      <th>description</th>
      <th>price</th>
      <th>address</th>
      <th>city</th>
      <th>phone</th>
      <th>website</th>
      <th>full_address</th>
      <th>formatted_address</th>
      <th>lat</th>
      <th>lng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>BLT</td>
      <td>Old Oak Tap</td>
      <td>The B is applewood smoked&amp;mdash;nice and snapp...</td>
      <td>$10</td>
      <td>2109 W. Chicago Ave.</td>
      <td>Chicago</td>
      <td>773-772-0406</td>
      <td>theoldoaktap.com</td>
      <td>2109 W. Chicago Ave., Chicago</td>
      <td>2109 West Chicago Avenue, Chicago, IL 60622, USA</td>
      <td>41.895734</td>
      <td>-87.679960</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Fried Bologna</td>
      <td>Au Cheval</td>
      <td>Thought your bologna-eating days had retired w...</td>
      <td>$9</td>
      <td>800 W. Randolph St.</td>
      <td>Chicago</td>
      <td>312-929-4580</td>
      <td>aucheval.tumblr.com</td>
      <td>800 W. Randolph St., Chicago</td>
      <td>800 West Randolph Street, Chicago, IL 60607, USA</td>
      <td>41.884672</td>
      <td>-87.647754</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Woodland Mushroom</td>
      <td>Xoco</td>
      <td>Leave it to Rick Bayless and crew to come up w...</td>
      <td>$9.50.</td>
      <td>445 N. Clark St.</td>
      <td>Chicago</td>
      <td>312-334-3688</td>
      <td>rickbayless.com</td>
      <td>445 N. Clark St., Chicago</td>
      <td>445 North Clark Street, Chicago, IL 60654, USA</td>
      <td>41.890602</td>
      <td>-87.630925</td>
    </tr>
  </tbody>
</table>

_Move onto the next section, which covers [working with DataFrames](/2013/10/26/working-with-pandas-dataframes/)._
