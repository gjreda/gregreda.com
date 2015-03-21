Title: How random is JavaScript's Math.random()?
Date: 2013-06-30
Slug: testing-javascripts-random-function
Tags: scraping, python, tutorial, data

A few weeks back, I was talking with my friend [Molly](http://mollybierman.tumblr.com) about personal domains and realized that her nickname, Bierface, was available.  The exchange basically went like this:

> Me: I should buy bierface.com and just put up a ridiculous picture of you.

> Molly: You would have to do a slideshow. Too many gems.

[So I did just that](http://www.bierface.com), switching randomly between 14 pictures every time the page is loaded.  The laughs from it have been well worth the $10 spent purchasing the domain.

She started to question the randomness though.  Here's what the code that loads each image looks like:

```html
<a href="http://mollybierman.tumblr.com">
  <img id="bierface" src=""/>
</a>
<script type="text/javascript">
  var n = Math.ceil(Math.random() * 14);
  document.getElementById("bierface").src = "./pictures/"+n+".jpg";
</script>
```
All we're doing is creating an empty _`<img>`_ element, and then changing the src attribute of that element via JavaScript.  The first line of JavaScript uses a combination of [Math.ceil()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/ceil) and [Math.random()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random) to get a random integer between 1 and 14 (which are how the images are named).  The second line uses that integer to create a file path and tells our _`<img>`_ element to use that path as the src for the image.

Since the image is loaded by your web client, this seemed like a great opportunity to learn the very basics of grabbing client-side data - I could write some code to repeatedly get which image was loaded in order to determine how random _Math.random()_ truly is.

#### The Setup
We're going to be using [Ghost.py](http://jeanphix.me/Ghost.py/) to simulate a [WebKit](http://en.wikipedia.org/wiki/WebKit) client.  Ghost.py requires [PyQt](http://en.wikipedia.org/wiki/PyQt) or [PySide](http://en.wikipedia.org/wiki/PySide), so you'll want to grab one of those, too.  I'm on OSX 1.8.2 and using PySide 1.1.0 for Python 2.7, which you can get [here](http://qt-project.org/wiki/PySide_Binaries_MacOSX).  You'll also need to grab Qt 4.7, which you can find [here](http://packages.kitware.com/item/3736).

#### The Code
With a little Python and Ghost.py, we can simulate a browser, allowing us to execute JavaScript telling us which image was loaded.  We can also use [matplotlib](http://matplotlib.org/) to plot the distribution.

```python
from ghost import Ghost
import matplotlib.pyplot as plt
import os

ghost = Ghost()

# JavaScript to grab the src file name for the image loaded
js = "document.getElementById('bierface').src.substr(33);"

# initialize zero'd out dictionary to hold image counts
# this way we can draw a nice, empty, base plot before we have actual values
counts = dict(zip(range(1, 15), [0 for i in range(1, 15)]))

for i in xrange(1, 1002):
    # draw empty plot on first pass
    if i != 1:
        page, page_resources = ghost.open('http://www.bierface.com')
        image = ghost.evaluate(js)[0]
        image = int(image.split('.')[0]) # grab just the image number
        counts[image] += 1

    plt.bar(range(1, 15), counts.values(), align='center')
    plt.xticks(range(1, 15), counts.keys())
    plt.xlabel('Image')
    plt.ylabel('# of times shown')
    plt.title('n = {0}'.format(str(i-1).zfill(4)))
    plt.grid()

    path = '{0}/images/{1}'.format(os.getcwd(), str(i).zfill(4))
    save(path, close=True)

os.system('ffmpeg -f image2 -r 10 -i images/%04d.png -s 480x360 random.avi')
```

Let's walk though the code:

1. Load our libraries and create an instance of the Ghost class.
2. Store the JavaScript we'll need to execute in order to grab the image file name into a variable named _js_.
3. The comment should explain this one - we're initializing a zero'd out dictionary called _counts_ so that our first plot doesn't have an x-axis with just one value.  Each key of the dictionary will correspond to one of the images.
4. The [for loop](http://docs.python.org/2/reference/compound_stmts.html#for) is used to run 1,000 simulations.  My [xrange](http://docs.python.org/2/library/functions.html#xrange) usage is a little wacky because I'm using it to title and name the plots - typically _xrange_ starts with 0 and runs up _until_ the number specified (e.g. 1,001 will be the last loop, not 1,002).
5. This is the section that grabs which image was loaded by simulating a WebKit client with Ghost.py.  This section does not get run on the first pass since we want to start with an empty plot.

    1. Load bierface.com into our _page_ variable.
    2. Execute the JavaScript mentioned in #2 and store it in the _image_ variable.  Remember that this will be a string.
    3. Split the _image_ string so that we just grab the image number loaded.
    4. Update our dictionary of counts for the given _image_.

6. Here we're using [matplotlib.pyplot](http://matplotlib.org/api/pyplot_api.html) to draw a bar chart.  Thanks to [Jess Hamrick](http://www.jesshamrick.com/) for some awesome [plot-saving boilerplate](http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/), which I'm using behind the _save_ function.
7. Finally, use [ffmpeg](https://en.wikipedia.org/wiki/FFmpeg) to stitch our plots together into a video.

#### The Results
_Math.random()_ is pretty random (though #7 is the clear loser in the video below).  It's easy to think it's not when working with a small sample size, but it's clear the numbers start to even out as the sample size increases.

<center><iframe width="480" height="360" src="//www.youtube.com/embed/y-tRXCyBk4w" frameborder="0" allowfullscreen></iframe></center>