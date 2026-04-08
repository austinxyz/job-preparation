---
processed: true
experience_note: "[[experience/eBay - Resolving L7 Traffic Gap]]"
---

## Story
At eBay, my team had successfully built APIs that allowed our capacity team to automatically balance resources across Availability Zones for most applications. However, we faced a critical gap: a small set of applications handling public Layer 7 traffic remained unsupported by our solution. This wasn't just a minor oversight - these applications were crucial to eBay's core business, capable of significantly impacting site performance and revenue during traffic spikes. We needed to address this gap, but there were conflicting views on how to proceed.

As the tech lead, my task was to resolve a critical disagreement with my manager about how to handle these L7 traffic applications. My manager prioritized resource efficiency and wanted to apply our existing solution with minimal changes. However, my team and I were deeply concerned about site reliability, knowing these applications needed specialized handling during traffic spikes. I needed to find a middle ground that would maintain efficient resource management across Availability Zones while ensuring our solution could properly support these critical applications during high-demand periods.

I began by acknowledging my manager's valid concerns about resource efficiency and the potential cost savings of extending our existing solution. However, I knew we needed more data to make an informed decision. I took the initiative to collaborate with our network team, who had extensive experience handling L7 traffic patterns. Through these discussions, I discovered they had already developed a specialized tool for managing L7 traffic ramp-ups, which could complement our existing solution. This revelation led me to develop a two-phase workflow that would bridge both approaches. First, we would use our existing resource balancing system for normal operations, then automatically trigger the network team's L7 tool during high-traffic periods. To ensure consistent implementation, I created a detailed Standard Operating Procedure (SOP) documenting the workflow, including specific triggers and handoff points between the two systems. This approach would maintain the resource efficiency my manager prioritized while adding the specialized handling these critical applications required.

The results exceeded our expectations. We implemented the two-phase workflow solution within just one month, enabling us to add AZ workload and ramp up traffic for public L7 applications within a single day - a significant improvement from our previous timeline. Over the next three months, my team successfully completed the auto-rebalance solution for both private traffic and public L4 applications, creating a comprehensive system that addressed all our traffic management needs. Throughout this process, we maintained AZ resource usage between 40-80% efficiency, meeting my manager's resource optimization goals. Most importantly, we achieved our primary objective of ensuring site reliability for all application types while maintaining resource efficiency. The solution's success demonstrated that by carefully considering different perspectives and leveraging existing tools, we could find creative solutions that addressed seemingly conflicting requirements. This experience reinforced the importance of thorough research and cross-team collaboration in resolving technical disagreements.

## Raw Answers
What was the potential business impact if these public L7 traffic applications couldn't be rebalanced across AZs?

If there are traffic spike (like in holiday season) for these public L7 traffic applications, then we need to quickly add more AZs, otherwise, eBay users will have high latency to access ebay site and impact the user experience and impact the revenue.

Can you recall a situation where you faced a conflict at work?

Yes, I'd like to share the situation that I have different opinion with my manager on AZ rebalance project. At that time, team has completed the AZ ramp up and ramp down functions for major eBay applications , capacity team can use these API to balance the AZ resources. however still there are few applications with public L7 traffic, we can not support. Team and I want to continue to support such applications because public L7 traffic application could have a big impact for eBay site, if we can not do AZ ramp up/ramp down in urgent case, it may cause revenue impacts. However my manager disagree it.

Were there any measurable improvements in site reliability or resource efficiency after implementing both solutions?

With two phase workflow on public L7 traffic application, we can quickly add one AZ workload and ramp up traffic within 1 days, it promise the site reliability for any type of applications. and the AZ auto-rebalance, it will keep the AZ resource usage always keeps in 40%-80%.

What was your manager's reasoning for disagreeing with supporting these public L7 traffic applications?

My manager wants team to continue to do AZ auto-rebalance based on current AZ ramp up/down features. so team will have a well-control on AZ resources, although we can not support all applications, but by auto-adjusting current supported applications (private traffic and public L4 applications), we can make sure the AZ resource usage between high water mark and low water mark. the public L7 traffic applications are a small set of application, even we don't support it, we still can satisfy the resource efficient utilization goal.

How did you initially approach discussing your concerns with your manager?

I recognize my manager's goal, which is an efficient goal and could save costs and my goal is related with site reliability which will reduce the risk to have business impacts. Both of these are important.

What was the final outcome of implementing this two-phase workflow solution, both in terms of site reliability and resource efficiency?

Yes, in one month, team quickly build out this two-phase workload solution and verified by try-run and pilot for few application, it works. then team continue to focus on the auto-rebalance solution for private traffic and public L4 applications. team also support auto-rebalance in 3 months.

What specific steps did you take to find a resolution that would address both your concerns about site reliability and your manager's focus on resource efficiency?

My manager's concern is to support public L7 traffic application ramp up and down, it is complex, it is related co-work with network team, and current solution is not mature. however he agreed to the ramp up/down capability is important for site reliability. When I started to discuss with network team on the solution, I learnt they have a tool which could support the L7 traffic ramp up, then I found an intermediate solution, we will leverage on current ramp up and then add a step to do L7 traffic ramp up by their tool. In current stage, we can not support 100% automation, however we could have a SOP as 2-phase workflow to support it. the effort is not big and on the other hand, team could still focus on the efficiency goal.


