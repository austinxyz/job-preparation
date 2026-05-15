---
title: Hello Interview — Key Technology: Flink (Stream Processing)
source: "https://www.notion.so/200afa27ec7280faa6add72d39134b53"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Streaming and Event-Driven Architecture]]"
---

# Key Technology: Flink (Stream Processing)

## Core Purpose

Distributed stream processing framework. Processes unbounded data streams in real-time with stateful computation, windowing, and exactly-once semantics.

## Key Concepts

- **Source**: data input (Kafka, files, sockets)
- **Transformation**: map, filter, aggregate, join
- **Sink**: output destination (database, Kafka, files)
- **Windows**: tumbling (fixed non-overlapping), sliding (overlapping), session
- **State**: maintained across events; checkpointed for fault tolerance

## When to Use Flink in Interviews

**Good fit**:
- Aggregating click/event streams in real-time (Ads Click aggregation)
- Complex stateful processing across events
- Exactly-once processing requirements
- Multiple simultaneous consumers with different processing logic

**Usually overkill**:
- Simple message transformation (just consuming from Kafka + service)
- Stateless per-event processing

## Important Caveats

1. **Operational overhead**: requires deploying + monitoring + scaling a separate Flink cluster
2. **State management**: most powerful feature + biggest operational challenge; must plan for state growth + recovery
3. **Window choice** dramatically impacts accuracy and resource usage — justify your windowing decisions
4. **Exactly-once processing**: adds performance overhead + complexity; confirm you actually need it

## Lessons from Flink's Design (applicable broadly)

1. **Separation of Time Domains**: processing time vs. event time (when event actually occurred) — important for out-of-order event handling
2. **Watermarks**: track progress through unordered event streams (declare "we've seen all events up to time T")
3. **State Management Patterns**: local state + checkpointing informs design of other stateful distributed systems
4. **Exactly-Once Processing**: checkpoint + transaction coordination techniques applicable to other streaming systems
5. **Resource Isolation**: slot-based resource management → clean isolation and sharing in distributed systems

## Interview Configuration Tips

For near real-time (<5s) processing:
- Tumbling windows of 1-2 seconds
- 10-20 parallel tasks per operator
- RocksDB state backend for large states
- Watermarks with small allowed lateness for late-arriving events
