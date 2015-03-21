Title: Useful Unix commands for data science
Date: 2013-07-15
Slug: unix-commands-for-data-science
Tags: unix, terminal, data, data science
Description: The command line tools that ship with any Unix-like system are extremely handy for many data tasks. Here are some of the ones that I've found most useful.
Affiliate_Link: <iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=tf_til&ad_type=product_link&tracking_id=gregrecom-20&marketplace=amazon&region=US&placement=1491947853&asins=1491947853&linkId=BMTSVBUMC7XEVULJ&show_border=true&link_opens_in_new_window=true"></iframe>

Imagine you have a 4.2GB CSV file.  It has over 12 million records and 50 columns.  All you need from this file is the sum of all values in one particular column.

How would you do it?

Writing a script in [python](http://www.python.org/)/[ruby](http://www.ruby-lang.org/)/[perl](http://www.perl.org/)/whatever would probably take a few minutes and then even more time for the script to actually complete.  A [database](http://en.wikipedia.org/wiki/Database) and [SQL](http://en.wikipedia.org/wiki/SQL) would be fairly quick, but then you'd have load the data, which is kind of a pain.

Thankfully, the [Unix utilities](http://en.wikipedia.org/wiki/List_of_Unix_utilities) exist and they're awesome.

To get the sum of a column in a huge text file, we can easily use [awk](http://en.wikipedia.org/wiki/AWK_(programming_language)).  And we won't even need to read the entire file into memory.

Let's assume our data, which we'll call _data.csv_, is pipe-delimited ( | ), and we want to sum the fourth column of the file.

```python
cat data.csv | awk -F "|" '{ sum += $4 } END { printf "%.2f\n", sum }'
```
The above line says:

1. Use the [cat](http://en.wikipedia.org/wiki/Cat_(Unix)) command to stream (print) the contents of the file to [stdout](http://en.wikipedia.org/wiki/Standard_streams).
2. [Pipe](http://en.wikipedia.org/wiki/Pipeline_(Unix)) the streaming contents from our cat command to the next one - awk. 
3. With [awk](http://en.wikipedia.org/wiki/AWK_(programming_language)):

	1. Set the field separator to the pipe character (-F "|"). Note that this has nothing to do with our pipeline in point #2.
	2. Increment the variable _sum_ with the value in the fourth column ($4). Since we used a pipeline in point #2, the contents of each line are being streamed to this statement.
    3. Once the stream is done, print out the value of _sum_, using [printf](http://www.gnu.org/software/gawk/manual/html_node/Printf-Examples.html) to format the value with two decimal places.

It took less than two minutes to run on the entire file - much faster than other options and written in a lot fewer characters.

[Hilary Mason](http://www.hilarymason.com) and [Chris Wiggins](http://www.columbia.edu/~chw2/) wrote over at the [dataists blog](http://www.dataists.com/) about the importance of any [data scientist being familiar with the command line](http://www.dataists.com/2010/09/a-taxonomy-of-data-science/), and I couldn't agree with them more.  The command line is essential to my daily work, so I wanted to share some of the commands I've found most useful.

For those who are a bit newer to the command line than the rest of this post assumes, Hilary previously wrote a [nice introduction to it](http://www.hilarymason.com/articles/intro-to-the-linux-command-line/).

### Other commands

#### [head](http://en.wikipedia.org/wiki/Head_(Unix)) & [tail](http://en.wikipedia.org/wiki/Tail_(Unix))

Sometimes you just need to inspect the structure of a huge file.  That's where [head](http://en.wikipedia.org/wiki/Head_(Unix)) and [tail](http://en.wikipedia.org/wiki/Tail_(Unix)) come in.  Head prints the first ten lines of a file, while tail prints the last ten lines.  Optionally, you can include the _-N_ parameter to change the number of lines displayed.

```python
head -n 3 data.csv
# time|away|score|home
# 20:00||0-0|Jump Ball won by Virginia Commonwealt.
# 19:45||0-0|Juvonte Reddic Turnover.

tail -n 3 data.csv
# 0:14|Trey Davis Turnover.|62-71|
# 0:14||62-71|Briante Weber Steal.
# 0:00|End Game|End Game|End Game
```

#### [wc](http://en.wikipedia.org/wiki/Wc_(Unix)) (word count)

By default, [wc](http://en.wikipedia.org/wiki/Wc_(Unix)) will quickly tell you how many lines, words, and bytes are in a file.  If you're looking for just the line count, you can pass the _-l_ parameter in.

I use it most often to verify record counts between files or database tables throughout an analysis.

```python
wc data.csv
#     377    1697   17129 data.csv
wc -l data.csv
#     377 data.csv
```

#### [grep](http://en.wikipedia.org/wiki/Grep)

[Grep](http://en.wikipedia.org/wiki/Grep) allows you to search through plain text files using [regular expressions](http://en.wikipedia.org/wiki/Regular_expression).  I tend [avoid regular expressions](http://regex.info/blog/2006-09-15/247) when possible, but still find grep to be invaluable when searching through log files for a particular event.

There's an assortment of extra parameters you can use with grep, but the ones I tend to use the most are _-i_ (ignore case), _-r_ (recursively search directories), _-B N_ (N lines before), _-A N_ (N lines after).

```python
grep -i -B 1 -A 1 steal data.csv
# 17:25||2-4|Darius Theus Turnover.
# 17:25|Terrell Vinson Steal.|2-4|
# 17:18|Chaz Williams made Layup.  Assisted by Terrell Vinson.|4-4|
```

#### [sed](http://en.wikipedia.org/wiki/Sed)

[Sed](http://en.wikipedia.org/wiki/Sed) is similar to [grep](http://en.wikipedia.org/wiki/Grep) and [awk](http://en.wikipedia.org/wiki/AWK_(programming_language)) in many ways, however I find that I most often use it when needing to do some find and replace magic on a very large file.  The usual occurrence is when I've received a CSV file that was generated on Windows and my [Mac isn't able to handle the carriage return](http://stackoverflow.com/questions/6373888/converting-newline-formatting-from-mac-to-windows) properly.

```python
grep Block data.csv | head -n 3
# 16:43||5-4|Juvonte Reddic Block.
# 15:37||7-6|Troy Daniels Block.
# 14:05|Raphiael Putney Block.|11-8|

sed -e 's/Block/Rejection/g' data.csv > rejection.csv
# replace all instances of the word 'Block' in data.csv with 'Rejection'
# stream the results to a new file called rejection.csv

grep Rejection rejection.csv | head -n 3
# 16:43||5-4|Juvonte Reddic Rejection.
# 15:37||7-6|Troy Daniels Rejection.
# 14:05|Raphiael Putney Rejection.|11-8|
```

#### [sort](http://en.wikipedia.org/wiki/Sort_(Unix)) & [uniq](http://en.wikipedia.org/wiki/Uniq)

[Sort](http://en.wikipedia.org/wiki/Sort_(Unix)) outputs the lines of a file in order based on a column key using the _-k_ parameter.  If a key isn't specified, sort will treat each line as a concatenated string and sort based on the values of the first column.  The _-n_ and _-r_ parameters allow you to sort numerically and in reverse order, respectively.

```python
head -n 5 data.csv
# time|away|score|home
# 20:00||0-0|Jump Ball won by Virginia Commonwealt.
# 19:45||0-0|Juvonte Reddic Turnover.
# 19:45|Chaz Williams Steal.|0-0|
# 19:39|Sampson Carter missed Layup.|0-0|

head -n 5 data.csv | sort
# 19:39|Sampson Carter missed Layup.|0-0|
# 19:45|Chaz Williams Steal.|0-0|
# 19:45||0-0|Juvonte Reddic Turnover.
# 20:00||0-0|Jump Ball won by Virginia Commonwealt.
# time|away|score|home

# columns separated by '|', sort on column 2 (-k2), case insensitive (-f)
head -n 5 data.csv | sort -f -t'|' -k2
# time|away|score|home
# 19:45|Chaz Williams Steal.|0-0|
# 19:39|Sampson Carter missed Layup.|0-0|
# 20:00||0-0|Jump Ball won by Virginia Commonwealt.
# 19:45||0-0|Juvonte Reddic Turnover.
```

Sometimes you want to check for duplicate records in a large text file - that's when [uniq](http://en.wikipedia.org/wiki/Uniq) comes in handy.  By using the _-c_ parameter, uniq will output the count of occurrences along with the line.  You can also use the _-d_ and _-u_ parameters to output only duplicated or unique records.

```python
sort data.csv | uniq -c | sort -nr | head -n 7
#   2 8:47|Maxie Esho missed Layup.|46-54|
#   2 8:47|Maxie Esho Offensive Rebound.|46-54|
#   2 7:38|Trey Davis missed Free Throw.|51-56|
#   2 12:12||16-11|Rob Brandenberg missed Free Throw.
#   1 time|away|score|home
#   1 9:51||20-11|Juvonte Reddic Steal.

sort data.csv | uniq -d
# 12:12||16-11|Rob Brandenberg missed Free Throw.
# 7:38|Trey Davis missed Free Throw.|51-56|
# 8:47|Maxie Esho Offensive Rebound.|46-54|
# 8:47|Maxie Esho missed Layup.|46-54|

sort data.csv | uniq -u | wc -l
#     369 (unique lines)
```

While it's sometimes difficult to remember all of the parameters for the Unix commands, getting familiar with them has been beneficial to my productivity and allowed me to avoid many headaches when working with large text files.

Hopefully you'll find them as useful as I have.


_Additional Resources:_

- [Explorations in Unix](http://www.drbunsen.org/explorations-in-unix/) by [Seth Brown](http://www.drbunsen.org/)
- [An Introduction to the Unix Shell](http://www.ceri.memphis.edu/computer/docs/unix/bshell.htm)
- [Data Analysis with the Unix Shell](http://blog.comsysto.com/2013/04/25/data-analysis-with-the-unix-shell/)
- [7 Command Line Tools for Data Science](http://jeroenjanssens.com/2013/09/19/seven-command-line-tools-for-data-science.html)