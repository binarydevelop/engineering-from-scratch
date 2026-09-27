# Phase 145: Final Design Challenge Set (25 Unseen Production Problems)

> **Motto:**  
> **"Mastery is not the ability to recite solved problems; it is the ability to walk into an ambiguous, unseen domain and systematically engineer an invariant-protecting, decoupled software system."**

---

## Challenge Set Structure & Rules
This challenge set contains **25 completely unseen, un-solved Low-Level Design specifications** categorized by difficulty:
- **Beginner Tier (5 Problems):** Single-process, focused domain boundaries with clear state rules.
- **Intermediate Tier (10 Problems):** Multi-component collaboration, polymorphism, time dependencies, and pluggable strategies.
- **Advanced Tier (10 Problems):** Concurrency contention, state machine lifecycles, recovery rollbacks, and architectural seams.

### Rules of Engagement:
1. **No Inline Solutions:** Do not search for pre-existing templates. Treat each problem as a live 45-minute architectural challenge.
2. **Behavior First:** Never start with class diagrams. Trace user journeys and dynamic use cases first.
3. **Explicit Invariants:** Identify at least 3 inviolable rules that must never be broken under any sequence of calls.
4. **GRASP Responsibility Assignment:** Fill a responsibility table justifying every class assignment with Information Expert.

---

## 🟢 Beginner Tier (5 Problems)

### Problem B-01: Digital Keypad Door Lock
- **Requirements:** 4-to-8 digit PIN code, temporary one-time guest codes with usage limits, physical lock/unlock status sensors, and 3-strike lockout for 5 minutes.
- **Ambiguous Points:** Does the lock auto-lock after a timeout? How are master administrator pins differentiated from guest pins?
- **Extension Request:** Support an emergency master NFC keycard override.
- **Edge Cases:** Power loss mid-unlock; entering 5 digits of an 8-digit pin and pausing for 30 seconds.

### Problem B-02: Coffee Mug Warmer Pad
- **Requirements:** Auto-detect mug placement via weight sensor (minimum 100g), adjustable target temperature presets (Low 45°C, Medium 55°C, High 65°C), 2-hour auto-shutoff timer.
- **Ambiguous Points:** Does empty mug trigger shutoff? How fast does the heater adjust to temperature changes?
- **Extension Request:** Add support for maintaining liquid volume estimates and alerting when boiling dry.
- **Edge Cases:** Rapidly placing and removing a mug 10 times in 5 seconds; sensor reporting -50°C due to hardware fault.

### Problem B-03: Library Study Room Booker
- **Requirements:** Single-room booking system, 1-hour fixed time slots from 8 AM to 8 PM, max 2 consecutive slots per student, student ID verification.
- **Ambiguous Points:** Can reservations be cancelled 5 minutes before the slot? How are no-shows released?
- **Extension Request:** Support recurring weekly slot bookings for study groups.
- **Edge Cases:** Two students requesting the same 2 PM slot at the exact same millisecond; student attempting to book slot 12 hours in advance.

### Problem B-04: Digital Counter Clicker (Tally Counter)
- **Requirements:** Increment, decrement, reset to zero, configurable step size (e.g. +1, +5), maximum count threshold alert.
- **Ambiguous Points:** Can count go below zero? Does reset require confirmation?
- **Extension Request:** Support multiple named tally counters with aggregate summary statistics.
- **Edge Cases:** Decrementing at zero; integer overflow past 2 billion.

### Problem B-05: Simple Pomodoro Timer Engine
- **Requirements:** 25-minute work interval, 5-minute short break, 15-minute long break after 4 intervals, pause/resume, audio bell callback contract.
- **Ambiguous Points:** What happens if user pauses for 2 hours? Does the interval reset?
- **Extension Request:** Support customizable interval durations and daily productivity metrics reporting.
- **Edge Cases:** System clock adjusted backward by 1 hour (DST transition) during active countdown.

---

## 🟡 Intermediate Tier (10 Problems)

### Problem I-01: Multi-Tenant Subscription Feature Gate
- **Requirements:** Support tiers (Free, Pro, Enterprise), per-feature quotas (e.g. 5,000 API calls/month), dynamic quota replenishment on billing date, hard-stop vs soft-cap warnings.
- **Ambiguous Points:** What happens when an organization changes tiers mid-billing cycle? How is prorated quota calculated?
- **Extension Request:** Support custom enterprise contract overrides for individual features.
- **Edge Cases:** Concurrent API calls consuming the final 1 available token simultaneously.

