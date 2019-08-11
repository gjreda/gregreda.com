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
Imagine we have the following dataset (you can find it [here](http://dmanalytics.org/wp-content/uploads/2014/10/chapter-12-relay-foods.xlsx)):

{% notebook notebooks/cohort-analysis.ipynb cells[1:2] %}

Pretty standard purchase data with IDs for the order and user, as well as the order date and purchase amount.

We want to go from the data above to something like this:

![example cohort chart](/images/cohort-example.png)

Here’s how we get there.

## Code
{% notebook notebooks/cohort-analysis.ipynb %}

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
