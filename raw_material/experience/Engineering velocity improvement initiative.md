---
processed: true
experience_note: "[[experience/eBay - Engineering Velocity Program]]"
---

## Story
While leading engineering teams at eBay, I faced a critical challenge with our application development speed. Our CI/CD pipelines were taking developers up to a week to complete - far too long for our business needs. This slow deployment process and difficult rollbacks were seriously impacting our ability to ship features and recover from incidents quickly, directly affecting our revenue. To address this, I initiated a large-scale engineering velocity program that required coordinating across 10+ development domains, 5 cloud infrastructure teams, and 3 platform teams. The complexity and business impact made this a high-stakes initiative.

As the Cloud Application Lifecycle Management team manager, I was tasked with leading a comprehensive infrastructure improvement initiative. My specific responsibility was to coordinate between multiple teams - from cloud infrastructure to security - and drive our deployment metrics to meet aggressive targets. I needed to ensure deployment completion within one day, enable on-demand frequency, achieve sub-hour rollbacks, and maintain a 95% success rate across 65% of our applications. Additionally, I had to guarantee infrastructure reliability above 99% while keeping deployment times under 60 minutes for our largest applications. The scope and complexity of these requirements demanded strong technical leadership and cross-team collaboration skills.

As the primary contact for cloud infrastructure, I took a systematic approach to address our deployment challenges. First, I conducted a thorough analysis of our metrics to identify key reliability bottlenecks and performance improvement opportunities. Based on this data, I developed a phased implementation strategy that would allow us to make incremental progress while maintaining system stability.

I recognized that security policies were a major factor in deployment delays, so I led an initiative to segment our applications into three categories based on their security requirements. This categorization helped us identify quick wins - applications with no security policies or simple requirements could be optimized immediately. I personally mediated discussions between our CD pipeline team and security team to reach a compromise that balanced speed with security concerns.

For the immediate term, I prioritized improvements for applications with minimal security requirements, which gave us early wins and built momentum. Simultaneously, I collaborated with our security team to architect a long-term solution for integrating complex security policies more efficiently into our deployment process. This balanced approach allowed us to show quick progress while developing a sustainable solution for our more complex applications.

Through this systematic approach and cross-team collaboration, we achieved significant improvements in our deployment metrics. Most notably, we reduced our 95th percentile deployment duration by 20% to 75 minutes for standard applications, excluding those with complex security requirements. The development teams particularly appreciated our balanced strategy - they saw immediate benefits from the quick wins while knowing we were working on a comprehensive solution for security-sensitive applications. My leadership in coordinating multiple teams and maintaining steady progress earned recognition from senior management. While the integration of our solution for large security applications is still in progress, we've established a strong foundation and clear path forward. This experience reinforced the importance of taking a data-driven approach to problem-solving while balancing short-term wins with long-term strategic improvements. It also highlighted how effective cross-team collaboration and clear communication can drive significant infrastructure improvements, even in complex technical environments.

## Raw Answers
Describe a situation where you exhibited leadership.

There is an engineering velocity program to improve the eBay developer productivity, the program is very complex and requirement infrastructure teams, platform teams and application development teams's cooperations. As the manager of Cloud Application lifecycle management team, I focus on improving Cloud infrastructure reliability, performance and supporting new functions - like blue/green deployment. I need to coordinate with multiple teams, internally work with Cloud app, fleet, network and security teams and externally work with platform, ebay cd team and different application development teams.

What feedback did you receive from the development teams and leadership about the impact of these improvements on their work?

development teams feel happy that we balanced the current solution and long term solution and they could not do waste efforts if we do large invest on current solution. leadership team is happy that I focus on major infrastructure blocks and coordinate multiple teams and keep making progress to improve the velocity

Can you walk me through a specific example of how you helped resolve a disagreement between engineering leads about a solution?

One example is about to improvement the application deployment duration. there are security related applications, when the deployment was happened, since pod will be recreated, need to setup security rules (policy) during initialization. current the performance is not good, particular for large pools. The cloud security team is working on a new generation of policy solution. however it takes time and can not help the performance improvement immediately. cd pipeline team tech lead wants to have a quick solution for current policy initialization while cloud security team tech lead wants them wait for a while and integrate with new version. I can understand both of them, and I analysis more details, there are different types of applications - application without security policy, small application with security policy and large application with security policy. in fact the percentage of large application with security policy are not big - about 5%, and there are easy way to improve the small application with security policy, then finally we have agreement, we can improve velocity by phases, in early stage, focus on application without security policy and security team will improve the small app policy initialization and buy time to switch to new solution and have integration with cd pipeline team after that.

What was the size and composition of the teams involved in this program, and what was your direct team's role?

Almost all eBay's development teams (10+ focus domains), cloud infrastructure teams (5 teams) and platform teams (3 teams) are involving this program. My role is as contact person from cloud infrastructure teams. I coordinate with platform teams and development teams, figure out the major blocks from infrastructure teams. worked with internal infrastructure teams and make sure we deliver the enhancements in time.

What specific responsibilities and decisions were you personally accountable for in driving this velocity improvement program?

Multiple components in cloud infrastructure could impact the development velocity. Based on the metrics, we identified the key reliability issues and improvement for performance. Then I need to coordinate with related teams to make sure the improvement to deliver in time with high quality. Sometime the solution could relate with multiple team's co-works, engineer leads may have different ideas and I help them have agreements with feasible plans.

What were the specific reliability and performance metrics you were trying to improve, and what were the target goals?

There are DORA metrics, including the deployment duration, deployment frequency, rollback duration and success rate. Our goal is to make sure 65% of applications (mainly for most frequent deployment applications) to reach elite (deployment duration within one day, frequency - on demand, < 1hour rollback and >95% success rate). As infrastructure, we make sure the infrastructure reliability > 99% and high performance for provision and deployment (60 mins for 95-percentile large applications)

When did this engineering velocity program take place, and what specific challenges was eBay facing that led to its creation?

When the program took place, the main challenges is the velocity of eBay application development is slow. developer may take 1 week to complete the ci/cd pipeline when they submit code into release branch and sometimes, it is hard to do rollback. It blocked the eBay's business growing and also it increase the incident recovery time which cause revenue lost.

What were the specific outcomes and improvements in deployment metrics after implementing your phased solution?

Now the 95% percentile application deployment duration is improved 20% to 75 mins excluding the large security applications. and the large security application solution is under integration.