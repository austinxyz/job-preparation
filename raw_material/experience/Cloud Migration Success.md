---
processed: true
experience_note: "[[experience/eBay - Cloud Migration to Kubernetes]]"
---

## Story

While leading platform engineering at eBay, we faced a massive challenge: transitioning our entire cloud infrastructure from VMs to containers and Kubernetes. We had 5,000 applications that needed migration across multiple technology stacks - everything from Java services to Node.js apps and batch jobs. Our existing home-grown CI/CD system was struggling with performance issues and slow recovery times. What made this especially complex was the variety of application types we supported, handling different traffic patterns from internal services to public-facing applications. The stakes were high - this migration would impact every development team at eBay.

As the engineering manager, I was tasked with leading a cross-functional team of 10+ engineers across our US and China offices to complete this migration within one year - without any service disruptions. My key responsibilities included developing a phased migration strategy, building automated tools to handle diverse application types, and ensuring compatibility with our new infrastructure components. I needed to coordinate closely with both the platform teams managing our new cloud resources and the application teams who would be impacted. The scope was daunting, but having clear ownership of the migration tooling and rollout plan gave us a solid foundation to start.

I started by establishing clear ownership between our global teams - the US team would focus on orchestration while our China team handled load balancer configuration conversion. To ensure alignment, I created a unified migration blueprint we called 'Application Instance Migration' that detailed each step of the process. I then worked closely with our product manager and tech lead to translate requirements into technical designs and secure the necessary resources.

Knowing the complexity of the migration, I implemented a phased approach with distinct stages: preparation, workload creation, traffic switching, baking period, and decommissioning. For each phase, I built in rollback capabilities to minimize risk. To validate our approach, I personally drove the implementation of comprehensive end-to-end test cases covering different application types.

To maintain visibility and accountability, I built a migration dashboard to track progress across all applications. I also set up multiple communication channels - regular sync meetings between teams, dedicated Slack channels for immediate support, and formal design review processes. This multi-channel approach ensured we could quickly address issues while maintaining proper documentation of key decisions.

Our systematic approach and strong team collaboration paid off significantly. We reduced deployment duration by 75%, bringing the time for large application pools down from 4 hours to just 60 minutes. The new containerized infrastructure, with its built-in remediation and auto-scaling capabilities, dramatically improved our site reliability. This led to a notable reduction in site incidents, which was particularly important given eBay's high-traffic environment.

The application teams were especially pleased with the improved productivity and reliability. Their positive feedback centered around the streamlined deployment process and reduced maintenance overhead. Perhaps most importantly, we successfully enabled eBay's framework team to leverage cloud-native features, opening up new possibilities for innovation and scalability.

What I'm most proud of is that we completed the migration of all 5,000 applications within our one-year timeline while maintaining system stability throughout the process. This success demonstrated not just technical excellence, but also the power of clear communication, thoughtful planning, and strong cross-functional collaboration. The project became a blueprint for how we approach large-scale infrastructure transitions at eBay.

## Raw Answers
What specific strategies or processes did you implement to track and ensure the successful migration of all 5000 applications?

We built the migration dashboard, it will clearly show the migration progress, and also based on the release plan for different features, we design the migration plan with multiple batches, based on application type, application size, topology types, started with pilot applications and then speed up. For each of application, we split as different phase, preparing (user notification), workload creation, traffic switch and baking and old application decomming, before the whole application decomm, each steps we support rollback. when there are migration issues happened, it is easy to move back.

Did you receive any recognition or feedback from stakeholders about the success of this migration project?

Yes, application teams were very happy since the migration significant improved the productivity and reliability. and eBay framework team also provide very positive feedback since the framework is designed based on cloud native features.

Can you tell me more about what triggered this cloud migration project and what challenges the team was facing with the existing system?

eBay cloud platform used to be VM (virtual machine) based, we have home-grown CI/CD - build and deployment system based on eBay own framework. And then the cloud platform moves to container based and K8s, which is more flexible and scalable and with powerful community support. To reduce the risk, the migration split as 2 phases, use pod/container as VM by eBay home-grown CI/CD (call as assimilation) and then migrate assimilation application into cloud native that we will just leverage on K8s build (image) and deployment. there are many challenges, eBay has 5000 applications with multiple stacks (Java, node js, messaging, batch etc.) and multiple topologies (private traffic, public traffic, public traffic with L7 and public traffic + POP traffic). We need to build migration tools smoothly migrate all applications without downtime within one year.

What were the key business drivers and potential risks if this migration wasn't executed successfully?

if migration wasn't executed successfully, then our application are managed by home grown build/deployment system, however these systems were built based on VM not on container. there are performance bottleneck. The slow recovery capability may cause business revenue lost. On the other hand, with tech refresh, new hardware (compute asset) is defined based on cloud native, and switched from hardware LB to software LB. Only cloud native solution can support the new asset and software LB.

What were the key measurable outcomes and benefits achieved after completing this migration project?

The overall velocity and reliability has a significant improvement when ebay application run as Cloud native application. The deployment duration was reduced to 25%, for large pools, it was 4 hours and now within 60 mins. The site reliability also has big improvement, with native, we support container remediation and auto-scale, so it will reduce the site incidents.

Can you describe a time when your communication and collaboration skills were pivotal in achieving a team goal?

I'd like share the story that I engage team to migrate eBay assimilation applications to native cloud application which will significantly improve the productivity and manageability.

What was the size of the team you were leading for this migration project?

I lead the cloud application lifecycle management team including 10+ members across US and China.

How did you structure and facilitate collaboration between the US and China teams to ensure effective communication and alignment?

US team and China team has different focus, in early stage we created a unified BP and decide the main responsibility for each team, US team mainly focus on the orchestration, we build a workflow calling Application Instance Migration. it define the whole migration flow - but different workload and different topology will have different steps. China team mainly focus to convert the original hardware LB configuration into K8s spec for software LB, they will support dry-run to make sure the conversion is success. so there are small interface/contract between two teams. We build many end2end test cases to support different type of application's migration. when new feature is release, it will be easy to verify by running end2end testing. Also we setup regular sync meeting, on-demand slack channel. formal design BP as mulitple channels for communications.

What specific responsibilities and goals were assigned to you personally in leading this migration project?

I need to work with framework team to built tools to support different type of applications (java service, front end app, messaging and batch), different type of application's workload are different - stateless and stateful, and work with network team to let tool support different type of topology traffic migration. there are lots of features and need to create a concrete plan with multiple phases. Internally I worked with product manager and tech lead to convert the migration requirements to design and promise enough resource and make sure we deliverable in time with high quality.