Title: Nonsensical beer reviews via Markov chains
Date: 2015-03-30
Slug: beer-review-markov-chains
Tags: beer, text, markov chain
Description: Introducing BeerSnobSays: a bot that tweets nonsensical beer reviews generated via Markov chains.

I’ve had a bunch of beer reviews and ratings data sitting on my hard drive for about year. For a beer nerd like me, that’s a pretty cool dataset, yet I’ve let it collect digital dust.

Fast forward to last week, where somehow I wound up in the Wikipedia Death Spiral. You know what I mean - you click a link to a Wikipedia article, that article takes you to a new one, then you’re on another, and another … we’ve all been there. And it’s kind of awesome.

Well, the rabbit hole led me to [Markov chains](http://en.wikipedia.org/wiki/Markov_chain), which seemed like a good excuse to mess around with that beer review data.

## What are Markov chains?
Markov chains are a random process that transitions to various states, where the “next state” is based on its probability distribution, given the current state.

Imagine we have the following sequence of days, where S indicates it was sunny and R indicates it was rainy:

> S S R R S R S S R R R R S R S S S R

Let’s pick a random beginning “state” - let’s just say it’s S (sunny). The next state is based **only** on the current state. Since our current state is S, we only need to look at observations immediately following a sunny day.

To illustrate, let’s look at the weather pattern again, this time putting the observations to be considered in bold.

> S **S** **R** R S **R** S **S** **R** R R R S **R** S **S** **S** **R**

Even though there are 18 observations, only nine need to be considered for the possible next state. Of the nine, four are S and five are R, giving us a 44% (4/9) chance of the next state being sunny and a 55% (5/9) chance of it being rainy.

Now, let’s assume our beginning state (S) transitioned to a second state of R (which it had a 55% chance of doing). Here are the states we need to consider for the possible third state:

> S S R **R** **S** R **S** S R **R** **R** **R** **S** R **S** S S R

There’s an equal chance (4/8) the third state will be S or R.

With a second-order Markov chain, the current state is two observations. Let’s assume a beginning state of SR and use the same weather sequence as above, again putting the possible next states in bold.

> S S R **R** S R **S** S R **R** R R S R **S** S S R

This time there are only four observations to consider as possible “next states,” with an equal chance it’ll be S or R.

Let’s assume the “next state” picked is R. Now our current (second) state is RR - the S from our beginning state is forgotten. The following are possible third states:

> S S R R **S** R S S R R **R** **R** **S** R S S S R

Again, there’s an equal chance of our third state being S or R.

We can continue picking “next states” and eventually we’ll have generated a random, yet probabilistic sequence of weather.

These same principles can be used to generate a sentence from text data - pick a random beginning state (word) from the text and then pick the next word based on the likelihood of it occurring, given the current word. A first-order Markov sentence would have a one word current state, a second-order would have a two word current state, … and so on.

The larger the corpus and the higher the order, the more sense these Markov generated sentences make. Good thing I have a lot of beer reviews.

## The (mini) project
This seemed ripe for a Twitter bot, so I created [BeerSnobSays](https://twitter.com/BeerSnobSays), which tweets nonsensical beer reviews generated via second-order Markov chains.

Not everything it tweets makes much sense:

> dissipates about a finger of head and some mild spice interwoven and even beer at a local Greek restaurant.

> a big thumbs up though and there are plenty other choices that I was really no distinguishing characteristics that stand out.

> those who are looking for a beer best characteristic of this beer into the hype and the lager style that is unwelcome.

But some of it is pretty funny:

> off by itself, the taste of apple juice colored brew with a nice warming alcohol bathes your noodle in its dryness.

> is almost like sour grains with a hint of booze in the finish, with sweet orange peels and pine sap.

> a charred woodiness and smoke can run into pineapple, oranges and citrusy oils with a clean alcohol sting at the bottom of the recipe.

> the berry aspect is evident but the tartness and dryness from the beer starts off surprisingly pleasant.

I’m not sure if that last one’s from the bot or a famous poet.

You can [follow me](https://twitter.com/gjreda) and [BeerSnobSays](https://twitter.com/BeerSnobSays) on Twitter. You can also find the code for the bot [on GitHub](https://github.com/gjreda/beer-snob-says).