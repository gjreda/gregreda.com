Title: Translating SQL to Pandas, Part 1
Date: 2013-01-23
Slug: translating-sql-to-pandas-part1
Tags: sql, python, pandas

_I wrote a three part pandas tutorial for SQL users that you can find [here](http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/)_.

_UPDATE: If you're interested in learning pandas from a SQL perspective and would prefer to watch a video, you can find video of my 2014 PyData NYC talk [here](http://reda.io/sql2pandas)._

For some reason, I've always found SQL to a much more intuitive tool for exploring a tabular dataset than I have other languages (namely R and Python).

If you know SQL well, you can do a whole lot with it, and since data is often in a relational database anyway, it usually makes sense to stick with it.  I find that my workflow often includes writing a lot of queries in SQL (using [Sequel Pro](http://www.sequelpro.com/)) to get the data the way I want it, reading it into R (with [RStudio](http://www.rstudio.com/)), and then maybe a bit more exploration, modeling, and visualization (with [ggplot2](http://ggplot2.org/)).

Not too long ago though, I came across [Wes McKinney](http://blog.wesmckinney.com/)'s [pandas](http://pandas.pydata.org) package and my interest was immediately piqued.  Pandas adds a bunch of functionality to Python, but most importantly, it allows for a DataFrame data structure - much like a database table or R's data frame.

Given the great things I've been reading about pandas lately, I wanted to make a conscious effort to play around with it.  Instead of my typical workflow being a couple disjointed steps with SQL + R + (sometimes) Python, my thought is that it might make sense to have pandas work its way in and take over the R work.  While I probably won't be able to completely give up R (too much ggplot2 love over here), I get bored if I'm not learning something new, so pandas it is.

I intend to document the process a bit - hopefully a couple posts illustrating the differences between SQL and pandas (and maybe some R too).

Throughout the rest of this post, we're going to be working with data from the [City of Chicago's open data](https://data.cityofchicago.org) - specifically the [Towed Vechicles data](https://data.cityofchicago.org/Transportation/Towed-Vehicles/ygr5-vcbg).

#### Loading the data
##### Using SQLite
To be able to use SQL with this dataset, we'd first have to create the table.  Using [SQLite](http://www.sqlite.org/) syntax, we'd run the following:

```sql
CREATE TABLE towed (
    tow_date text,
    make text,
    style text,
    model text,
    color text,
    plate text,
    state text,
    towed_address text,
    phone text,
    inventory text
);
```
Because SQLite [uses a very generic type system](http://www.sqlite.org/datatype3.html), we don't get the strict data types that we would in most other databases (such as MySQL and PostgreSQL); therefore, all of our data is going to be stored as text.  In other databases, we'd store tow_date as a date or datetime field.

Before we read the data into SQLite, we need to tell the database to that the fields are separated by a comma.  Then we can use the import command to read the file into our table.
```sql
.separator ','
.import ./Towed_Vehicles.csv towed
```
Note that the downloaded CSV contains two header rows, so we'll need to delete those from our table since we don't need them.
```sql
DELETE FROM towed WHERE tow_date = 'Tow Date';
```
We should have 5,068 records in our table now (note: the City of Chicago regularly updates this dataset, so you might get a different number).
```sql
SELECT COUNT(*) FROM towed; -- 5068
```

##### Using Python + pandas
Let do the same with [pandas](http://pandas.pydata.org) now.
```python
import pandas as pd

col_names = ["tow_date", "make", "style", "model", "color", "plate", "state",
    "towed_address", "phone", "inventory"]
towed = pd.read_csv("Towed_Vehicles.csv", header=None, names=col_names,
    skiprows=2, parse_dates=["tow_date"])
```
The read_csv function in pandas actually allowed us to skip the two header columns and translate the tow_date field to a datetime field.

Let's check our count just to make sure.
```python
len(towed) # 5068
```

#### Selecting data
##### SQL
Selection data with SQL is fairly intuitive - just SELECT the columns you want FROM the particular table you're interested in.  You can also take advantage of the LIMIT clause to only see a subset of your data.
```sql
-- Return every column for every record in the towed table
SELECT * FROM towed;

-- Return the tow_date, make, style, model, and color for every record in the towed table
SELECT tow_date, make, style, model, color FROM towed;

-- Return every column for the first five records of the towed table
SELECT * FROM towed LIMIT 5;

-- Return every column in the towed table - start at the fifth record and show the next ten
SELECT * FROM towed LIMIT 5, 10; -- records 5-14
```

Additionally, you can throw a WHERE or ORDER BY (or both) into your queries for proper filtering and ordering of the data returned:
```sql
SELECT * FROM towed WHERE state = 'TX'; -- Only towed vehicles from Texas

SELECT * FROM towed WHERE make = 'KIA' AND state = 'TX'; -- KIAs with Texas plates

SELECT * FROM towed WHERE make = 'KIA' ORDER BY color; -- All KIAs ordered by color (A to Z)
```

##### Python + pandas
Let's do some of the same, but this time let's use pandas:
```python
# show only the make column for all records
towed["make"]

# tow_date, make, style, model, and color for the first ten records
towed[["tow_date", "make", "style", "model", "color"]][:10]

towed[:5] # first five rows (alternatively, you could use towed.head())
```

Because pandas is built on top of [NumPy](http://www.numpy.org/), we're able to use [boolean indexing](http://pandas.pydata.org/pandas-docs/dev/indexing.html#boolean-indexing).  Since we're going to replicate similar statements to the ones we did in SQL, we know we're going to need towed cars from TX made by KIA.
```python
towed[towed["state"] == "TX"] # all columns and records where the car was from TX

towed[(towed["state"] == "TX") & (towed["make"] == "KIA")] # made by KIA AND from TX

towed[(towed["state"] == "MA") | (towed["make"] == "JAGU")] # made by Jaguar OR from MA

towed[towed["make"] == "KIA"].sort("color") # made by KIA, ordered by color (A to Z)
```

##### Conclusion, Part 1
This was obviously a very basic start, but there are a lot of good things about pandas - it's certainly concise and readable.  Plus, since it works well with the various science + math packages ([SciPy](http://www.scipy.org), [NumPy](http://www.numpy.org/), [Matplotlib](http://matplotlib.org/), [statsmodels](http://statsmodels.sourceforge.net/), etc.), there's the potential to work almost entirely in one language for analysis tasks.

I plan on covering aggregate functions, pivots, and maybe some matplotlib in my next post.