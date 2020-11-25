title: newbird: a theme for pelican
slug: newbird-pelican-theme
date: 2020-11-25
tags: python, pelican

In 2014, I [wrote a custom theme](https://github.com/gjreda/void) for [Pelican](https://blog.getpelican.com/), the static site generator I use for this site.

At the time, there were few themes available and I wanted something that was fairly simple in its design, but also that I understood well enough to tweak as necessary. I opted to use [Skeleton](http://getskeleton.com/) for the theme's general structure, but also added a [fair amount of custom CSS](https://github.com/gjreda/void/blob/master/static/css/void.css) to get things the way I wanted.

But over time all that custom CSS became more of a pain than it was worth. I wanted something I could just drop in and have it look nice.

Yesterday I came across [new.css](https://newcss.net/), which I feel achieves its goal of sensible design and [classless CSS](https://blog.usejournal.com/the-next-css-frontier-classless-5e66f3f25fdd). It allowed me to quickly create a new Pelican theme with limited CSS-fiddling.

The new theme, which I've named [newbird](https://github.com/gjreda/newbird-pelican-theme), includes support for Google Analytics, [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards), and [Facebook Open Graph](https://developers.facebook.com/docs/sharing/webmasters/). It also allows for articles to be written in Jupyter Notebooks thanks to Pelican's liquid tags plugin. Notably, I opted not to include any social sharing buttons in order to decrease clutter and page loads.

If you're interested in using newbird for your Pelican-based site, you can find it [here](https://github.com/gjreda/newbird-pelican-theme).
