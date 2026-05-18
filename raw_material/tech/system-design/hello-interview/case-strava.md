---
title: "Hello Interview — Case: Strava (Activity Tracking)"
source: "https://www.notion.so/1edafa27ec728029846fdbeeaffba8d2"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Strava]]"
---

# Case: Strava (Activity Tracking)

## Key Design Questions & Answers

### Start/Pause/Stop/Save Activities

1. User starts activity: `POST /activities` → Activity Service creates record in DB, returns activityId
2. PATCH activity status as START; client sends regular POST to record route locations (Route table)
3. PAUSE: `PATCH /activities/:id` with status=PAUSED + timestamp
4. RESUME: `PATCH` with status=RESUMED (sum timestamps to calculate active duration, excluding paused periods)
5. FINISH: `PATCH` with status=COMPLETED

### Live Statistics During Activity

1. Client app uses device GPS, records location every 5 seconds → POST to Activity Service
2. Activity Service stores location + timestamp in Route table
3. Client app maintains local location list → calculates distance, speed, duration locally

### Efficient Distance Calculation for Long Rides

1. Client stores batch of route data in mobile in-memory, every 3s → persists to mobile local temp file
2. Every 30s: incremental distance calculation using **Vincenty formula** (accounts for Earth's curvature for long distances)
3. Client sends batch route + current total distance to Activity Service every longer interval
4. After server update, local data refreshed
5. Server only receives incremental updates, not full recalculations

### Offline Activity Tracking

1. Client records route in mobile memory → every 3s persists to local storage
2. Offline: route data stays on device
3. On reconnection: client batch-POSTs all route info to server
4. Conflict resolution strategies: version field, client-first, or server-first policy
5. For long offline periods: compress route data to save local storage
6. Sync checkpointing: split into chunks (1-50, 51-100), resume from failed checkpoint; avoid re-syncing successful chunks
7. Extended storage: reduce precision for older route points, or establish max thresholds

### Real-Time Friend Activity Sharing (In-Progress)

1. Client polls `GET /activities?status=inprogress&type=friend` → get in-progress friends' activityIds
2. For specific activity: mobile polls `GET /activities/:id/routes` every 5s (polling preferred over WebSocket to keep server stateless)
3. Active app: short poll interval; background: longer interval
4. Add Redis cache for hot activity/route data under high polling load
5. Priority-based polling for large friend lists: close friends + hot activities get higher priority with rate limiting

### Global Leaderboard (Total Distance)

1. **Redis Sorted Set** for leaderboard
2. On activity completion: `ZAdd` with athlete's total distance
3. `ZRange` to get top N athletes sorted by total distance
4. Redis in-memory → data loss risk; reconcile service periodically reads Activity DB and reconciles total distances
5. At millions of users: split into regional leaderboards (SF, LA, etc.) → merge top N per region into global board