### Problem I-02: Airport Luggage Conveyor Router
- **Requirements:** Track baggage tags through 3 routing junction scanners, sort bags by destination flight gate, emergency jam divert bays, baggage weight verification.
- **Ambiguous Points:** What happens if a tag is unreadable by scanner? How is baggage rerouted if a gate changes mid-transit?
- **Extension Request:** Support priority baggage fast-track routing algorithm.
- **Edge Cases:** Scanner misread producing unknown flight number; baggage overweight by 0.1kg.

### Problem I-03: Cinema Concession Stand Order Kiosk
- **Requirements:** Combo meals with substitutions (swap soda for water, size upgrades), inventory ingredient deduction, loyalty points redemption, split cash/card payment.
- **Ambiguous Points:** When is inventory reserved: at item addition to cart or at payment swipe?
- **Extension Request:** Dynamic combo pricing optimization (automatically grouping individual items into combos for lowest customer price).
- **Edge Cases:** Popcorn machine runs out of butter salt while customer is swiping credit card.

### Problem I-04: Automated Car Wash Controller
- **Requirements:** 3 wash programs (Basic, Deluxe, Platinum), sequence of physical stations (Pre-soak, Foam, Scrub, Rinse, Wax, Dry), safety vehicle sensor interlocks.
- **Ambiguous Points:** How does the conveyor coordinate vehicles entering while another is drying?
- **Extension Request:** Emergency stop button that halts conveyor and raises washing brushes immediately.
- **Edge Cases:** Car shifts out of neutral during scrubbing; driver opens door mid-wash.

### Problem I-05: Doctor Appointment Calendar Engine
- **Requirements:** Variable length appointment slots (15m checkup, 45m consultation), doctor availability schedules, buffer times between patients, conflict detection.
- **Ambiguous Points:** Can appointments span across lunch breaks? How are emergency walk-ins accommodated?
- **Extension Request:** Support patient waiting list with automatic notification when a cancellation occurs.
- **Edge Cases:** Doctor updates schedule to take leave after appointments are already booked.

### Problem I-06: Vending Machine Smart Refund Manager
- **Requirements:** Cash and digital contactless payments, escrow coin return, failure compensation rollback, change coin tube inventory optimization.
- **Ambiguous Points:** What happens if machine owes $0.40 change but only has $0.25 and $0.05 coins?
- **Extension Request:** Dynamic pricing based on refrigerated beverage temperature.
- **Edge Cases:** Mechanical drop sensor fails to detect beverage dropping into hopper.

### Problem I-07: Fitness Gym Turnstile Access Gate
- **Requirements:** NFC membership badge scan, active subscription check, facility capacity head-count limiter, emergency fire evacuation unlock.
- **Ambiguous Points:** What if a member scans in, turns around without entering, and scans again?
- **Extension Request:** Restrict off-peak memberships from scanning between 5 PM and 8 PM.
- **Edge Cases:** Power outage during turnstile rotation mid-step.

### Problem I-08: Self-Service Parcel Drop-off Kiosk
- **Requirements:** Barcode scanning, dimension scale measurement, weight verification, shipping label generation, locker bin deposit assignment.
- **Ambiguous Points:** What if measured weight exceeds declared postage weight?
- **Extension Request:** Hazardous goods declaration questionnaire gating compartment assignment.
- **Edge Cases:** Customer closes locker door before placing parcel inside.

### Problem I-09: Bicycle Rental Dock Station
- **Requirements:** Multi-dock physical stand, bike release solenoid lock, trip duration billing calculation, broken bike reporting lockout.
- **Ambiguous Points:** How is overtime billed if user docks bike at a full station?
- **Extension Request:** Rebalancing incentive calculation (discounting trips that return bikes to depleted stations).
- **Edge Cases:** User yanks bike from dock while solenoid is unlocking.

### Problem I-10: Online Auction Bid Sniping Protector
- **Requirements:** Timed English auction, minimum bid increment rules, auto-extension window (bids in final 2 minutes extend auction by 5 minutes), proxy bidding.
- **Ambiguous Points:** How are simultaneous identical proxy bids prioritized?
- **Extension Request:** Reserve price hidden threshold logic.
- **Edge Cases:** Two bids placed in the exact same millisecond with identical amounts.

---

## 🔴 Advanced Tier (10 Problems)

### Problem A-01: High-Contention Flash Sale Ticket Engine
- **Requirements:** 50,000 concurrent users fighting for 500 VIP concert tickets. 5-minute temporary reservation hold, inventory decrement race condition defense, payment gateway seam.
- **Ambiguous Points:** How are expired holds returned to inventory without race conditions?
- **Extension Request:** Tiered queue waiting room with token-based entry pass.
- **Edge Cases:** User closes browser after card is charged but before confirmation callback.

