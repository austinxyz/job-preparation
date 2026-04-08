---
processed: true
experience_note: "[[experience/eBay - Automated Cluster Management Overhaul]]"
---

## Story
As the lead engineer on our cloud fleet team, I was responsible for managing the lifecycle of over 20 diverse clusters annually - everything from cloud control planes to Hadoop systems. Our existing process for building and retiring clusters was a mess of manual steps and scripts that took up to a month per cluster. This wasn't just a technical headache - it was costing us real money. New hardware would sit unused while we worked through the process, and we were paying premium rates on old hardware we couldn't efficiently decommission. I knew we needed a better way.

My task was to design and implement an automated system that could handle the entire cluster lifecycle in under a week - a dramatic improvement from our month-long process. I needed to coordinate with multiple teams to define automation workflows and establish clear handoff points between different components. The challenge was particularly complex because we had to maintain business continuity during peak holiday periods while simultaneously rolling out the new system. I was also responsible for ensuring the transition wouldn't create additional costs during implementation, as we were already dealing with significant hardware expenses.

I started by sharing my automation vision with the capacity team and negotiating a transition timeline that wouldn't disrupt their operations. To maintain momentum, I prioritized key clusters based on their business impact and scheduled decommissions. I created a strategic roadmap that balanced our team's development work on the automation system with their ongoing operational responsibilities.

I broke down the project into three manageable phases: cluster build, tech refresh, and decommission. We tackled decommission first since it had the clearest ROI by reducing costs on outdated hardware. I worked directly with component teams to establish common implementation standards and contracts that would ensure smooth handoffs between different parts of the system.

To demonstrate the feasibility of our approach, I collaborated with the app lifecycle team to create a proof-of-concept implementation. This example helped other teams understand how to implement the contracts we'd defined. When we needed additional resources to accelerate development, I prepared a detailed progress report and presented it to management, successfully securing their support for the project.

Through persistent effort and collaboration, we achieved remarkable results. The automated decommission process reduced our timeline from several weeks to just a few days, and I implemented a self-service capability that gave the capacity team direct control over the process. We successfully applied the new automated system to more than five clusters, with the most significant win being our API gateway cluster automation meeting the one-week timeline target. The capacity team was particularly pleased with the self-service features, and leadership praised our ability to maintain business continuity while implementing such a significant change. Perhaps most importantly, we created a foundation for future immutable infrastructure capabilities that will help reduce incidents and improve resource utilization across our entire fleet. Looking back, this project taught me that breaking down complex challenges into manageable pieces, maintaining clear communication with stakeholders, and staying focused on incremental progress are crucial when tackling large-scale automation initiatives. The persistence required to coordinate multiple teams and overcome technical hurdles ultimately paid off in creating a more efficient, cost-effective system.

## Raw Answers
Could you tell me more about what triggered the need for this cluster lifecycle management vision and what challenges your team was facing at the time?

As a cloud fleet team, we keeps build new cluster and retire old cluster with hardware tech refresh. there are different clusters - cloud control plan cluster, network cluster, lb/app gateway clusters, generic clusters and hadoop clusters. With lots of customization, the cluster build and decomm right now are very complex flow, some of steps are manual, some of steps are based on script. it is risky and time consuming to complete one cluster build. Decomm is also risky, since we need to make sure all workload/traffic are moved out from this clusters. However the slow cluster build/decomm may cause finance impacts since new hardware is idle and old hardware kept high discount.

Can you recall an experience where your perseverance played a key role in overcoming a challenge?

I'd like to share my experience that I created a team vision on cluster lifecycle management and continuously put team resource on it and finally complete this complex product phase by phase.

What measurable improvements did you achieve in terms of cluster build/decomm time and cost savings after implementing your automation vision?

Now we completed the cluster decomm, it is fully automated, capacity team can just triage the decomm flow, by several days, the cluster got decommed, we have applied this way for more than 5 clusters. Team has completed the cluster build major flow and supported the api gateway cluster automation, we can build the cluster within one week. team is continuous working on other type of clusters.

What was the scale of this operation in terms of number of clusters and the typical timeline for building or decommissioning a cluster?

Every year, we need to build and retire 20+ clusters. and typical it took 2 week - 1 month to complete the build and decommission.

What specific actions did you take to drive this initiative forward when faced with resistance or setbacks?

I took multiple actions. 1. I shared the vision with our customer, capacity team owns the clusters build/decomm plan, I shared the automation vision but also persuade them to keep patient, since by investing resource on automation, we may have less developers working on current cluster build/decomm, so it could take more time. However there are 20+ clusters on plan, I identified these key clusters, and make sure key clusters' decomm/build delivered in time. 2. I communicate with team on balancing the development and operational work. we need to promise key clusters decomm/build, so no finance impacting, while we need to build a roadmap on cluster lifecycle. with limited resource, we split as cluster build, cluster tech refresh and cluster decomm, and we started with cluster decomm firstly. 3. I communicate with different component teams, discuss with them on common contract, and let them buy-in to implement the contract, based on it, they will remove the manual setup and decomm as well. I pickup one component (app lifecycle team owned) as example, share with others how to implement the contract. 4. When I made progress on cluster decomm, I did a share with management team, and let them know the complexity and benefits, and ask for more supports to continue investing on cluster build and cluster tech refresh.

Can you share any feedback or recognition you received from stakeholders or leadership about the impact of this automation initiative?

Capacity team is very happy since they can triage the cluster decomm by themselves, the decomm period has a significant reduction (from weeks to few days). Leadership team has high expectation on full cluster lifecycle automation, with this capability, then we can support immutable cluster/infrastructure, it will greatly reduce incident, easy to scale and improve the resource usage.

What were the potential business impacts or risks if the cluster lifecycle management wasn't improved?

When new hardware was purchased, if we can not build as cluster, then eBay can not use these resources, it will cause waste, on the other hand, if we retired the hardware later, then the discount will keep increasing, it also has finance loss. On the other hand, with business increasing, particular in holiday, if we can not onboard new clusters, the application will be in risky on high resource usage. then we probably can not support holiday peak time. it will impact the ebay site reliability and scalability

What specific goals or objectives did you set for yourself and the team to address these cluster lifecycle management challenges?

The cluster build and decomm automation are very complex, it involves multiple components owned by multiple teams (application lifecycle, network, security, hadoop etc.), My goal is complete the build and decomm within one week. To support it we need to define an automation flow and define contract for each components, then the flow will trigger each component's build and decomm.