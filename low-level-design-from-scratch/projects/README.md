# Canonical Low-Level Design Projects

This directory contains **23 complete, production-grade LLD systems**. Every project demonstrates first-principles object-oriented design, explicit responsibility placement (GRASP Information Expert), inviolable domain invariants, and automated test coverage.

| Project | System | Core Architectural Challenge |
|:---|:---|:---|
| `01-tic-tac-toe` | **Tic-Tac-Toe Game Engine** | Design an extensible NxN Tic-Tac-Toe engine with dynamic board dimensions, configurable winning strategies, and turn-based player loops. |
| `02-snake-and-ladder` | **Snake and Ladder Game** | Turn-based board game with configurable dice strategies, jump chains (snakes and ladders), and winning position invariants. |
| `03-vending-machine` | **Vending Machine System** | The canonical state modeling problem: inventory management, multi-coin insertion, product dispensing, change return, and refund safety. |
| `04-parking-lot` | **Parking Lot Management** | Multi-floor parking lot with dynamic vehicle size allocation (Motorcycle, Compact, Large, EV), tickets, and pluggable pricing tariffs. |
| `05-elevator-system` | **Elevator Bank System** | Multi-car elevator bank with hall calls, car calls, car movement state machines, and LOOK/SCAN scheduling dispatch algorithms. |
| `06-library-management` | **Library Management System** | Book title catalog vs physical barcode copies, member borrowing limits, reservation queues, and fine calculation. |
| `07-chess-game` | **Chess Game Move Engine** | 8x8 Board representation, polymorphic piece movement rules, check detection, turn validation, and game status tracking. |
| `08-atm-system` | **ATM Banking Terminal** | ATM session state machine, PIN authentication, cash dispenser Chain of Responsibility, and bank gateway boundaries. |
| `09-splitwise` | **Splitwise Expense Sharing** | Users, groups, expense creation, split strategies (Equal, Exact, Percentage), and debt balance graph simplification. |
| `10-movie-ticket-booking` | **Movie Ticket Booking Engine** | Cinema halls, shows, seat reservations, temporary locks with timeouts, and payment processing seams. |
| `11-hotel-booking` | **Hotel Room Booking System** | Room types, inventory availability across date ranges, seasonal tariffs, and cancellation policies. |
| `12-car-rental` | **Car Rental Fleet Service** | Vehicle fleet inventory, branch reservations, rental duration calculation, and damage inspection logs. |
| `13-food-delivery` | **Food Delivery Cart & Order** | Restaurant menus, cart aggregate root, line items, order state transitions, and delivery driver assignment. |
| `14-ride-sharing` | **Ride Sharing Trip Engine** | Rider/Driver matching strategies, trip state machine (Requested, Accepted, InProgress, Completed), surge tariffs, and fare calculation. |
| `15-logger-framework` | **Extensible Logging Framework** | Log levels, hierarchical loggers, message formatters, and appender destinations (Console, File) using Chain and Decorator. |
| `16-lru-cache` | **In-Memory LRU / LFU Cache** | Generic key-value storage with capacity limits and pluggable eviction strategies (LRU via Doubly Linked List + Map). |
| `17-rate-limiter` | **API Rate Limiter Engine** | Token Bucket and Sliding Window rate limiting algorithms with thread-safe client request accounting. |
| `18-task-scheduler` | **Priority Task Scheduler** | One-time and recurring cron tasks, priority queue execution ordering, retry policies, and execution worker pool. |
| `19-notification-service` | **Multi-Channel Notification Platform** | Email, SMS, Push notification dispatch with provider failovers, priority queuing, and template rendering. |
| `20-payment-gateway` | **Idempotent Payment Gateway** | Payment requests, idempotency key deduplication, payment processor interfaces, and refund state machines. |
| `21-inventory-management` | **SKU Inventory Reservation** | Warehouse SKUs, atomic stock reservation, release on timeout, and fulfillment verification. |
| `22-in-memory-pubsub` | **Topic Pub/Sub Engine** | Publishers, topics, subscriber registration, content filtering, and event broadcast dispatch. |
| `23-metrics-library` | **Application Metrics Telemetry Library** | In-memory Counter, Gauge, Timer metrics collectors and console/Prometheus formatters. |