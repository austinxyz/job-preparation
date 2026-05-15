---
title: Hello Interview — Core Concept: CAP Theorem
source: "https://www.notion.so/1f9afa27ec728079ae01e1068b143384"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Distributed Systems]]"
---

# Core Concept: CAP Theorem

## Three Properties

- **Consistency**: all nodes see the same data at the same time
- **Availability**: every request receives a response
- **Partition Tolerance**: system continues operating despite arbitrary message loss or partial failures

**Key rule**: In a distributed system, partition tolerance is a **must-have**. So the real choice is between consistency and availability during network partitions.

## When to Choose Consistency (CP)

**Use cases**: Ticket booking, e-commerce inventory, financial systems

**Design approaches**:
- Distributed transactions
- Single-node solutions (single source of truth)
- **Databases**: RDBMS, Google Spanner, DynamoDB in strong consistency mode

## When to Choose Availability (AP)

**Use cases**: Social media, content platforms (Netflix), review sites (Yelp)

**Design approaches**:
- Multiple replicas
- Change Data Capture (CDC) for sync
- **Databases**: Cassandra, DynamoDB (default), Redis

## Both in the Same System

Many real systems need both — for **different features**:

| System | Consistency Feature | Availability Feature |
|--------|--------------------|--------------------|
| TicketMaster | Booking a seat | Viewing event info |
| Tinder | Match creation | Viewing user profiles |

## Consistency Levels (Spectrum)

- **Strong consistency**: every read returns the most recent write (bank accounts, inventory)
- **Causal consistency**: operations in causal order visible to all users (comments, posts)
- **Read-your-own-writes consistency**: user sees their own writes immediately (social media posts)
- **Eventual consistency**: all nodes converge to same value given enough time
