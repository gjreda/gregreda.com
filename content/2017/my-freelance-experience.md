Title: My Experience as a Freelance Data Scientist
Date: 2017-01-07
Slug: freelance-data-science-experience
Tags: data science, thoughts, freelance

Every so often, data scientists who are thinking about going off on their own will email me with questions about my year of freelancing (2015). In my most recent response, I was a little more detailed than usual, so I figured it'd make sense as a blog post too.

If my response comes across as negative, that's certainly not the intention -- being straight-forward about my experience is.

I learned a lot, it just wasn't for me. Working by yourself on short(ish)-term things can get old.

### How was your year of freelancing?
Generally, it was good and I learned a lot.

My reason for setting out on my own was really about scratching an itch I've always had (and I suspect many of us have) - can I strike it out on my own?

The freedom was really nice and if you're able to find the work, you can likely work less than you would full-time while making more money. That said, it's certainly not for everyone.


### Why'd you stop?
I didn't find it very rewarding in a non-monetary sense.

Freelancing/consulting doesn't really give you the luxury of thinking long-term about something like a product company does. Typically, a client hires you to do something, you do it, and then you're gone.

Thinking long-term and deeply through all the ways data / data science can be impactful upon a business or product is something I really enjoy -- "ohh, we can build a recommendations engine with this ... the search results we're displaying to the user here aren't great -- we can use this data to improve them, etc." I definitely enjoy a more of a slant towards data scientist + product manager than I do data scientist + software engineer.

As an individual freelancer, landing this sort of "feature" work is very hard because:

1. You're one person and typically these are not small projects. You only have so much capacity (24 hours/day), so it'd take more time for you to do it than it would a team.

2. Companies often want these things to be a "core competency" in that they do not want someone to build Big Important Thing and disappear. They are risk-averse.

3. You didn't strike out on your own to build Big Important Thing and then really just maintain that thing for one client in perpetuity (which would likely happen if the company allowed you to build it) -- you started freelancing because you (presumably) wanted some variety.

Companies often have a Thing In Mind they want you to do -- or, they want to "buy" your time for some period (e.g. 80 hours over the next three months at $/hour -- a retainer).

When they have a Thing In Mind, it is much more likely to be dirty work that they do not feel is the best use of their existing team's time than it is to be something they need you, the consultant, for.

When on retainer, I found the experience to be similar, except it can be a bunch of ad-hoc tasks that come up ("can you pull this data for me") that you didn't know would be the case when you signed the contract.

This is all a long way of saying, in my experience, _a non-trivial portion of you has to be ok with being a mercenary_ -- do the thing you're being paid to do and not worry about the rest.

I struggled with that internally and thus did not find the work very stimulating -- I like buying into something, giving it my all, and thinking about the various directions it can be taken.


### Tips or lessons learned?
So many, but here are a few:

#### [Keep It Simple, Stupid](https://en.wikipedia.org/wiki/KISS_principle)
This isn't specific to freelancing per se, but it was something freelancing emphasized.

I think data scientists (generally) have a bad habit of latching onto specific words a stakeholder says, while ignoring the other words in the request.<sup>1</sup> For example:

> "What's the optimal number of leads that a rep should get? We want to get directionally better."

As data scientists, we hear "optimal number" and we start thinking about doing complex math and building models. We end up ignoring the most important part: "We want to get directionally better" -- our stakeholder is telling us "we don't know much about this right now -- help!"

We need to start simple -- maybe some basic exploratory work + charts -- and surface that back to our stakeholder, giving them the opportunity to say "cool, this is all I needed" or "this is good, but keep going." We need to allow our stakeholder to choose incremental progress and we should not assume they need the more complex (and time-intensive) solution.

#### Try to get systems access before the project begins
This probably isn't a high priority for the systems team at your client. Thus, if the process of getting you access to things (databases, vpn, etc.) starts the same day the project is set to start, the first day or two will wind up being a waste of time.

#### Productized consulting
Nail down exactly what you do or create. Have a fixed price for doing it. Don't deviate from that. Turn your "consulting" into a product.

For example, you'll build a churn model for $XX. My brother's company is a [good example of this](https://ethercycle.com/pricing/).

Try not to sell hours. Which leads me to ...

#### Don't bill hourly
Tracking hours sucks and also limits your margin. Try to sell daily or weekly rates (or productized consulting).

Better yet, if you have a well defined scope (ideal, but sometimes hard) and you know the amount of time the project will take you, then set a price on the project. The risk here is the project taking longer than you anticipated and now you're really just doing free work.

I was fearful of underestimating the amount of time something would take me, so I billed hourly. It wasn't fun though. Additionally, all of my clients ended up being retainers.


### My biggest fears involve health insurance. Do you have any good resources?
Not really. I just used healthcare.gov and went with a BCBS PPO because I'm pretty risk-averse.


### In the data science pipeline, where did your services fall (e.g. Databases > Data Cleaning > Business Intelligence > Advanced Analytics)? Did you do everything?
This was something I should have been better about -- I never really established what my services were. My thesis in going freelance was more about feeling there was a gap in the data consulting market.

My belief was that there was (in 2015 ... and probably still is) a population of companies trying to figure out how to utilize their data, who are not interested in bringing on a consulting firm ($$$), and don't necessarily know if they need a data scientist full-time yet. I felt uniquely positioned to fill that gap due to being GrubHub's first data hire and also having prior consulting experience (PwC, Datascope).

For the reasons mentioned in the second question, I'd classify most of the work I ended up doing as Business Intelligence, along with some product/marketing analytics work -- instrumentation, how to think about using the data, etc -- but never in a "building data-driven features/products" sense. No machine learning or similar.

<hr class="small" id="footnotes"></hr>
1. I have a longer post about this in the works.
