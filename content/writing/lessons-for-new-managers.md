Title: Lessons for New Data Science Managers
Date: 2019-04-27
Slug: lessons-for-new-data-science-managers
Tags: data science, management, thoughts
Status: Draft

I've had this post sitting in draft for a long time -- basically ever since I become a Director in October 2018. I've found myself thinking about it quite a bit recently, so I figured it was time to get it out into the world.

Part of this is me writing it for my own sake, something for me to come back to when I'm struggling with something. To remember what I've learned. To read this and regain trust in myself and my decisions.

This post should otherwise be known as "Mistakes I've Made."

### Delegating
Delegating is hard and doesn't feel natural.

When your team is small, delegating is as simple as having a conversation with the person next to you. The problem doesn't have to be very fleshed out because you're next to them and can just talk any issues through.

As your team grows though, the conversation based approach doesn't scale and written communication becomes more important. A project management tool like Jira becomes necessary, as does weaving something like design docs into your team's process for sufficiently sized work. We found that our design docs tended to be a less implementation focused and more approach focused: problem statement, goals, assumptions, scoping (in and out), and some ideas of approaches to spike on.

I think it's also important to note that delegating can feel weird in the beginning -- that you're telling someone what to do. But over time you that delegating is also giving someone direction.

Make sure the team knows what is most important to work on, and who is responsible for which task.

### Stay out of the critical path
Managing can be difficult and draining, especially if you are naturally an introvert.

Sometimes you might find yourself just wanting to write some code. In my experience there's nothing wrong with this, but when doing so, it is critical that you do not write code that is in the team's critical path. As a people (and sometimes project) manager, it's common for you to be pulled in many directions. Because of this, you shouldn't be picking up tickets from the board that need to get done in a timely fashion. You should be looking for opportunities to create leverage for your team -- maybe you can refactor some area of the code, or make the team's test/build process a bit easier. Or maybe you can ...

Code you write should be a "nice to have" -- it should seek to make things better for you, the team, or others, but it should not be something that is mission-critical. You should be delegating that to your team.

### Implementing Process


### Creating Space


### Employee Growth
Growth is not monotonic, nor is it linear. It oscillates around some true distribution, with the overall trendline more closely matching an exponential growth rate. In the beginning, growth is hard to come by -- you are learning a lot of new skills, terms, and things. The flywheel is turning slowly. But eventually, if you keep learning, everything eventually starts to click. The flywheel catches momentem. The exponential growth curve excelerates greatly -- everything comes together. Eventually though, you reach a new level, a new plateau, a new role, and growth will be slow to come by for a while again. So you just keep working and learning, comsuming all you can. Trying and failing. And then eventually, you hit that gradient again, and growth excellerates exponentially again.

### Team Hype Person


### Feedback Mechanisms
The IC Feedback Loop is much shorter and easier to understand -- code works or it doesn't -- this combats our Impostor Syndrom. The Manager Feedback Loop is _brutal_ -- you might never realize results, or they might take a long time -- so long you forgot. Imposter Syndrome abounds. It's important to find ways to shorten this feedback loop -- your boss and mentors are helpful. Get their opinions, seek advice on how you're approaching something with the team.

Because of this, part of you will probably always consider getting back on the IC path. It happens to all of us. It's important to carve out some time each week to still scratch this itch, be it writing your own code or pairing with one of the more junior members of your team.

Trust in your decision making process. Almost like poker -- if you shoved your chips with the better odds, don't beat yourself up when it doesn't work -- you're playing the long game and will win over many hands.


### Patience

When your team is small, delegating is just a conversation with the person next to you. The problem doesn't have to be fleshed out because your next to them and can just talk about it. 

Delegating is weird, but people would rather have something to do than nothing to do. It's also an investment without an immediate payoff. Think of it like a SaaS company -- when acquiring a customer, your return is surely negative. However as their LTV grows, so does your business / revenue. As long as your LTV/CAC is positive, you're in good shape.

