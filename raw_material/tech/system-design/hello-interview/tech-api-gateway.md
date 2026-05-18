---
title: "Hello Interview — Key Technology: API Gateway"
source: "https://www.notion.so/1feafa27ec728025bfddd966500a2e31"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/API Design]]"
---

# Key Technology: API Gateway

## Purpose

Single entry point for all client requests. Manages and routes requests to appropriate backend services.

## Core Functions

- **Routing**: primary function; URL paths, HTTP methods, query parameters, headers
- **Authentication**: verify identity before forwarding
- **Request handling**: validation (URL, headers, body format), size limits
- **Rate limiting**: throttle traffic per client/endpoint
- **SSL termination**: decrypt HTTPS at gateway level
- **Caching**: full response or partial (for infrequently-changing data); TTL or event-based invalidation
- **Middleware**: logging/monitoring, compression, CORS headers, IP whitelist/blacklist, response timeouts, API versioning, service discovery integration

## Protocol Support

- Primarily HTTP/REST
- Can support gRPC

## Scaling

- **Horizontal scaling**: stateless → add more gateway instances
- **Global distribution**: regional deployments, DNS-based routing (GeoDNS), configuration synchronization across regions

## Popular Implementations

| Product | Notes |
|---------|-------|
| AWS API Gateway | AWS integration; REST/WebSocket |
| Azure API Management | Policy-based configuration |
| Google Cloud Endpoints | gRPC support |
| Kong | Built on Nginx |
| Tyk | GraphQL; multi-data-center |
| Express Gateway | Node.js based |

## When to Use

**Use when**: microservices architecture with multiple backend services

**Skip when**: simple client-server architecture (single backend)

> TLDR: API Gateway adds value when you have multiple services that need a unified entry point. It's unnecessary overhead for monolithic or simple architectures.
