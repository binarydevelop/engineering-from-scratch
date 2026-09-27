# Social Network Dataset

Graph and engagement model for social interactions, follower relationships, mutual connections, and content feeds.

## Entity-Relationship Diagram

```text
       ┌──────────┐
       │  users   │◄────────┐
       └───┬──────┘         │
           │ 1              │
     ┌─────┴────────┐       │
     ▼ N            ▼ N     │ N
  [posts]       [follows] ──┘
     │ 1            (follower_id -> users.id, following_id -> users.id)
     ├─── N [comments]
     └─── N [likes]
```

## Key Query Capabilities
- Mutual follow graph queries (find users who follow each other).
- Follower recommendations ("Followed by people you follow").
- Feed generation sorted by activity with composite index optimization.
- Lurker detection (users with 0 posts and 0 follows).
