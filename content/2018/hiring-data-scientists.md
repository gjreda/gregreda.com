Title: Hiring Data Scientists
Date: 2018-02-04
Slug: hiring-data-scientists
Tags: data science, hiring, thoughts

Chicago's a big city that feels small -- everyone seems only a degree or two
away from one another. This feels especially true within Chicago's tech and data
science communities.

As a result, I occasionally get asked about hiring data scientists.
Specifically, how do you vet, hire, and evaluate a data scientist if you don't
have existing experience (either personally or within your company)?

While I feel this is a hard problem -- and one I never have a great answer
to -- I figured sharing how I think about hiring might prove helpful to others.

### How I think about it
My general belief is that so long as the candidate clears some
programming bar and some quantitative bar (neither of which should be too high),
the most important things for success are _**curiosity and skepticism**_.

The programming and quantitative bars should be based _**solely on examples of
work they'd do on the job**_.

I do this via a small take-home assignment that should take candidates a couple
of hours. The assignment asks variations of questions they are likely to encounter
in the role. A small dataset is provided, which the questions reference.

In my opinion, the programming and quantitative bars mostly come down to:

- Can they write code to do what they need to? Getting data out of a database, analysis at scale, automating some regular analysis, etc.

- Do they think from a quantitative perspective? Do they think probabilistically?

- Can they build a basic model and evaluate it? Do they understand statistics enough such that their analysis will not be _harmful_?

    - My belief is that _no data_ is preferable to _bad data_. With no data, you're forced to seek alternative forms of information (e.g. talking to users). With bad data, you risk drawing improper conclusions that lead you astray -- false confidence.

Assuming the candidate clears these bars, I believe curiosity and skepticism are the two most
important attributes for success.

If they are curious, they will continue to fill gaps in their knowledge, learn
new approaches to problems, and seek to continuously learn the business/product
side -- and how their work can add value to it. A data scientist that has a
tendency to go down rabbit holes can be a good thing if properly directed.

If they are skeptical, they'll refine everyone's
thought process by questioning things in a healthy way. They'll innately seek to
prove things believed to be true and they'll seek to answer questions
that arise -- be it via their own curiosity or others'. This skepticism also
acts as a check -- they'll seek alternative ways to prove and
test their own work, cautiously fearful of creating bad data that can lead to
improper action.

### My interview process

1. Phone screen with recruiter (30 mins)

2. Phone screen with me (30 mins)

3. Take-home assignment (~2 hours)

4. In-office interview (3 hours)

The phone screens are really about feeling the person out, learning about what they're
looking for next, and digging into specifics about their past experience/work.

The take-home assignment acts as the "programming and statistical bar" with
respect to the job -- brief examples of questions or problems they might work on
in the role. We ask candidates to provide any code they wrote or charts
they created to answer all questions, even if it's exploratory in nature. We
also ask that they be prepared to discuss their work during interviews.

My in-office interviews are three one-hour interviews. Usually, two one-hour
interviews with myself and my team, and a joint interview with a
product manager and platform engineer. Time is _always_ left for the candidate
to ask the interviewers questions.

I should note that depending on how tenured the candidate is and their existing
body of work, this process might change slightly. My approach tends to change when
candidates can point me to prior work (GitHub, side projects, blog posts).

If you’re looking for more details an ideal hiring process for data scientists, [Trey Causey’s advice is excellent](http://treycausey.com/hiring_data_scientists.html) and has influenced much of my thinking. Similarly, [Q McCallum](http://qethanm.cc/)’s series on [common data science hiring mistakes](http://qethanm.cc/2018/01/23/common-mistakes-in-data-science-hiring-part-1/) offers practical advice to determine whether you actually need a data scientist, and that you can hire and retain them. Finally, [Mikhail Popov](https://mpopov.com/)'s piece on [Wikipedia's approach to data science hiring](https://blog.wikimedia.org/2017/02/02/hiring-data-scientist/) is worth your time.
