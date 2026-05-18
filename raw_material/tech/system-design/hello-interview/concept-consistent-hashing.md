---
title: "Hello Interview — Core Concept: Consistent Hashing"
source: "https://www.notion.so/1f9afa27ec72802fa7d8fcc87d97b0ab"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Sharding and Scalability]]"
---

# Core Concept: Consistent Hashing

## Core Problem

How to distribute data across servers while **minimizing redistribution** when the number of servers changes.

Traditional modulo hashing: adding/removing one server remaps almost all keys → massive data movement.

## How It Works

1. Arrange both servers (nodes) and keys in a **circular hash ring** (0 to max hash value)
2. To find which node stores a key: hash the key, then **walk clockwise** to the first node
3. Adding a node: only keys between the new node and its predecessor need remapping
4. Removing a node: only that node's keys move to the next node clockwise

**Result**: adding/removing a node affects only a small fraction (1/n) of keys.

## Virtual Nodes

Each physical node is represented by **multiple virtual nodes** on the ring.

**Benefits**:
- More even load distribution
- Reduces variance in key assignment
- Graceful scaling: adding a node takes a small amount from many nodes rather than all from one

## Real-World Usage

- **Redis Cluster**: MOVED response directs clients to correct shard
- **Apache Cassandra**: partitioning data across nodes
- **Amazon DynamoDB**: internal partitioning
- **CDNs**: routing requests to edge nodes

## Key Design Scenarios

1. **Distributed database**: partition table rows across DB nodes
2. **Distributed cache**: find which cache node stores a given key
3. **Distributed message broker**: route messages to partitions/brokers

## Example Quote

> "Arrange everything in a circle and walk clockwise."

This mental model applies whenever you need to map a large keyspace to a smaller set of servers in a way that tolerates server additions/removals gracefully.
