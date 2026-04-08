---
processed: true
experience_note: "[[experience/eBay - Cloud Infrastructure Team Turnaround]]"
---

## Story
Last year, I stepped in to manage a cloud infrastructure team of seven engineers that had been without leadership for several months. The situation was critical - we were experiencing severe reliability issues, including a recent 24-hour API server outage that impacted our customers. System reliability had dropped below 90%, and we were dealing with frequent critical incidents. The constant firefighting and stream of customer complaints had taken a heavy toll on team morale. I knew I needed to act quickly to stabilize both our systems and the team.

My immediate task was to lead a comprehensive turnaround of both our technical infrastructure and team dynamics. I was responsible for developing and executing a strategy to bring our system reliability back above 99%, while simultaneously rebuilding team confidence that had been shattered by months of constant firefighting. Senior leadership tasked me with addressing the mounting customer complaints about our service stability. Additionally, I needed to implement fundamental structural changes to prevent similar crises in the future. The challenge wasn't just fixing immediate issues - I had to transform how the team operated.

I began by conducting in-depth discussions with our key customers to understand their specific pain points and establish clear service level objectives. Based on these insights, I focused our team's efforts on two critical initiatives: upgrading our API server infrastructure and implementing SRE best practices. I developed a phased approach for the API server upgrade, starting with a comprehensive testing environment to minimize risk. Throughout the process, I maintained regular customer engagement to ensure our solutions aligned with their needs.

Rather than dictating solutions, I empowered my engineers by asking probing questions that guided them toward robust technical approaches while building their confidence. When an engineer proposed an innovative caching solution for our API endpoints, I helped them refine the idea through technical discussions and supported their ownership of the implementation.

To prevent future issues, I established regular retrospectives where we analyzed incidents and identified improvement opportunities. I made sure to recognize team achievements both internally and externally - celebrating wins like achieving our first month of 99.9% uptime helped rebuild team confidence and reinforce positive momentum.

Within three months, we achieved remarkable improvements across all key metrics. Our system reliability jumped from below 90% to consistently above 99%, meeting our target SLAs. More importantly, we dramatically reduced our incident recovery time - what previously took over 24 hours now took less than one hour to resolve. The implementation of SRE best practices led to a significant decrease in critical incidents, from multiple per week to rare occurrences. Our customers noticed the difference - within two months, we received positive feedback about our improved stability and responsiveness. One customer specifically commended our transparent communication during the transformation. The structural improvements we put in place, including automated testing, comprehensive monitoring, and incident response protocols, created a sustainable foundation for long-term reliability. But perhaps most rewarding was seeing the team's renewed confidence and engagement. They shifted from constantly reacting to problems to proactively identifying and addressing potential issues. This experience reinforced my belief that technical challenges often require both infrastructure improvements and cultural changes to create lasting solutions.

## Raw Answers
What specific challenges did you face in getting buy-in from the team for these two focus areas?

Team has concerns to do upgrade, it will increase risks with lots of verification/testing works. also Team has no confidence on how SRE best practice help on reliability and reduce incidents.

What specific improvements in system reliability and team performance did you observe after implementing these changes?

The system reliability used to <90% with critical incidents, system was down > 24 hours, now it keeps >99% and very few incidents and it could be recovered within an hour.

How did you specifically help the team overcome their concerns about the API server upgrade and SRE best practices implementation?

1. I asked team to do upgrade version by version, not complete all upgrade, split as phases, and do a minor version upgrade with enough testing. upgrade to testing/staging environment at first. 2. For SRE best practices onboarding, at first we identify the key non-functional requirement and checked with customer what kinds of metrics are most important SLO. We start the most important one at first.

How did you personally support and guide the team through the implementation of these changes while maintaining their motivation?

1. I trusted them and let them provide solution. however I asked questions to check if their solution could resolve the major customers' pain point. 2. I allowed team to make mistakes, but we keep on retrospective and learnt from mistakes 3. when team made progress, I recognized their works, internally and externally

What were the two major projects you decided to focus on, and why did you choose these specifically?

I decided to pick api server upgrade and onboard SRE best practices for api server. With new version upgrade, I can use new features which will support customer's requirement. and SRE best practices onboarding, it will mainly focus on improving the system reliability and reducing the incidents.

Can you recall an experience where your adaptability was crucial in navigating through a situation?

situation: I became the manager to manage a new team, fleet and core team. the team has no managers for several months, team members are self-driven but the results were not good, there were several critical incidents and several projects got big delays. I talked with key customers, understood what were the main customer pain points. I focus on 2 major projects, and discussed with key engineers. I share why the things were important, but left engineer to provide how. I trusted them and provided enough support to let them just focus on these 2 projects and keep engaging customer to make sure we are on right track. with 2 months, team made significant progress and earn the customer's confidence.

When did this transition happen, and what was the size and scope of the team you were taking over?

team has 7 developers and they were mainly working on cloud infrastructure

What were the specific critical incidents that the team was facing when you took over?

the cloud infrastructure includes api server, one major development api server got down > 24 hours. most of developers got impacted

What was the state of the team's morale and collaboration when you took over as their manager?

team felt really depressed, they were busy on fire flighting, but still there were lots of customer complains