### Problem A-02: Autonomous Drone Delivery Air-Traffic Grid
- **Requirements:** 3D cubic airspace collision avoidance, delivery corridor reservation, battery drain waypoint recalculation, emergency landing failsafes.
- **Ambiguous Points:** How do drones communicate priority when two paths intersect?
- **Extension Request:** Dynamic weather exclusion zones that reroute in-flight drones.
- **Edge Cases:** Sudden loss of GPS signal requiring dead-reckoning state transition.

### Problem A-03: Multi-Account Financial Settlement Engine
- **Requirements:** Double-entry ledger accounting, multi-currency transaction splits, daily batch netting balance simplification, immutable audit journal.
- **Ambiguous Points:** How are rounding fractions of cents allocated across 3-way split transactions?
- **Extension Request:** Support automated rollback and compensation transactions for failed settlement legs.
- **Edge Cases:** Attempting to settle an account while a concurrent debit transaction is uncommitted.

### Problem A-04: Distributed Lock Lease Manager (In-Process)
- **Requirements:** Reentrant lock with configurable lease timeout, heartbeat renewal contract, deadlock detection via wait-for graph, fair FIFO acquisition queue.
- **Ambiguous Points:** What happens if lease expires while holder thread is still executing critical section?
- **Extension Request:** Asynchronous lock acquisition with CompletableFuture callbacks.
- **Edge Cases:** Thread terminates abruptly without releasing held lock lease.

### Problem A-05: Real-Time Stock Order Matching Engine
- **Requirements:** Price-time priority limit order book (Bids / Asks), market orders, partial order fills, trade execution event publication, cancellation in O(1) or O(log N).
- **Ambiguous Points:** How are market orders handled when order book has insufficient depth?
- **Extension Request:** Support Stop-Loss and Iceberg order types.
- **Edge Cases:** Incoming buy limit price higher than current lowest ask (immediate cross execution).

### Problem A-06: Containerized Job Pipeline DAG Scheduler
- **Requirements:** Directed Acyclic Graph (DAG) dependency resolution, topological task execution, retry with exponential backoff, parallel task worker pool, downstream failure cancellation.
- **Ambiguous Points:** How are cycles detected and rejected during pipeline definition?
- **Extension Request:** Support conditional branching tasks based on upstream task output exit codes.
- **Edge Cases:** Upstream task fails while two parallel downstream branches are running.

### Problem A-07: In-Memory Time-Series Metric Aggregator
- **Requirements:** Thread-safe high-throughput metric ingestion (100k events/sec), sliding window rollups (1m, 5m, 1h), percentile approximations (p50, p95, p99), memory-bounded retention.
- **Ambiguous Points:** What is the tradeoff between memory consumption and quantile accuracy (T-Digest vs Reservoir Sampling)?
- **Extension Request:** Downsampling older raw datapoints into 1-hour summary buckets.
- **Edge Cases:** Clock skew causing metric timestamps to arrive out-of-order by 10 minutes.

### Problem A-08: Smart Grid EV Charging Load Balancer
- **Requirements:** Total substation electrical capacity limit (e.g. 500kW), dynamic charging rate throttling across 30 charging bays based on vehicle battery curve, departure urgency priority.
- **Ambiguous Points:** How is power reallocated when a vehicle completes charging or a new high-priority vehicle plugs in?
- **Extension Request:** Integration with fluctuating solar panel power input sensors.
- **Edge Cases:** Power grid brownout dropping total available capacity to 50kW instantaneously.

### Problem A-09: Collaborative Document Real-Time Operational Transform (OT)
- **Requirements:** Character insertion and deletion transformations across 2 concurrent users, site ID tie-breaking, intent preservation, undo stack operational inverse.
- **Ambiguous Points:** How does client state synchronize with central server revision history?
- **Extension Request:** Rich text formatting range transformations (bold, italic spans).
- **Edge Cases:** Client disconnects, makes 10 offline edits, and reconnects to a document that has advanced 50 revisions.

### Problem A-10: Automated Multi-Floor Warehouse Shuttle Dispatcher
- **Requirements:** Fleet of 10 automated robotic shuttles moving totes between storage racks and pick stations, collision avoidance on shared tracks, battery charging schedule, throughput optimization.
- **Ambiguous Points:** How are totes prioritized when 5 pick stations request items from the same rack simultaneously?
- **Extension Request:** Emergency track segment blockage isolation without halting unaffected warehouse zones.
- **Edge Cases:** Shuttle breakdown on a main trunk track carrying a critical customer tote.