As your team grows, this doesn't scale, and written communication because more important - clear and thorough jira stories, outlining rationale and proposals on a wiki, etc. 

Infra is critical, as is basic Analytics within the org. But you only have so many "internal tokens" before you need to show value. Don't spend all your tokens too early. At some point you're going to have to show off a sexy model because that's why they're paying you. Build it and get it working and right knowing you'll likely need to revamp it later when your infra is more fleshed out. 

Balancing being a technical team lead and people manager is hard.

It's ok to put yourself first sometimes. As a new manager, you might have a tendency to put the team's needs always above your own -- I know I did. The team is more important that any individual. But without some selfishness and care for yourself, you'll find yourself stressed and run the risk of burn out. You were technical once. You probably still enjoy doing a little of that. You have problems of your own that you need to work on solving -- managerial ones -- sometimes you need sign off of Slack, hide in an office, and work on what you need to do.

Figure out what you're not going to do.

"You don't approach and breakdown managerial problems the way you do technical problems. Your mind doesn't seem to process them the same way."

Hiring and developing great people is the most important part of your job (and offers the best return on your time).





Optimize for inter-team learning -- DS can often work on a problem individually, thus everyone on the team is focusing on a different thing. This works for a while, but will not scale. It will also leave folks feeling isolated, increase their own imposter syndrome, inhibit growth, and lead to silo'ing of work -- de facto "owners." Don't allow for this long term -- pair people together on projects. Maybe this will decrease your team's throughput, but it will increase their satisfaction and increase the quality of their work. It will also ensure you have some defense against an individual being out or leaving.

Sometimes you need to make changes — structural, personal style, etc — state the change and why you’re making it - the problem you’re trying to solve - explain he historical context of why things were the way they were in the first place, and again explain why you think the problem got created and how you think this will solve it. 

I’ve had to do this with canceling some of our recurring team meetings. I’ve had to do this when changing my management style from democratic to directing - focusing more on execution than consensus. Consensus is good when you’re small (less than 5), but as you grow it stops working. Someone needs to me in charge and ensure decisions and progress are being made. 

#### Promoter in chief
Let's face it, Data Science teams, especially in smaller organizations (less than 1000), can very easily find themselves positioned in a very tough spot. _Every_ department or team within the organization could use data in their job, and it is very likely they have never had access to all the data that might be useful to them (think customer usage data). Now, there's a data science team that can get it all for them (no).

I've found that organizations around DS teams grow at a much greater rate than DS teams. And that DS teams scope expands over time -- "special projects" at first, then data infrastructure, then data warehousing, then basic analysis, maybe mix in some internal applications (custom web apps/dashboards), some core infrastructure (instrumentation systems), maybe the company will start doing A/B testing.

Eventually, you find yourself in a position where you "can't win." Someone is always looking for something that you can't (or shouldn't) deliver on, that you have to push back on. Generally, this will leave you feeling shitty, because you want to be helpful. It also runs the risk of others in the organization wondering "what exactly do you do here."

Eventually, as a Director, you might find that your role turns into the Promoter-in-Chief of your team. As data scientists, we generally aren't great marketers or salespeople of our work, despite the fact that it might have global applicaability. We just want to build more stuff, or attack the next problem, not spend a bunch of time marketing our work. This is wrong, and someone needs to do it.

I've started to do bi-weekly Release Notes, as I've found that others didn't necessarily know about all the great work that my team was doing, mainly because the org had gotten so large that it was impossible for everyone to know, and to combat the idea that we _weren't_ doing things that people thought we should be doing. I decided that I needed to communicate that we are instead attacking larger, higher level problems, and buildng more general things that can hopefully be utilized by a wider set of stakeholders.


Additional Resources:
- http://firstround.com/review/our-6-must-reads-for-first-time-managers-to-hit-the-ground-running/
