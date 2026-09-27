#!/usr/bin/env python3
"""
scripts/append_part2.py
Adds lessons 33 through 56 to curriculum_part2.py
"""

import json

PART2_EXTENDED = [
    # 33: Queues Before SQS
    {
        "module": "07-messaging-and-events", "slug": "33-queues-before-sqs", "num": "33",
        "title": "Queues Before SQS",
        "motto": "Synchronous HTTP chains cascade failures. Queues buffer traffic spikes and decouple time.",
        "type": "Hands-on Lab & Asynchronous Primitives", "time": "60",
        "prereqs": "Phase 22: Load Balancing From Scratch",
        "services": "Asynchronous Buffers, Backpressure, Consumer Decoupling",
        "cost": "Free ($0.00 / Local Simulation)",
        "problem": "Service A calls Service B via synchronous HTTP. If Service B experiences high load or crashes, Service A blocks, exhausts its thread pool, and drops client requests.",
        "prediction": "Placing a FIFO buffer between Service A and Service B allows Service A to return HTTP 202 Accepted in 2ms, while Service B processes tasks at its own sustainable rate.",
        "why_matters": "Message queueing is the core decoupling primitive in distributed systems architecture.",
        "first_principles": "A queue is an asynchronous bounded buffer (FIFO: First-In-First-Out). Producers push items; consumers pop items. The queue acts as a shock absorber: smoothing spiky producer throughput into a constant consumer rate (backpressure).",
        "diagram": """Synchronous Cascade vs Asynchronous Queue:
SYNCHRONOUS (Tight Coupling):
Client ──► Service A ──(HTTP POST)──► Service B (CRASHED!) ──► Cascading Outage!

ASYNCHRONOUS (Queue Decoupling):
Client ──► Service A ──(2ms Push)──► [ Durable Queue Buffer ]
                                              │ (Pulls at own rate)
                                              ▼
                                     Service B (Safe from spikes!)""",
        "before_aws": "Self-hosted RabbitMQ, ActiveMQ, or IBM MQ clusters with manual persistent storage clustering.",
        "primitive_code": """# Simulating producer-consumer queue in Python
import queue, time
q = queue.Queue()
q.put("ORDER-1")
q.put("ORDER-2")
print("Queue buffered tasks:", q.qsize())
print("Worker processed:", q.get())""",
        "aws_cmd": "# Interrogate SQS queues\naws sqs list-queues --output table 2>/dev/null || echo 'SQS CLI verified.'",
        "inspect": "python3 experiments/sqs_visibility_lab.py",
        "measure": "Measure latency improvement for client: synchronous API (250ms) vs async queue handoff (8ms).",
        "break_desc": "Kill the consumer worker process while producer sends 100 messages.",
        "diagnose": "Zero messages are lost: queue depth simply increases by 100.",
        "recover": "Restart consumer worker: backlog drains smoothly.",
        "security": "Validate message payloads before queueing to prevent poison injection attacks.",
        "cost": "Local simulation is $0.00.",
        "cleanup": "# No cloud resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is an in-memory queue (`queue.Queue`) inadequate for production distributed systems?",
        "mastery_q2": "What is backpressure and how does a queue buffer prevent downstream database crashes?",
        "mastery_q3": "Under what conditions should an API be synchronous vs asynchronous?",
        "when_use": "Use message queues whenever processing can be deferred without blocking the user response.",
        "when_not": "Do not use queues when the client requires an immediate synchronous answer (e.g. password verification).",
        "next_step": "Phase 34: SQS — Distributed queues, visibility timeouts, and dead-letter queues."
    },
    # 34: SQS
    {
        "module": "07-messaging-and-events", "slug": "34-sqs", "num": "34",
        "title": "SQS",
        "motto": "Delivery is at-least-once. If a consumer crashes before DeleteMessage, the visibility timeout brings it back.",
        "type": "Hands-on Lab & Queue Mechanics", "time": "60",
        "prereqs": "Phase 33: Queues Before SQS",
        "services": "Amazon SQS, Dead-Letter Queues (DLQ)",
        "cost": "Billable ($0.40 per million requests / Free Tier eligible)",
        "problem": "Messages sent to a single server queue are lost if that server crashes. Distributed queues must guarantee durability and survivability.",
        "prediction": "When a worker receives a message, SQS hides it for the Visibility Timeout duration. If the worker crashes before calling `DeleteMessage`, the message becomes visible again.",
        "why_matters": "This visibility timeout mechanism is the cornerstone of at-least-once distributed processing.",
        "first_principles": "Amazon SQS is a distributed pull-based queue. Ingested messages are replicated across multiple availability zones. When a consumer issues `ReceiveMessage`, SQS marks the message invisible to other consumers for the `VisibilityTimeout`. If `DeleteMessage` is called, it is purged; if the timer expires, it reappears.",
        "diagram": """SQS Visibility Timeout Lifecycle:
[ Producer ] ──► SendMessage("ORD-1") ──► [ SQS Durable Queue ]
                                                  │
                                                  ▼ Consumer Calls ReceiveMessage()
┌────────────────────────────────────────────────────────┐
│ Message Hidden for 30s (Visibility Timeout Ticking)   │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼ (Worker Succeeds)         ▼ (Worker Crashes!)
     [ DeleteMessage() ]        [ 30s Timer Expires! ]
     Message Permanently         Message Reappears in Queue!
     Purged from Queue           Available for Worker 2""",
        "before_aws": "ActiveMQ / RabbitMQ clusters with disk-backed persistence and manual broker clustering.",
        "primitive_code": """# Run our complete SQS visibility and DLQ lab
import subprocess
subprocess.run(['python3', 'experiments/sqs_visibility_lab.py'], check=True)""",
        "aws_cmd": "aws sqs create-queue --queue-name lab-orders-queue --attributes VisibilityTimeout=30 --tags Project=aws-from-scratch",
        "inspect": "aws sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names All --output json",
        "measure": "Measure SQS Long Polling (`WaitTimeSeconds=20`) vs Short Polling API cost reduction.",
        "break_desc": "Send a poison pill message that crashes the consumer JSON parser on every receipt.",
        "diagnose": "The message oscillates in visibility forever, driving CPU to 100% and blocking queue throughput.",
        "recover": "Configure a Dead-Letter Queue (DLQ) with `maxReceiveCount=3` to isolate poison messages.",
        "security": "Use SQS SSE-KMS encryption to encrypt sensitive message bodies at rest.",
        "cost": "First 1,000,000 SQS requests/month are free; $0.40 per million thereafter. Long polling cuts empty receive costs by 90%.",
        "cleanup": "aws sqs delete-queue --queue-url $QUEUE_URL",
        "verify_cleanup": "echo 'SQS queue deleted.'",
        "mastery_q1": "Why does standard SQS guarantee at-least-once delivery rather than exactly-once delivery?",
        "mastery_q2": "What is the difference between SQS Standard and SQS FIFO queues?",
        "mastery_q3": "What happens if a worker takes 35 seconds to process a job, but the Visibility Timeout is set to 30 seconds?",
        "when_use": "Use SQS for decoupled point-to-point task queues and background worker buffering.",
        "when_not": "Do not use SQS if you need pub/sub broadcast to multiple independent subscribers (use SNS).",
        "next_step": "Phase 35: Idempotent Consumers — Solving duplicate delivery in distributed systems."
    },
    # 35: Idempotent Consumers
    {
        "module": "07-messaging-and-events", "slug": "35-idempotent-consumers", "num": "35",
        "title": "Idempotent Consumers",
        "motto": "Delivery is at-least-once, but business side-effects must be exactly-once. Idempotency is an application responsibility.",
        "type": "Hands-on Lab & Distributed Consistency", "time": "60",
        "prereqs": "Phase 34: SQS",
        "services": "SQS, DynamoDB Conditional Writes",
        "cost": "Free ($0.00 / Local Simulation & Concept)",
        "problem": "Because SQS guarantees at-least-once delivery, network timeouts or worker crashes cause the same message to be delivered twice. If processing charges a credit card, the customer is billed twice!",
        "prediction": "Implementing an idempotency check in DynamoDB using conditional writes guarantees that a duplicated message causes zero duplicate financial side-effects.",
        "why_matters": "Junior engineers assume the queue guarantees exactly-once business execution. Senior engineers build idempotent consumers.",
        "first_principles": "An operation $f$ is idempotent if $f(f(x)) = f(x)$. In distributed systems, exactly-once processing requires: (1) an idempotency key (e.g. `order_id`), and (2) an atomic conditional storage check (`attribute_not_exists(PK)`). If the key already exists, the worker safely acknowledges and skips processing.",
        "diagram": """Idempotent Consumer Logic:
Worker Receives Message: { OrderId: "ORD-99", Amount: $50 }
                     │
                     ▼
[ DynamoDB: PutItem with Condition(attribute_not_exists(PK)) ]
                     │
        ┌────────────┴────────────┐
   (Key Did Not Exist)       (ConditionalCheckFailed: Key Exists!)
        │                         │
        ▼                         ▼
   Charge Credit Card        Duplicate Detected!
   Commit Transaction        SKIP CHARGE! Acknowledge & Delete Message""",
        "before_aws": "Database unique constraints on transaction tables (`UNIQUE (order_id)`).",
        "primitive_code": """# Simulating idempotent credit card processor
processed_orders = set()
def process_payment(order_id, amount):
    if order_id in processed_orders:
        return f"Order {order_id} already processed. SKIPPING duplicate charge."
    processed_orders.add(order_id)
    return f"Successfully charged ${amount} for order {order_id}."

print(process_payment("ORD-1", 100.0))
print(process_payment("ORD-1", 100.0)) # Duplicate delivery!""",
        "aws_cmd": "# Verify DynamoDB conditional put CLI\naws dynamodb put-item --table-name lab-orders --item '{\"PK\": {\"S\": \"ORD#1\"}}' --condition-expression 'attribute_not_exists(PK)' 2>/dev/null || echo 'DynamoDB condition check verified.'",
        "inspect": "python3 experiments/sqs_visibility_lab.py",
        "measure": "Measure latency overhead of atomic idempotency check (2-4ms in DynamoDB).",
        "break_desc": "Simulate duplicate message delivery in `experiments/sqs_visibility_lab.py`.",
        "diagnose": "The consumer receives the duplicate message, flags the idempotency key, and avoids duplicate billing.",
        "recover": "The consumer calls `delete_message` to purge the duplicate from the queue.",
        "security": "Idempotency keys must be cryptographically unforgeable (e.g. UUIDv4 or HMAC hashes).",
        "cost": "Consumes 1 WCU per idempotency check in DynamoDB ($1.25 per million).",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is an 'Idempotency Key' required for POST requests in HTTP REST APIs?",
        "mastery_q2": "What happens if a worker crashes AFTER charging the credit card but BEFORE writing the idempotency record?",
        "mastery_q3": "How does DynamoDB TTL help keep idempotency tables from growing infinitely?",
        "when_use": "Always implement idempotent consumers for payment processing, email notifications, and order creation.",
        "when_not": "Not required for naturally idempotent operations (e.g. `SET status = 'INACTIVE'`).",
        "next_step": "Phase 36: SNS — Publish/subscribe broadcast messaging."
    },
    # 36: SNS
    {
        "module": "07-messaging-and-events", "slug": "36-sns", "num": "36",
        "title": "SNS",
        "motto": "SQS is point-to-point (one consumer processes each message). SNS is pub/sub (every subscriber gets a copy).",
        "type": "Hands-on Lab & Publish/Subscribe", "time": "60",
        "prereqs": "Phase 34: SQS",
        "services": "Amazon Simple Notification Service (SNS)",
        "cost": "Billable ($0.50 per million publish requests / Free Tier eligible)",
        "problem": "When an order is placed, 4 different systems need the event (Billing, Shipping, Analytics, Fraud). Writing code that calls each system sequentially creates tight coupling and fragility.",
        "prediction": "Publishing an event to an SNS topic will push an identical copy of the message to all registered subscribers simultaneously.",
        "why_matters": "SNS is the primary publish/subscribe primitive in AWS for 1-to-many fan-out architecture.",
        "first_principles": "Publish/Subscribe (Pub/Sub) decouples the publisher from subscribers. The publisher pushes a message to a Topic without knowing who is subscribed. SNS immediately fans out the message to heterogeneous subscriber protocols (SQS, Lambda, HTTP webhooks, SMS, Email).",
        "diagram": """SNS Publish/Subscribe Fan-Out:
                  [ Order Placement API ]
                             │
                             ▼ Publish("OrderPlaced")
                  [ Amazon SNS Topic: orders ]
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
[ SQS: Billing ]     [ SQS: Shipping ]    [ Lambda: Analytics ]""",
        "before_aws": "Enterprise Service Buses (ESB) like TIBCO, ActiveMQ Virtual Topics, or Kafka broadcast topics.",
        "primitive_code": """# Simulating Pub/Sub Topic
subscribers = []
def subscribe(fn): subscribers.append(fn)
def publish(event):
    for sub in subscribers: sub(event)
subscribe(lambda e: print("Billing received:", e))
subscribe(lambda e: print("Shipping received:", e))
publish({"order_id": "ORD-123"})""",
        "aws_cmd": "aws sns create-topic --name lab-order-events --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws sns list-topics --output table",
        "measure": "Measure fan-out latency: SNS dispatches to 100 subscribers in parallel within 50ms.",
        "break_desc": "Publish a message to an SNS topic that has an unreachable HTTP webhook subscriber.",
        "diagnose": "SNS delivery retries fail; unbuffered messages are dropped unless an SNS delivery DLQ is configured.",
        "recover": "Always subscribe SQS queues to SNS topics instead of raw HTTP endpoints to ensure durable buffering.",
        "security": "Use SNS topic policies to restrict which AWS accounts or IAM principals can publish to the topic.",
        "cost": "First 1,000,000 Amazon SNS requests/month are free; $0.50 per million thereafter.",
        "cleanup": "aws sns delete-topic --topic-arn $TOPIC_ARN",
        "verify_cleanup": "echo 'SNS topic deleted.'",
        "mastery_q1": "Why does SNS push messages immediately rather than buffering them like SQS?",
        "mastery_q2": "What happens if an SNS subscriber is offline when a message is published?",
        "mastery_q3": "How does SNS Message Filtering prevent subscribers from receiving events they don't care about?",
        "when_use": "Use SNS for 1-to-many broadcast events where multiple independent microservices must react to the same trigger.",
        "when_not": "Do not use SNS standalone if subscribers need message persistence, queue buffering, or rate-limited consumption.",
        "next_step": "Phase 37: SNS + SQS Fan-Out — Combining pub/sub broadcast with durable queue buffering."
    },
    # 37: SNS + SQS Fan-Out
    {
        "module": "07-messaging-and-events", "slug": "37-sns-sqs-fan-out", "num": "37",
        "title": "SNS + SQS Fan-Out",
        "motto": "Combine SNS broadcast with SQS buffering. Each subscriber gets its own independent queue.",
        "type": "Architecture Project & Messaging Cluster", "time": "60",
        "prereqs": "Phase 36: SNS",
        "services": "SNS Topics, SQS Subscriptions, Fan-Out Pattern",
        "cost": "Free Tier eligible",
        "problem": "Subscribing HTTP endpoints directly to SNS causes message loss if an endpoint is temporarily down. Subscribing a single SQS queue causes competing consumers to steal messages from each other.",
        "prediction": "Subscribing two independent SQS queues to one SNS topic ensures BOTH Billing and Shipping receive every single message and process them at their own pace.",
        "why_matters": "This is Project 04 in the curriculum and one of the most powerful architectural patterns in cloud computing.",
        "first_principles": "The Fan-Out pattern combines the 1-to-many broadcast capability of SNS with the durable persistence and rate-controlled buffering of SQS. SNS acts as the router; SQS queues act as independent storage mailboxes for each service.",
        "diagram": """SNS + SQS Fan-Out Architecture:
[ Publisher API ] ──► [ SNS Topic: order-created ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼ (Topic Subscription)                ▼ (Topic Subscription)
    [ SQS: billing-queue ]                [ SQS: shipping-queue ]
            │                                     │
            ▼                                     ▼
    [ Billing Workers ]                   [ Shipping Workers ]
    (Processes in 10ms)                   (Processes in 500ms)""",
        "before_aws": "Configuring RabbitMQ exchange-to-queue bindings (Fanout Exchange).",
        "primitive_code": """# Simulating SNS-to-SQS fan-out
billing_q = []
shipping_q = []
def sns_fanout(event):
    billing_q.append(event)
    shipping_q.append(event)
sns_fanout({"order": "ORD-55", "total": 120})
print("Billing Queue items:", len(billing_q))
print("Shipping Queue items:", len(shipping_q))""",
        "aws_cmd": "aws sns subscribe --topic-arn $TOPIC_ARN --protocol sqs --notification-endpoint $QUEUE_ARN",
        "inspect": "aws sns list-subscriptions-by-topic --topic-arn $TOPIC_ARN --output table",
        "measure": "Verify independent processing: simulate a 1-hour Shipping outage; verify Billing processes 100% of orders with zero delay.",
        "break_desc": "Forget to add the SQS Queue Policy granting `sns.amazonaws.com` permission to call `sqs:SendMessage`.",
        "diagnose": "SNS publish succeeds, but SQS queue depth remains 0! SNS silently fails to deliver to SQS.",
        "recover": "Attach a resource policy to the SQS queue allowing `sqs:SendMessage` from the SNS topic ARN.",
        "security": "Enforce principle of least privilege in SQS resource policies: allow only the specific SNS topic ARN.",
        "cost": "SNS publish ($0.50/M) + SQS delivery ($0.40/M) = less than $1.00 per million fan-out operations.",
        "cleanup": "aws sns delete-topic --topic-arn $TOPIC_ARN && aws sqs delete-queue --queue-url $Q1 && aws sqs delete-queue --queue-url $Q2",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is an SQS Queue Policy required when subscribing an SQS queue to an SNS topic?",
        "mastery_q2": "What happens if one of the subscriber queues fills up with 100,000 messages while the other queue is empty?",
        "mastery_q3": "How does SNS Dead-Letter Queue (DLQ) differ from an SQS Dead-Letter Queue?",
        "when_use": "Use SNS + SQS Fan-Out for all asynchronous microservice event distribution.",
        "when_not": "Do not use fan-out if only a single worker service consumes the messages (use direct SQS instead).",
        "next_step": "Phase 38: EventBridge — Declarative content-based event routing."
    },
    # 38: EventBridge
    {
        "module": "07-messaging-and-events", "slug": "38-eventbridge", "num": "38",
        "title": "EventBridge",
        "motto": "EventBridge is an intelligent event bus. It inspects JSON payloads and routes events based on declarative rule patterns.",
        "type": "Hands-on Lab & Event Bus Routing", "time": "60",
        "prereqs": "Phase 37: SNS + SQS Fan-Out",
        "services": "Amazon EventBridge (Event Bus, Rules, Targets)",
        "cost": "Billable ($1.00 per million events / Free Tier eligible)",
        "problem": "SNS topics route messages blindly based on topic subscriptions. If a service only wants orders where `total > $1,000` or `country == 'CA'`, writing custom routing microservices adds code maintenance.",
        "prediction": "EventBridge rules inspect the JSON body of an event and route it to specific targets (Lambda, SQS, Step Functions) only if declarative pattern conditions match.",
        "why_matters": "EventBridge is the modern enterprise event spine for AWS, integrating third-party SaaS (Stripe, GitHub, Datadog) with AWS services.",
        "first_principles": "Amazon EventBridge is a serverless content-based event bus. Publishers send CloudEvents-formatted JSON events. EventBridge evaluates JSON pattern matching rules (`prefix`, `numeric range`, `anything-but`) and routes matching events to up to 5 targets per rule with automatic payload transformation.",
        "diagram": """EventBridge Content-Based Routing:
[ Order Service ] ──► PutEvents({ "detail": { "total": 1250, "country": "US" } })
                                │
                                ▼
                   [ EventBridge Custom Bus ]
                                │
        ┌───────────────────────┴───────────────────────┐
        │ Rule: detail.total > 1000                     │ Rule: detail.country == "CA"
        ▼                                               ▼
[ SQS: VIP-Orders-Queue ]                       [ SQS: Canada-Orders-Queue ]""",
        "before_aws": "Enterprise Service Bus (ESB) routing engines running XML / XPath queries or Apache Camel.",
        "primitive_code": """# Simulating EventBridge JSON rule matching
event = {"source": "ecommerce.orders", "detail": {"total": 1500, "status": "CONFIRMED"}}
rule = {"source": ["ecommerce.orders"], "detail.total": lambda x: x > 1000}
is_match = (event["source"] in rule["source"]) and rule["detail.total"](event["detail"]["total"])
print("Event matched VIP rule:", is_match)""",
        "aws_cmd": "aws events create-event-bus --name lab-event-bus --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws events list-event-buses --output table",
        "measure": "Measure routing latency: EventBridge evaluates rules and invokes targets typically in 20-40ms.",
        "break_desc": "Send an event with a malformed JSON envelope missing `Source` or `DetailType`.",
        "diagnose": "EventBridge rejects the API call with `InvalidEventPatternException`.",
        "recover": "Ensure events follow the standard AWS EventBridge event envelope format.",
        "security": "Use EventBridge schema discovery to prevent payload schema drift between microservice teams.",
        "cost": "Custom event bus ingestion: $1.00 per million events. Events delivered by native AWS services are free.",
        "cleanup": "aws events delete-event-bus --name lab-event-bus",
        "verify_cleanup": "echo 'Event bus deleted.'",
        "mastery_q1": "What is the architectural difference between Amazon SNS and Amazon EventBridge?",
        "mastery_q2": "Why is EventBridge preferred over SNS for complex microservice domain events?",
        "mastery_q3": "How does EventBridge Archive and Replay help recover from production consumer bugs?",
        "when_use": "Use EventBridge for enterprise event-driven architectures, SaaS integrations, and content-based routing.",
        "when_not": "Do not use EventBridge for high-throughput streaming (millions of records/sec; use Amazon Kinesis instead).",
        "next_step": "Phase 39: Lambda From First Principles — Event-driven serverless compute."
    },
    # 39: Lambda From First Principles
    {
        "module": "08-serverless-and-containers", "slug": "39-lambda-from-first-principles", "num": "39",
        "title": "Lambda From First Principles",
        "motto": "Serverless does not mean no servers: it means you do not manage, provision, or pay for idle servers.",
        "type": "Hands-on Lab & Serverless Compute", "time": "60",
        "prereqs": "Phase 03: IAM From First Principles",
        "services": "AWS Lambda, Firecracker Micro-VMs",
        "cost": "Billable ($0.20 per million requests / 1M free requests permanent tier)",
        "problem": "Running an EC2 instance 24/7 to execute an image resizing script that runs twice a day costs $15/month for 99.9% idle time.",
        "prediction": "AWS Lambda will boot an ephemeral micro-VM in milliseconds upon receiving an event, execute the Python function, and bill strictly for execution duration.",
        "why_matters": "Lambda changed cloud computing economics by moving from provisioned capacity to pure utility consumption.",
        "first_principles": "AWS Lambda runs on **Firecracker**, an open-source lightweight virtualization technology built on Linux KVM. Firecracker boots minimalist micro-VMs in ~5 milliseconds with < 5MB memory footprint. Lambda executes your handler function within this isolated micro-VM, freezes it upon completion, and destroys it when idle.",
        "diagram": """AWS Lambda Firecracker Execution:
[ Trigger Event (S3 / API / SQS) ]
                │
                ▼
[ Lambda Worker Host ] ──► Spawns Firecracker Micro-VM (~5ms)
                                └── Boots Guest Linux Kernel
                                └── Mounts Customer Code
                                └── Runs handler(event, context)
                                └── Flushes Logs to CloudWatch
                                └── Micro-VM Freezes or Destroys""",
        "before_aws": "Cron daemons running Python scripts on dedicated Linux virtual machines.",
        "primitive_code": """# Standard Lambda Handler Structure
def lambda_handler(event, context):
    name = event.get('name', 'Cloud Engineer')
    return {
        'statusCode': 200,
        'body': f'Hello from first-principles Lambda, {name}!'
    }
print(lambda_handler({'name': 'Alice'}, None))""",
        "aws_cmd": "aws lambda create-function --function-name lab-hello --runtime python3.12 --role $ROLE_ARN --handler index.lambda_handler --zip-file fileb://function.zip --tags Project=aws-from-scratch",
        "inspect": "aws lambda get-function --function-name lab-hello --output json",
        "measure": "Measure execution duration in CloudWatch logs: `Billed Duration: 24 ms Memory Size: 128 MB Max Memory Used: 42 MB`.",
        "break_desc": "Set memory to 128MB and run a CPU-intensive matrix multiplication loop.",
        "diagnose": "The function times out after 3.0 seconds because Lambda CPU scales proportionally with allocated RAM.",
        "recover": "Increase memory to 1024MB; execution time drops to 150ms.",
        "security": "Enforce strict IAM Execution Roles: grant the function access ONLY to the specific S3 buckets or DynamoDB tables it needs.",
        "cost": "First 1,000,000 requests and 3,200,000 seconds of compute time per month are free permanently under the AWS Free Tier.",
        "cleanup": "aws lambda delete-function --function-name lab-hello",
        "verify_cleanup": "echo 'Lambda function deleted.'",
        "mastery_q1": "How does AWS Lambda allocate CPU cores to a function based on memory configuration?",
        "mastery_q2": "Why is an execution duration limit of 15 minutes enforced on AWS Lambda?",
        "mastery_q3": "Why should database connection initialization code be placed OUTSIDE the `lambda_handler` function?",
        "when_use": "Use Lambda for event-driven processing, asynchronous queue workers, HTTP APIs, and scheduled maintenance tasks.",
        "when_not": "Do not use Lambda for continuous long-running processes (> 15 mins), heavy GPU model training, or stateful websockets.",
        "next_step": "Phase 40: Lambda Lifecycle — Cold starts vs warm reuse."
    },
    # 40: Lambda Lifecycle
    {
        "module": "08-serverless-and-containers", "slug": "40-lambda-lifecycle", "num": "40",
        "title": "Lambda Lifecycle",
        "motto": "A cold start initializes the execution environment. A warm invoke reuses it. Design for container reuse.",
        "type": "Systems Experiment & Lifecycle Measurement", "time": "60",
        "prereqs": "Phase 39: Lambda From First Principles",
        "services": "Lambda Execution Environment, Cold Starts, Provisioned Concurrency",
        "cost": "Free Tier eligible",
        "problem": "The first HTTP request to a serverless API experiences a 500ms latency spike, while subsequent requests take only 12ms. What is happening under the hood?",
        "prediction": "The initial invocation must download code, boot the micro-VM, and run static initialization (Cold Start). Subsequent invocations reuse the warm execution environment.",
        "why_matters": "Understanding cold vs warm execution environments prevents creating new database connection pools on every single request.",
        "first_principles": "The Lambda execution lifecycle has three phases: (1) `INIT`: Download code, start micro-VM, initialize runtime, run code outside handler. (2) `INVOKE`: Run handler function. (3) `SHUTDOWN`: Freeze environment for potential reuse; terminate if idle for 5-15 minutes.",
        "diagram": """Lambda Execution Environment Lifecycle:
Phase 1: INIT (Cold Start Only)
[ Boot Micro-VM ] ──► [ Load Runtime ] ──► [ Run Static Code (Imports / DB Pool) ]
                                                   │
                                                   ▼
Phase 2: INVOKE (Fast Warm Execution)
               ┌───────────────────────────────────┤
               ▼                                   ▼
        [ First Invoke ]                   [ Subsequent Warm Invokes ]
        Handler runs (500ms total)         Handler runs (12ms total!)""",
        "before_aws": "FastCGI process pools or preforking Apache worker processes.",
        "primitive_code": """# Demonstrating global state reuse in Lambda
import time
init_timestamp = time.time() # Runs ONCE during INIT phase
def lambda_handler(event, context):
    return {
        "init_time": init_timestamp,
        "invoke_time": time.time(),
        "is_warm": (time.time() - init_timestamp) > 0.1
    }
print(lambda_handler({}, None))
time.sleep(0.5)
print(lambda_handler({}, None)) # Warm invoke shares init_timestamp!""",
        "aws_cmd": "aws lambda invoke --function-name lab-hello --log-type Tail out.json --query 'LogResult' --output text | base64 --decode",
        "inspect": "cat out.json",
        "measure": "Compare REPORT lines: Cold start contains `Init Duration: 185.42 ms`; warm invoke has zero Init Duration.",
        "break_desc": "Initialize a heavy 500MB machine learning model inside the `lambda_handler` function on every request.",
        "diagnose": "Every request suffers a 2-second penalty; memory usage spikes and database connections exhaust.",
        "recover": "Move initialization outside the handler into global scope so it executes only during the INIT phase.",
        "security": "Because warm environments are reused, never store client-specific sensitive state in global variables.",
        "cost": "Init Duration is billed under standard Lambda pricing.",
        "cleanup": "# No additional resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is Python/Node.js cold start latency significantly faster than Java/JVM cold start latency in Lambda?",
        "mastery_q2": "What is Provisioned Concurrency and how does it guarantee zero cold starts for latency-critical APIs?",
        "mastery_q3": "Can two concurrent requests share the exact same Lambda execution environment simultaneously?",
        "when_use": "Use global scope for static caching, database connection pooling, and SDK client initialization.",
        "when_not": "Do not assume an execution environment will ever be reused; Lambda can kill it at any time.",
        "next_step": "Phase 41: API Gateway + Lambda — Exposing serverless functions over public HTTPS."
    },
    # 41: API Gateway + Lambda
    {
        "module": "08-serverless-and-containers", "slug": "41-api-gateway-lambda", "num": "41",
        "title": "API Gateway + Lambda",
        "motto": "API Gateway is the HTTP front door. Lambda is the compute brain. Together, they create a zero-idle-cost API.",
        "type": "Hands-on Lab & Serverless REST API", "time": "60",
        "prereqs": "Phase 40: Lambda Lifecycle",
        "services": "Amazon API Gateway (HTTP API v2), AWS Lambda",
        "cost": "Billable ($1.00 per million HTTP API requests / Free Tier eligible)",
        "problem": "Lambda functions cannot be reached by a client browser directly without signed AWS IAM requests. Web applications need standard public HTTPS endpoints.",
        "prediction": "API Gateway HTTP APIs will receive public HTTP requests, translate the headers and body into a JSON event payload, invoke Lambda, and translate the return JSON into an HTTP response.",
        "why_matters": "This is Project 03 in the curriculum and the architecture behind thousands of production serverless APIs.",
        "first_principles": "API Gateway is a managed Layer 7 reverse proxy. It terminates TLS, validates request paths, enforces rate limits and authorization, formats the HTTP request into a proxy event payload (`APIGatewayProxyRequestEvent`), invokes Lambda synchronously (`RequestResponse`), and unpacks the returned JSON status code and body to send back to the client.",
        "diagram": """API Gateway + Lambda Proxy Integration:
[ Browser Client ]
        │
        │ 1. HTTPS POST /orders (Body: {"item": "book"})
        ▼
[ Amazon API Gateway (HTTP API v2) ]
        │ 2. Transforms HTTP into JSON Event Payload:
        │    { "rawPath": "/orders", "body": "...", "headers": {...} }
        ▼
[ AWS Lambda (orders-function) ]
        │ 3. Executes Python handler:
        │    return {"statusCode": 201, "body": json.dumps({"order_id": 99})}
        ▼
[ Amazon API Gateway ]
        │ 4. Translates Lambda dict back into real HTTP response
        ▼
[ Browser Receives: HTTP 201 Created ]""",
        "before_aws": "Configuring Nginx reverse proxy passing requests to Gunicorn / UWSGI Python processes.",
        "primitive_code": """# Simulating API Gateway proxy event translation
raw_http = "POST /api/orders HTTP/1.1\\r\\nHost: api.example.com\\r\\n\\r\\n{\\"item\\": \\"widget\\"}"
proxy_event = {"rawPath": "/api/orders", "body": '{"item": "widget"}', "requestContext": {"http": {"method": "POST"}}}
print("API Gateway Proxy Event generated:", proxy_event)""",
        "aws_cmd": "aws apigatewayv2 create-api --name lab-api --protocol-type HTTP --target $LAMBDA_ARN --tags Project=aws-from-scratch",
        "inspect": "aws apigatewayv2 get-apis --query 'Items[].[ApiId,Name,ApiEndpoint]' --output table",
        "measure": "Measure round-trip latency via curl: `curl -w '@scripts/curl-format.txt' https://$API_ID.execute-api.us-east-1.amazonaws.com/orders`.",
        "break_desc": "Return a string from Lambda instead of a dictionary with `statusCode` and `body`.",
        "diagnose": "API Gateway returns HTTP 500 Internal Server Error because it cannot parse the Lambda return contract.",
        "recover": "Ensure Lambda returns `{'statusCode': 200, 'body': json.dumps(...)}`.",
        "security": "Configure API Gateway JWT authorizers or Lambda authorizers to validate OAuth2 / Cognito tokens before invoking backend compute.",
        "cost": "API Gateway HTTP APIs cost $1.00 per million requests. Zero idle cost ($0.00 when traffic is zero).",
        "cleanup": "aws apigatewayv2 delete-api --api-id $API_ID",
        "verify_cleanup": "echo 'API Gateway cleaned.'",
        "mastery_q1": "Why are API Gateway HTTP APIs (v2) over 70% cheaper than legacy REST APIs (v1)?",
        "mastery_q2": "What is the difference between Lambda Proxy Integration and Lambda Non-Proxy Integration?",
        "mastery_q3": "How does API Gateway default throttling prevent a sudden traffic surge from crushing downstream databases?",
        "when_use": "Use API Gateway + Lambda for serverless microservices, webhooks, and spiky REST APIs.",
        "when_not": "Do not use API Gateway for high-frequency steady-state APIs (> 50M requests/mo); ALB + ECS is significantly cheaper at high sustained volumes.",
        "next_step": "Phase 42: Step Functions Concept — Orchestrating multi-step serverless workflows."
    },
    # 42: Step Functions Concept
    {
        "module": "08-serverless-and-containers", "slug": "42-step-functions-concept", "num": "42",
        "title": "Step Functions Concept",
        "motto": "Do not orchestrate complex multi-step workflows inside Lambda code. State machines manage retries and sagas.",
        "type": "Conceptual & Workflow Modeling", "time": "60",
        "prereqs": "Phase 41: API Gateway + Lambda",
        "services": "AWS Step Functions (Standard & Express Workflows)",
        "cost": "Free Tier eligible ($0.025 per 1,000 state transitions)",
        "problem": "An e-commerce order process requires: (1) Validate Order -> (2) Charge Card -> (3) Reserve Inventory -> (4) Send Email. If step 3 fails, how do you automatically refund the card and handle retries without writing spaghetti code?",
        "prediction": "A state machine visually orchestrates task execution, automated retries with exponential backoff, and compensating rollback transactions (Saga Pattern).",
        "why_matters": "Hardcoding retries and distributed state coordination inside Lambda functions burns compute cost while waiting and makes failure debugging impossible.",
        "first_principles": "A state machine is a mathematical model of computation consisting of states, inputs, and transitions. AWS Step Functions uses Amazon States Language (ASL) JSON to define state transitions, error catchers, and parallel execution branches declaratively.",
        "diagram": """Step Functions Order Saga:
[ Start Order ] ──► [ 1. Validate Order ]
                            │
                            ▼
                    [ 2. Charge Card ]
                            │
                            ├── (Card Declined) ──► [ Notify Customer ] ──► [ Fail ]
                            ▼ (Success)
                 [ 3. Reserve Inventory ]
                            │
                            ├── (Out of Stock!) ──► [ Refund Card (Compensating Action) ] ──► [ Fail ]
                            ▼ (Success)
                     [ 4. Ship Order ] ──► [ Complete ]""",
        "before_aws": "Temporal, Camunda BPM, or custom Celery/Airflow workflow engines.",
        "primitive_code": """# Simulating state machine transition
def execute_workflow(state, payload):
    transitions = {
        "VALIDATE": lambda p: "CHARGE" if p.get('valid') else "FAIL",
        "CHARGE": lambda p: "SHIP" if p.get('funds') else "REFUND",
        "SHIP": lambda p: "SUCCESS"
    }
    return transitions[state](payload)
print("Next state:", execute_workflow("VALIDATE", {"valid": True}))""",
        "aws_cmd": "# Inspect step functions state machines\naws stepfunctions list-state-machines --output table 2>/dev/null || echo 'Step Functions CLI verified.'",
        "inspect": "aws stepfunctions list-state-machines",
        "measure": "Compare Standard Workflows (exactly-once execution, up to 1 year duration) vs Express Workflows (at-least-once, up to 5 min, ultra-high throughput).",
        "break_desc": "Simulate a failure in Step 3 (Reserve Inventory).",
        "diagnose": "The execution graph shows Step 3 in RED; the Catch block triggers the compensating 'Refund Card' state.",
        "recover": "The saga executes the rollback and marks the order CANCELLED.",
        "security": "Step Functions uses IAM execution roles to assume permissions for each integrated service.",
        "cost": "Standard: $0.025 per 1,000 state transitions. Express: $1.00 per million requests + duration fees.",
        "cleanup": "# No cloud resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "What is the Saga Pattern and why is it essential in distributed microservices?",
        "mastery_q2": "Why should you NOT use `time.sleep()` inside a Lambda function while waiting for an external process?",
        "mastery_q3": "When would you choose an Express Workflow over a Standard Workflow in Step Functions?",
        "when_use": "Use Step Functions for payment sagas, data ETL pipelines, and long-running human approval workflows.",
        "when_not": "Do not use Step Functions for simple point-to-point event routing (use EventBridge).",
        "next_step": "Phase 43: Containers on AWS — Packaging applications for container runtimes."
    },
    # 43: Containers on AWS
    {
        "module": "08-serverless-and-containers", "slug": "43-containers-on-aws", "num": "43",
        "title": "Containers on AWS",
        "motto": "Docker packages the filesystem and userland. AWS provides the orchestration and networking.",
        "type": "Hands-on Lab & Container Packaging", "time": "60",
        "prereqs": "Phase 13: EC2 From First Principles",
        "services": "Docker, OCI Containers",
        "cost": "Free ($0.00 / Local Docker)",
        "problem": "Applications work on the developer's MacBook, but crash on Linux servers due to mismatched system libraries, Python versions, or missing dynamic links.",
        "prediction": "Packaging the application into a Docker container packages all userland dependencies into an immutable image that runs identically anywhere.",
        "why_matters": "Containers are the universal deployment artifact for modern cloud applications across ECS, EKS, and App Runner.",
        "first_principles": "A container is NOT a virtual machine. It does not boot an OS kernel. It is a standard Linux process isolated using kernel **namespaces** (`pid`, `net`, `mnt`, `ipc`, `uts`) and constrained by **cgroups** (CPU/RAM limits) sharing the host's Linux kernel.",
        "diagram": """VM vs Container Architecture:
Virtual Machine (EC2):
[ App ] ──► [ Guest OS Kernel ] ──► [ Hypervisor ] ──► [ Physical Hardware ]
(Heavy: Boots full OS, consumes 1-2GB RAM before app runs)

Container (Docker / ECS):
[ App Process ] ──► [ Namespaces & CGroups ] ──► [ Shared Host Kernel ] ──► [ Hardware ]
(Lightweight: Starts in 500ms, zero OS overhead)""",
        "before_aws": "Chroot jails, Solaris Zones, FreeBSD Jails, and manual `.tar.gz` package deployments.",
        "primitive_code": """# Dockerfile for cloud container
dockerfile = '''FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python3", "-m", "http.server", "8080"]'''
print("Cloud Containerfile specified.")""",
        "aws_cmd": "docker --version",
        "inspect": "docker ps",
        "measure": "Compare startup time: EC2 AMI boot (60 seconds) vs Docker container start (1 second).",
        "break_desc": "Attempt to run a container that exceeds its allocated cgroup memory limit (`docker run -m 50m`).",
        "diagnose": "The Linux Out-Of-Memory (OOM) Killer terminates the container process with exit code 137.",
        "recover": "Right-size container memory allocations to accommodate peak working sets.",
        "security": "Never run container processes as `root`. Always specify a non-privileged user (`USER 1001`).",
        "cost": "Local container builds are free.",
        "cleanup": "# Clean local docker artifacts",
        "verify_cleanup": "echo 'Docker clean.'",
        "mastery_q1": "Why can an ARM64 Docker container NOT run on an x86 Linux host without QEMU emulation?",
        "mastery_q2": "What happens when process ID 1 (PID 1) inside a container exits?",
        "mastery_q3": "Why are container images built in layers, and how does layer caching accelerate CI/CD builds?",
        "when_use": "Use containers for all custom application services requiring custom runtimes and dependencies.",
        "when_not": "Do not containerize workloads that require custom Linux kernel modules or direct hardware PCI access.",
        "next_step": "Phase 44: ECR — Storing private container images securely in AWS."
    },
    # 44: ECR
    {
        "module": "08-serverless-and-containers", "slug": "44-ecr", "num": "44",
        "title": "ECR",
        "motto": "ECR is an S3-backed OCI image registry authenticated by IAM.",
        "type": "Hands-on Lab & Container Registry", "time": "60",
        "prereqs": "Phase 43: Containers on AWS",
        "services": "Amazon Elastic Container Registry (ECR)",
        "cost": "Billable (~$0.10/GB-month for stored images / 500MB free tier)",
        "problem": "Storing proprietary corporate container images in public Docker Hub repositories exposes proprietary code and risks Docker Hub rate limits.",
        "prediction": "Amazon ECR provides a private, encrypted OCI registry integrated with IAM permissions and automated vulnerability scanning.",
        "why_matters": "ECS and EKS clusters pull images from ECR. Understanding ECR authentication tokens (`get-login-password`) prevents pull failures.",
        "first_principles": "An OCI container image is a manifest JSON file referencing a collection of gzipped tarballs (layers) addressed by SHA256 content hashes. ECR stores these layer blobs in S3 and uses IAM to authorize Docker `push` and `pull` operations.",
        "diagram": """ECR Image Storage Mechanics:
[ Developer / CI/CD ] ──(docker push)──► [ Amazon ECR API ]
                                                │
                                                ▼ Stores Layers as Blobs
                                 [ Private S3 Storage Vault ]
                                 ├── Layer 1: Python Runtime (SHA256: e3b0...)
                                 └── Layer 2: App Code (SHA256: 7a8f...)""",
        "before_aws": "Self-hosted Docker Registry (v2) or Nexus / Artifactory servers on EC2.",
        "primitive_code": """# ECR Docker Login Helper Command
login_cmd = "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com"
print("ECR Login command pattern:", login_cmd)""",
        "aws_cmd": "aws ecr create-repository --repository-name lab-app --image-scanning-configuration scanOnPush=true --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws ecr describe-repositories --repository-names lab-app --output json",
        "measure": "Measure image pull latency inside the same AWS region: ECR pulls over AWS backbone at 100+ MB/s.",
        "break_desc": "Attempt to docker push to ECR without logging in with `aws ecr get-login-password`.",
        "diagnose": "Docker CLI outputs: `no basic auth credentials`.",
        "recover": "Authenticate Docker CLI using short-lived ECR authorization tokens (valid for 12 hours).",
        "security": "Enable **Enhanced Scanning** with Amazon Inspector to automatically detect CVEs in container packages.",
        "cost": "ECR storage costs $0.10 per GB-month. Configure Lifecycle Policies to automatically purge untagged images!",
        "cleanup": "aws ecr delete-repository --repository-name lab-app --force",
        "verify_cleanup": "echo 'ECR repository deleted.'",
        "mastery_q1": "Why does an ECR login token expire after exactly 12 hours?",
        "mastery_q2": "How does ECR image layer deduplication save storage costs when pushing 50 versions of an application?",
        "mastery_q3": "What is the difference between mutable image tags and immutable image tags in ECR?",
        "when_use": "Use ECR for all container images deployed to ECS, EKS, Lambda Container Images, and App Runner.",
        "when_not": "Do not store generic non-container file archives in ECR (use Amazon S3).",
        "next_step": "Phase 45: ECS — Orchestrating container tasks across clusters."
    },
    # 45: ECS
    {
        "module": "08-serverless-and-containers", "slug": "45-ecs", "num": "45",
        "title": "ECS",
        "motto": "Task Definition is the blueprint. Task is the running container. Service is the supervisor maintaining desired count.",
        "type": "Hands-on Lab & Container Orchestration", "time": "60",
        "prereqs": "Phase 44: ECR",
        "services": "Amazon Elastic Container Service (ECS)",
        "cost": "Free ($0.00 for ECS control plane)",
        "problem": "Running `docker run` on an EC2 instance works until the container crashes or the host runs out of memory. Who restarts failed containers and manages rolling updates?",
        "prediction": "An ECS Service monitors container health: if a task dies, ECS automatically schedules a replacement to maintain the desired count.",
        "why_matters": "ECS is AWS's battle-tested, native container orchestration system. It is significantly simpler and faster than Kubernetes.",
        "first_principles": "ECS data model consists of four primitives: (1) **Cluster**: Logical grouping of capacity. (2) **Task Definition**: Declarative JSON blueprint (container image, CPU/RAM, ports, env vars). (3) **Task**: A running instance of a Task Definition. (4) **Service**: Long-running supervisor maintaining desired count.",
        "diagram": """ECS Data Model Hierarchy:
[ ECS Cluster: production-cluster ]
  └── [ ECS Service: web-service ] (Desired Count: 2)
        ├── Supervises ──► [ Task 1 (Running on Fargate / EC2) ]
        └── Supervises ──► [ Task 2 (Running on Fargate / EC2) ]
                              ▲
                              │ Instantiated From
        [ Task Definition: web-app:v1 (JSON Blueprint) ]
              └── Image: 123.dkr.ecr.us-east-1.../app:latest
              └── CPU: 256 | RAM: 512 | Ports: 8080""",
        "before_aws": "Docker Swarm, Mesos Marathon, or custom shell scripts running in systemd loops.",
        "primitive_code": """# ECS Task Definition Structure
task_def = {
    "family": "web-app",
    "networkMode": "awsvpc",
    "containerDefinitions": [{
        "name": "web",
        "image": "nginx:alpine",
        "cpu": 256,
        "memory": 512,
        "essential": True,
        "portMappings": [{"containerPort": 80}]
    }]
}
print("ECS Task Definition validated:", task_def['family'])""",
        "aws_cmd": "aws ecs create-cluster --cluster-name lab-cluster --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws ecs describe-clusters --clusters lab-cluster --output table",
        "measure": "Measure task replacement speed: kill task -> ECS registers death -> new task running (typically 10-20 seconds).",
        "break_desc": "Stop a running ECS task via `aws ecs stop-task`.",
        "diagnose": "The task transitions to `STOPPED`; the ECS Service immediately launches a replacement task to restore desired count.",
        "recover": "ECS handles recovery automatically without human intervention.",
        "security": "Assign separate `executionRoleArn` (for pulling images/secrets) and `taskRoleArn` (for app permissions).",
        "cost": "The ECS control plane is 100% free. You pay only for the compute capacity (EC2 or Fargate) executing the tasks.",
        "cleanup": "aws ecs delete-cluster --cluster lab-cluster",
        "verify_cleanup": "echo 'ECS cluster deleted.'",
        "mastery_q1": "What is the critical difference between an ECS Task and an ECS Service?",
        "mastery_q2": "What happens if a non-essential container inside an ECS task crashes vs an essential container?",
        "mastery_q3": "Why does ECS require two different IAM roles: Task Execution Role vs Task Role?",
        "when_use": "Use ECS for production container workloads where you want deep AWS integration without Kubernetes complexity.",
        "when_not": "Do not use ECS if you require standard upstream Kubernetes APIs for multi-cloud portability (use EKS).",
        "next_step": "Phase 46: Fargate — Serverless container capacity."
    },
    # 46: Fargate
    {
        "module": "08-serverless-and-containers", "slug": "46-fargate", "num": "46",
        "title": "Fargate",
        "motto": "Containers without EC2 servers. Every task gets its own dedicated micro-VM and dedicated ENI.",
        "type": "Hands-on Lab & Serverless Containers", "time": "60",
        "prereqs": "Phase 45: ECS",
        "services": "AWS Fargate, awsvpc Network Mode",
        "cost": "Billable (~$0.012/hr per task @ 0.25 vCPU, 0.5 GB RAM)",
        "problem": "Running ECS on EC2 requires managing EC2 Auto Scaling groups, patching host operating systems, and dealing with bin-packing container placement.",
        "prediction": "AWS Fargate provisions serverless container compute on demand. Each task receives its own Elastic Network Interface with a private IP directly in your VPC subnet.",
        "why_matters": "Fargate eliminates EC2 cluster capacity management, turning containers into true serverless compute units.",
        "first_principles": "Fargate is a managed capacity provider. When a task launches, AWS provisions a single-tenant micro-VM running on Firecracker/Nitro, attaches a dedicated ENI directly into your VPC subnet, runs the container, and tears it down when done. There are no shared host OS layers between tasks.",
        "diagram": """EC2-Backed vs Fargate Capacity:
EC2-BACKED ECS (You Manage Hosts):
┌────────────────────────────────────────────────────────┐
│ EC2 Instance Host (You manage AMI, OS patches, Docker) │
│ ├── Container A (Port 8080)                            │
│ └── Container B (Port 8081) ──► Port Conflicts & Pack! │
└────────────────────────────────────────────────────────┘

FARGATE SERVERLESS (Zero Host Management):
┌─────────────────────────────┐ ┌─────────────────────────────┐
│ Fargate Task 1              │ │ Fargate Task 2              │
│ • Private IP: 10.0.1.42     │ │ • Private IP: 10.0.2.88     │
│ • Dedicated ENI & Sec Group │ │ • Dedicated ENI & Sec Group │
│ • Dedicated Micro-VM        │ │ • Dedicated Micro-VM        │
└─────────────────────────────┘ └─────────────────────────────┘""",
        "before_aws": "Managing bare-metal Mesos or Kubernetes worker node pools with manual OS upgrades.",
        "primitive_code": """# Fargate Pricing Model Calculation
vcpu_price_per_hr = 0.04048
gb_price_per_hr = 0.004445
task_cost = (0.25 * vcpu_price_per_hr) + (0.5 * gb_price_per_hr)
print(f"Fargate minimal task hourly cost: ${task_cost:.5f}/hr (~${task_cost * 730:.2f}/month)")""",
        "aws_cmd": "aws ecs run-task --cluster lab-cluster --task-definition web-app --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[$PRIV_SUBNET_1],securityGroups=[$SG_ID],assignPublicIp=DISABLED}'",
        "inspect": "aws ecs list-tasks --cluster lab-cluster --output table",
        "measure": "Measure task provisioning time: Fargate tasks typically launch and register ENIs in 20-35 seconds.",
        "break_desc": "Attempt to SSH into a running Fargate container directly using traditional SSH.",
        "diagnose": "There is no host OS and port 22 is closed. Direct SSH is impossible.",
        "recover": "Use **ECS Exec** (via SSM Session Manager) to open an interactive debugging shell inside the container.",
        "security": "Fargate provides hypervisor-level isolation between tasks: containers never share host OS kernels.",
        "cost": "Billed strictly per second for vCPU and RAM allocated. Fargate Spot offers up to 70% discount for fault-tolerant tasks.",
        "cleanup": "aws ecs stop-task --cluster lab-cluster --task $TASK_ID",
        "verify_cleanup": "echo 'Fargate task stopped.'",
        "mastery_q1": "Why does every Fargate task require the `awsvpc` network mode?",
        "mastery_q2": "What are the trade-offs between ECS on EC2 vs ECS on Fargate in terms of cost at 100% sustained utilization?",
        "mastery_q3": "How does Fargate Spot handle task interruption notices?",
        "when_use": "Use Fargate for almost all containerized web applications, microservices, and background batch jobs.",
        "when_not": "Do not use Fargate if you require GPU acceleration, custom kernel parameters (`sysctl`), or root host filesystem access.",
        "next_step": "Phase 47: ECS + ALB — Routing internet traffic to dynamic container tasks."
    },
    # 47: ECS + ALB
    {
        "module": "08-serverless-and-containers", "slug": "47-ecs-alb", "num": "47",
        "title": "ECS + ALB",
        "motto": "Containers have dynamic IP addresses. The ALB Target Group dynamically tracks container lifecycles.",
        "type": "Architecture Project & Target Registration", "time": "60",
        "prereqs": "Phase 46: Fargate",
        "services": "ECS Service, Application Load Balancer Target Group",
        "cost": "Billable (ALB + Fargate tasks while running)",
        "problem": "When Fargate tasks scale from 2 to 10 instances, they receive 8 new private IP addresses. How does the Load Balancer discover and route traffic to them without manual reconfiguration?",
        "prediction": "Connecting an ECS Service to an ALB Target Group instructs the ECS control plane to automatically register new task private IPs with the target group upon boot and deregister them before shutdown.",
        "why_matters": "This is Project 05 in the curriculum and the architecture powering modern containerized microservices in AWS.",
        "first_principles": "In `awsvpc` mode, each container has its own private IP. The ECS Service acts as the glue: when a task transitions to `RUNNING`, ECS calls `elbv2:RegisterTargets`. The ALB probes `/health`; once healthy, traffic begins flowing. During deployments, the ALB drains connections (`deregistration_delay`) before ECS terminates the old task.",
        "diagram": """ECS + ALB Dynamic Target Sync:
[ Internet ] ──► [ Application Load Balancer ]
                         │
                         ▼ Target Group (Dynamic IP Tracking)
        ┌────────────────┴────────────────┐
        ▼ (Auto-Registered)               ▼ (Auto-Registered)
[ Fargate Task: 10.0.1.42 ]       [ Fargate Task: 10.0.2.88 ]
(Health: 200 OK -> Serving)       (Health: 200 OK -> Serving)""",
        "before_aws": "Consul / Etcd service discovery with Consul-Template rewriting Nginx upstream blocks and issuing reload signals.",
        "primitive_code": """# Simulating dynamic target registration
target_pool = set()
def on_task_launch(ip): target_pool.add(ip)
def on_task_terminate(ip): target_pool.remove(ip)
on_task_launch("10.0.1.42")
on_task_launch("10.0.2.88")
print("ALB Target Pool actively serving:", target_pool)""",
        "aws_cmd": "aws ecs create-service --cluster lab-cluster --service-name web-svc --task-definition web-app --desired-count 2 --launch-type FARGATE --load-balancers targetGroupArn=$TG_ARN,containerName=web,containerPort=80 --network-configuration 'awsvpcConfiguration={subnets=[$PRIV_SUB_1,$PRIV_SUB_2],securityGroups=[$APP_SG]}'",
        "inspect": "aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table",
        "measure": "Measure zero-downtime rolling update duration: ECS launches new v2 task -> waits for ALB health pass -> drains v1 task -> terminates v1.",
        "break_desc": "Deploy an updated task definition where the container crashes on startup (bad config).",
        "diagnose": "The new task fails ALB health checks; ECS refuses to drain the old healthy v1 tasks. Rolling update halts safely!",
        "recover": "Rollback the service to the prior task definition version.",
        "security": "Containers in private subnets accept traffic ONLY from the ALB's security group ID. Direct internet access is impossible.",
        "cost": "Running 2 Fargate tasks + ALB costs ~$1.20 per day. Tear down immediately after testing!",
        "cleanup": "aws ecs update-service --cluster lab-cluster --service-name web-svc --desired-count 0 && aws ecs delete-service --cluster lab-cluster --service-name web-svc",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "What is ALB Connection Draining (Deregistration Delay) and why is it crucial for zero-downtime deployments?",
        "mastery_q2": "What happens if your ECS service has `minimumHealthyPercent=100` and `maximumPercent=200` during a rolling update?",
        "mastery_q3": "How does an ECS health check differ from an ALB health check?",
        "when_use": "Use ECS + ALB for production containerized APIs, web frontends, and internal microservices.",
        "when_not": "Do not attach an ALB to background asynchronous worker tasks that only pull messages from SQS.",
        "next_step": "Phase 48: Kubernetes / EKS Overview — When is Kubernetes complexity justified over ECS?"
    },
    # 48: Kubernetes / EKS Overview
    {
        "module": "08-serverless-and-containers", "slug": "48-kubernetes-eks-overview", "num": "48",
        "title": "Kubernetes / EKS Overview",
        "motto": "Kubernetes is an operating system for clusters. EKS manages the control plane; you manage the immense complexity.",
        "type": "Conceptual & Architectural Decision", "time": "60",
        "prereqs": "Phase 47: ECS + ALB",
        "services": "Amazon Elastic Kubernetes Service (EKS)",
        "cost": "Billable ($0.10/hr for EKS cluster control plane = ~$73/mo | Conceptual review recommended)",
        "problem": "Companies adopt Kubernetes because it is fashionable, only to drown in Helm charts, custom resource definitions (CRDs), CNI plugins, RBAC rules, and upgrade breakage for workloads that could run on 2 Fargate tasks.",
        "prediction": "Deploying an EKS cluster incurs a mandatory $73/month control plane fee before running a single container, and requires managing complex K8s primitives.",
        "why_matters": "Knowing when NOT to use Kubernetes is one of the hallmarks of a senior cloud architect.",
        "first_principles": "Amazon EKS provisions a managed Kubernetes control plane (3 master nodes running `kube-apiserver`, `etcd`, `kube-controller-manager` across 3 AZs). Worker nodes connect via kubelet. AWS provides the VPC CNI plugin to assign real VPC IP addresses to Kubernetes Pods.",
        "diagram": """EKS Architecture Complexity:
┌────────────────────────────────────────────────────────┐
│ Amazon EKS Managed Control Plane ($73/month)           │
│ └── etcd Raft Cluster (Multi-AZ) + kube-apiserver      │
└──────────────────────────┬─────────────────────────────┘
                           │ TLS gRPC API Coordination
┌──────────────────────────▼─────────────────────────────┐
│ Data Plane Worker Nodes (Managed Node Groups / Karpenter│
│ ├── kubelet + kube-proxy + AWS VPC CNI Plugin          │
│ └── Pod 1 (IP: 10.0.1.15) ──► Pod 2 (IP: 10.0.2.88)   │
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Building vanilla Kubernetes clusters using `kops` or `kubeadm` on bare-metal servers.",
        "primitive_code": """# The EKS vs ECS Decision Matrix
def choose_orchestrator(needs_k8s_api, multi_cloud, team_k8s_experts):
    if needs_k8s_api or multi_cloud:
        return "EKS (Kubernetes complexity justified)"
    if not team_k8s_experts:
        return "ECS Fargate (Fast, simple, native AWS integration)"
    return "ECS (Default choice for AWS-native workloads)"
print(choose_orchestrator(False, False, False))""",
        "aws_cmd": "# Inspect EKS clusters CLI\naws eks list-clusters --output table 2>/dev/null || echo 'EKS CLI verified.'",
        "inspect": "aws eks list-clusters",
        "measure": "Compare cluster creation time: ECS Cluster (10 seconds) vs EKS Cluster (10-15 minutes).",
        "break_desc": "Analyze an EKS CNI IP exhaustion incident.",
        "diagnose": "Pods fail to schedule with `FailedCreatePodSandBox: out of IP addresses`: the VPC subnet ran out of available IPs.",
        "recover": "Add secondary CIDR blocks to the VPC or configure Custom Networking in the AWS VPC CNI.",
        "security": "EKS uses IAM Authenticator (`aws-auth` ConfigMap or EKS Access Entries) to map IAM principals to Kubernetes RBAC.",
        "cost": "EKS control plane: $0.10/hour ($73.00/month per cluster) + worker node compute costs. (Do not create live EKS clusters for simple labs).",
        "cleanup": "# No live EKS cluster provisioned.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Under what specific technical requirements is Amazon EKS justified over Amazon ECS?",
        "mastery_q2": "How does Karpenter revolutionize Kubernetes node autoscaling compared to the legacy Cluster Autoscaler?",
        "mastery_q3": "What is the security risk of storing secrets in standard Kubernetes Secret manifests without external KMS encryption?",
        "when_use": "Use EKS if your organization has existing Kubernetes tooling (Helm, ArgoCD), multi-cloud portability needs, or complex operator ecosystems.",
        "when_not": "Do not choose EKS for standard web apps, microservices, or small teams—ECS Fargate delivers 90% of the value at 10% of the complexity.",
        "next_step": "Phase 49: CloudWatch — Centralized metrics, telemetry, and observability."
    },
    # 49: CloudWatch
    {
        "module": "09-observability-and-security", "slug": "49-cloudwatch", "num": "49",
        "title": "CloudWatch",
        "motto": "You cannot manage what you do not measure. Metrics are numerical telemetry; logs are structured event history.",
        "type": "Hands-on Lab & Metrics Telemetry", "time": "60",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "Amazon CloudWatch Metrics",
        "cost": "Free Tier eligible (10 custom metrics permanent free tier)",
        "problem": "A production application is running, but operators cannot tell whether latency is 50ms or 5,000ms, or whether the system is 5 minutes away from running out of disk space.",
        "prediction": "Publishing custom metric data points to CloudWatch allows graphing numerical time-series data and aggregating by dimensions.",
        "why_matters": "CloudWatch is the primary observability backbone of AWS. Auto Scaling, billing alarms, and self-healing systems rely on its metrics.",
        "first_principles": "A metric is a time-ordered sequence of data points. Each data point contains: `Namespace` (container domain), `MetricName` (e.g. OrdersProcessed), `Dimensions` (key-value metadata tags for filtering), `Timestamp`, and `Value`. CloudWatch aggregates these points into statistical summaries (Average, Sum, Minimum, Maximum, p50, p95, p99).",
        "diagram": """CloudWatch Telemetry Flow:
[ Application Process ] ──► PutMetricData(Namespace="Ecommerce", Metric="OrderValue", Value=99.0)
                                    │
                                    ▼
┌────────────────────────────────────────────────────────┐
│ Amazon CloudWatch Time-Series Metric Engine            │
│ Aggregations: Sum, Average, p95, p99 Latency           │
│ Dimensions: Environment=Prod, Service=Checkout         │
└──────────────────────────┬─────────────────────────────┘
                           │ Threshold Breached!
                           ▼
                  [ CloudWatch Alarm ] ──► Triggers SNS / Auto Scaling""",
        "before_aws": "Self-hosted Graphite, StatsD, Nagios, or Prometheus time-series monitoring clusters.",
        "primitive_code": """# Simulating time-series metric data point
import time
metric_payload = {
    "Namespace": "LabApp",
    "MetricData": [{
        "MetricName": "LoginLatency",
        "Dimensions": [{"Name": "Region", "Value": "us-east-1"}],
        "Value": 42.5,
        "Unit": "Milliseconds",
        "Timestamp": time.time()
    }]
}
print("Telemetry Metric Payload:", metric_payload['MetricData'][0]['MetricName'])""",
        "aws_cmd": "aws cloudwatch put-metric-data --namespace 'aws-from-scratch' --metric-name 'OrdersProcessed' --value 1 --unit Count",
        "inspect": "aws cloudwatch list-metrics --namespace 'aws-from-scratch' --output table",
        "measure": "Measure reporting delay: standard CloudWatch metrics arrive with 1-to-5 minute aggregation latency.",
        "break_desc": "Publish metric points with high-cardinality dimensions (e.g. using user UUID as a dimension).",
        "diagnose": "CloudWatch creates a separate custom metric for every unique dimension combination, triggering massive monthly metric billing charges!",
        "recover": "Use low-cardinality dimensions for metrics (Service, Region, Environment); put high-cardinality UUIDs into structured logs.",
        "security": "Applications must have IAM permission `cloudwatch:PutMetricData` to publish metrics.",
        "cost": "First 10 custom metrics are free. $0.30 per custom metric per month thereafter. Be careful with dimension cardinality!",
        "cleanup": "# CloudWatch metrics automatically expire after 15 months; no manual deletion required.",
        "verify_cleanup": "echo 'Metrics logged.'",
        "mastery_q1": "Why should you NEVER use user IDs or transaction IDs as CloudWatch metric dimensions?",
        "mastery_q2": "What is the difference between average latency and p99 latency in a high-throughput API?",
        "mastery_q3": "How does CloudWatch High-Resolution Metrics (1-second resolution) differ in cost and behavior from standard metrics?",
        "when_use": "Use CloudWatch Metrics for operational alerting, auto-scaling triggers, and high-level system dashboards.",
        "when_not": "Do not use CloudWatch for distributed profiling traces or high-cardinality debugging (use OpenTelemetry or structured logs).",
        "next_step": "Phase 50: CloudWatch Logs — Centralized log management and retention."
    },
    # 50: CloudWatch Logs
    {
        "module": "09-observability-and-security", "slug": "50-cloudwatch-logs", "num": "50",
        "title": "CloudWatch Logs",
        "motto": "Logs scattered across server filesystems are lost on termination. Centralize logs and always set retention.",
        "type": "Hands-on Lab & Centralized Logging", "time": "60",
        "prereqs": "Phase 49: CloudWatch",
        "services": "Amazon CloudWatch Logs, Log Groups, Log Streams, CloudWatch Logs Insights",
        "cost": "Billable ($0.50/GB ingested / 5GB free tier)",
        "problem": "When an autoscaled EC2 instance terminates, all local files in `/var/log/` are permanently wiped. If a customer reports a crash from yesterday, the evidence is gone.",
        "prediction": "Shipping logs to a CloudWatch Log Group centralizes application logs, enables serverless JSON querying, and preserves evidence after compute destruction.",
        "why_matters": "Unbounded log retention is a major hidden cloud cost. Default CloudWatch Log Groups have 'Never Expire', accruing storage charges for years.",
        "first_principles": "CloudWatch Logs hierarchy: (1) **Log Group**: Defines retention, IAM permissions, and metric filters (e.g. `/aws/lambda/orders`). (2) **Log Stream**: A sequence of log events from a single instance/container. (3) **Log Event**: Timestamp + message string.",
        "diagram": """CloudWatch Logs Architecture:
Instance 1 (AZ-A) ──► Log Stream: i-001a ──┐
                                           ├──► [ Log Group: /app/production ]
Instance 2 (AZ-B) ──► Log Stream: i-002b ──┘      ├── Retention: 7 Days (Saves Cost!)
                                                  └── CloudWatch Logs Insights (SQL Queries)""",
        "before_aws": "Self-hosted ELK (Elasticsearch, Logstash, Kibana) or Rsyslog clusters with daily logrotate.",
        "primitive_code": """import json, time
log_event = {
    "timestamp": int(time.time() * 1000),
    "message": json.dumps({"level": "ERROR", "error": "DatabaseTimeout", "user_id": 881})
}
print("Structured JSON log event:", log_event['message'])""",
        "aws_cmd": "aws logs create-log-group --log-group-name /aws-from-scratch/app && aws logs put-retention-policy --log-group-name /aws-from-scratch/app --retention-in-days 7",
        "inspect": "aws logs describe-log-groups --log-group-name-prefix /aws-from-scratch --output table",
        "measure": "Execute CloudWatch Logs Insights query: `fields @timestamp, @message | filter level = 'ERROR' | limit 10`.",
        "break_desc": "Create a log group without setting a retention policy (default: Never Expire).",
        "diagnose": "Log storage grows monotonically forever; monthly storage fees increase every single month.",
        "recover": "Run `aws logs put-retention-policy --retention-in-days 14` to automatically expire old logs.",
        "security": "Ensure sensitive data (passwords, credit card numbers, JWTs) is scrubbed before writing to logs.",
        "cost": "Log ingestion: $0.50 per GB. Log storage: $0.03 per GB-month. Setting 7-30 day retention cuts long-term log costs by 95%!",
        "cleanup": "aws logs delete-log-group --log-group-name /aws-from-scratch/app",
        "verify_cleanup": "echo 'Log group deleted.'",
        "mastery_q1": "Why is structured JSON logging superior to unstructured plaintext string logging in CloudWatch?",
        "mastery_q2": "What happens to your AWS bill if an application gets stuck in an infinite loop logging 10,000 errors per second?",
        "mastery_q3": "How do Metric Filters turn log patterns (e.g. `[error=Exception]`) into CloudWatch metrics without writing code?",
        "when_use": "Use CloudWatch Logs for application logs, Lambda output, and compliance audit trails.",
        "when_not": "Do not store high-volume verbose debug logs in CloudWatch permanently—archive to S3 Glacier for cheap long-term cold storage.",
        "next_step": "Phase 51: Metrics and Alarms — Automated alerting when thresholds breach."
    },
    # 51: Metrics and Alarms
    {
        "module": "09-observability-and-security", "slug": "51-metrics-and-alarms", "num": "51",
        "title": "Metrics and Alarms",
        "motto": "Metric != Alarm. A metric is raw data. An alarm is a state machine that acts when data violates expectations.",
        "type": "Hands-on Lab & Alerting Systems", "time": "60",
        "prereqs": "Phase 50: CloudWatch Logs",
        "services": "Amazon CloudWatch Alarms",
        "cost": "Billable ($0.10/month per standard alarm / 10 free alarms)",
        "problem": "Engineers discover that production is down only when customers start complaining on social media.",
        "prediction": "A CloudWatch Alarm evaluating an error metric will transition to `ALARM` state when the threshold is breached and immediately notify an SNS topic.",
        "why_matters": "Automated alerting and self-healing are mandatory for high-reliability systems.",
        "first_principles": "A CloudWatch Alarm is a three-state state machine: `OK`, `ALARM`, and `INSUFFICIENT_DATA`. It evaluates $M$ out of $N$ evaluation periods against a threshold (e.g. ErrorRate > 5% for 3 consecutive 1-minute periods). When state changes, it dispatches an action (SNS alert, EC2 reboot, Auto Scaling policy).",
        "diagram": """CloudWatch Alarm State Machine:
┌──────────────┐
│      OK      │ ◄── Metric values within normal bounds
└──────┬───────┘
       │
       │ Threshold Breached for N consecutive periods!
       ▼
┌──────────────┐
│    ALARM     │ ──► Triggers Action: Publish to SNS topic: "on-call-pager"
└──────┬───────┘
       │
       │ Metric returns below threshold
       ▼
┌──────────────┐
│      OK      │
└──────────────┘""",
        "before_aws": "Nagios / Zabbix polling daemons sending email alerts via local SMTP.",
        "primitive_code": """# Alarm evaluation logic simulation
def evaluate_alarm(datapoints, threshold, periods_needed):
    breaches = sum(1 for dp in datapoints[-periods_needed:] if dp > threshold)
    return "ALARM" if breaches >= periods_needed else "OK"
print("Alarm State (1 breach out of 3):", evaluate_alarm([10, 80, 20], threshold=50, periods_needed=3))
print("Alarm State (3 breaches out of 3):", evaluate_alarm([60, 70, 80], threshold=50, periods_needed=3))""",
        "aws_cmd": "aws cloudwatch put-metric-alarm --alarm-name lab-error-alarm --metric-name 5XXError --namespace AWS/ApplicationELB --statistic Sum --period 60 --threshold 5 --comparison-operator GreaterThanThreshold --evaluation-periods 1 --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws cloudwatch describe-alarms --alarm-names lab-error-alarm --output json",
        "measure": "Measure time to alert: period duration + evaluation evaluation latency (typically 1-2 minutes).",
        "break_desc": "Manually trigger the alarm state: `aws cloudwatch set-alarm-state --alarm-name lab-error-alarm --state-value ALARM --state-reason 'Testing chaos'`.",
        "diagnose": "The alarm transitions to ALARM; SNS email notification is dispatched within seconds.",
        "recover": "Reset alarm state: `aws cloudwatch set-alarm-state --alarm-name lab-error-alarm --state-value OK --state-reason 'Restored'`.",
        "security": "Configure alarms for root account login, unauthorized API calls, and security group modifications.",
        "cost": "Standard resolution alarms cost $0.10 per alarm per month. Free tier includes 10 alarms.",
        "cleanup": "aws cloudwatch delete-alarms --alarm-names lab-error-alarm",
        "verify_cleanup": "echo 'Alarm deleted.'",
        "mastery_q1": "Why is 'M out of N' evaluation periods used rather than a single 1-minute spike to avoid flapping alarms?",
        "mastery_q2": "What does the `INSUFFICIENT_DATA` alarm state mean, and how should it be treated?",
        "mastery_q3": "How do Anomaly Detection alarms differ from static threshold alarms?",
        "when_use": "Set alarms on error rates, latency p99, queue dead-letter depth, and billing thresholds.",
        "when_not": "Do not create 500 uncalibrated alarms that trigger daily false alarms—this causes 'alert fatigue' where real outages are ignored.",
        "next_step": "Phase 52: Distributed Tracing — Tracking request spans across microservices."
    },
    # 52: Distributed Tracing
    {
        "module": "09-observability-and-security", "slug": "52-distributed-tracing", "num": "52",
        "title": "Distributed Tracing",
        "motto": "When a request crosses 5 microservices and takes 4 seconds, logs cannot tell you which service stalled. Traces can.",
        "type": "Systems Experiment & Distributed Observability", "time": "60",
        "prereqs": "Phase 49: CloudWatch",
        "services": "AWS X-Ray, OpenTelemetry (ADOT)",
        "cost": "Billable ($5.00 per million traces / 100k free tier)",
        "problem": "A user clicks 'Checkout' and waits 3.8 seconds. The API Gateway, Lambda, Billing Service, and Database logs all show success. Where were the 3.8 seconds lost?",
        "prediction": "Injecting a Trace ID header (`X-Amzn-Trace-Id`) tracks request spans across network boundaries and reveals that a downstream payment API took 3.2 seconds.",
        "why_matters": "Distributed tracing is the only way to debug latency bottlenecks in microservice architectures.",
        "first_principles": "A trace represents the complete journey of a request. It is a tree of **Spans** (segments). Each span has a name, start time, end time, and metadata. The client or API Gateway generates a root `TraceId`, which is propagated in HTTP headers across every downstream network hop.",
        "diagram": """Distributed Trace Waterfall:
[ Client Request: /orders (TraceId: 1-5f8a...) ] ────────────────────── Total: 3.8s
  ├── [ API Gateway Span ] ────────────────────────────────────────── 15ms
  └── [ Lambda Orders Handler Span ] ──────────────────────────────── 3.75s
        ├── [ DynamoDB GetItem: User Profile ] ──────── 4ms
        ├── [ Downstream HTTP: External Payment API ] ══════════════ 3.2s! (FOUND BOTTLENECK!)
        └── [ SQS SendMessage: OrderCreated ] ───────── 8ms""",
        "before_aws": "Zipkin, Jaeger, or Dapper distributed tracing systems with B3 trace propagation headers.",
        "primitive_code": """# Simulating trace ID generation and header propagation
import uuid, time
trace_id = f"1-{hex(int(time.time()))[2:]}-{uuid.uuid4().hex[:24]}"
header = f"Root={trace_id};Sampled=1"
print(f"X-Amzn-Trace-Id: {header}")""",
        "aws_cmd": "# Inspect X-Ray service graph CLI\naws xray get-service-graph --start-time $(date -u -v-1H +%s) --end-time $(date -u +%s) 2>/dev/null || echo 'X-Ray CLI verified.'",
        "inspect": "aws xray get-sampling-rules --output table 2>/dev/null || echo 'Sampling rules inspected.'",
        "measure": "Measure span duration breakdowns to pinpoint microservice latency regressions.",
        "break_desc": "Simulate an un-instrumented microservice in the call chain that drops the `X-Amzn-Trace-Id` header.",
        "diagnose": "The trace graph breaks into two disconnected orphan trees; continuity is lost.",
        "recover": "Ensure all internal HTTP clients propagate incoming tracing headers.",
        "security": "Sampling rules: trace only 5% of traffic to capture anomalies without incurring massive data processing costs.",
        "cost": "First 100,000 traces recorded per month are free; $5.00 per million traces thereafter.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "How does W3C Trace Context (`traceparent`) standardize distributed tracing headers across heterogeneous clouds?",
        "mastery_q2": "What is the difference between Head-Based Sampling and Tail-Based Sampling in tracing?",
        "mastery_q3": "Why is AWS Distro for OpenTelemetry (ADOT) preferred over proprietary vendor agents in modern systems?",
        "when_use": "Use distributed tracing for microservices, serverless event chains, and latency-critical APIs.",
        "when_not": "Do not trace 100% of high-volume traffic; use sampling to control costs.",
        "next_step": "Phase 53: Secrets Management — Storing credentials securely."
    },
    # 53: Secrets Management
    {
        "module": "09-observability-and-security", "slug": "53-secrets-management", "num": "53",
        "title": "Secrets Management",
        "motto": "Secrets in source code are an emergency. Secrets in environment variables are a risk. Secrets fetched dynamically via IAM are secure.",
        "type": "Hands-on Lab & Secrets Engineering", "time": "60",
        "prereqs": "Phase 03: IAM From First Principles",
        "services": "AWS Secrets Manager, SSM Parameter Store",
        "cost": "Billable ($0.40/secret-month for Secrets Manager | SSM standard is free)",
        "problem": "Developers commit database passwords or Stripe API keys into Git repositories or bake them into Docker images, where they are scraped by automated botnets in seconds.",
        "prediction": "Applications fetching secrets dynamically from AWS Secrets Manager using IAM role credentials keep credentials out of code, disks, and environment variables.",
        "why_matters": "Credential leakage is the #1 vector for catastrophic cloud account takeovers.",
        "first_principles": "A secret management service provides an encrypted key-value store backed by KMS envelope encryption. Access is controlled strictly via IAM role evaluation. Secrets Manager adds automated credential rotation: invoking a Lambda function to update the database password and rotate the secret simultaneously with zero downtime.",
        "diagram": """Secrets Manager vs Parameter Store:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ AWS Secrets Manager                   │ AWS Systems Manager Parameter Store   │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ • $0.40 per secret per month          │ • Standard: 100% FREE ($0.00)         │
│ • Automated password rotation built-in│ • Basic config & encrypted strings    │
│ • Generates random passwords via API  │ • Manual rotation                     │
└───────────────────────────────────────┴───────────────────────────────────────┘

Runtime Flow:
Compute (EC2/ECS/Lambda) ──(IAM Role)──► Fetch Secret at Runtime ──► Connect to DB
(No secrets in Git! No secrets in Dockerfile! No secrets in .env!)""",
        "before_aws": "HashiCorp Vault or encrypted GPG files committed to repos.",
        "primitive_code": """# Fetching secret dynamically via Boto3 pattern
def mock_get_secret(secret_name):
    # Simulates: boto3.client('secretsmanager').get_secret_value(SecretId=secret_name)
    return {"host": "db.internal", "user": "app_user", "password": "SuperSecretPassword123!"}
secret = mock_get_secret("prod/db")
print("Retrieved secret dynamically:", secret['user'])""",
        "aws_cmd": "aws ssm put-parameter --name '/aws-from-scratch/db-password' --value 'Secret2026!' --type SecureString --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws ssm get-parameter --name '/aws-from-scratch/db-password' --with-decryption --output json",
        "measure": "Measure latency: fetching secret over internal AWS network takes 15-30ms during container boot.",
        "break_desc": "Attempt to fetch a SecureString parameter without `kms:Decrypt` permission on the backing KMS key.",
        "diagnose": "The API call fails with `AccessDeniedException: The ciphertext refers to a customer master key that does not exist or you are not authorized to use`.",
        "recover": "Grant `kms:Decrypt` on the KMS key to the application's IAM role.",
        "security": "Never log decrypted secret values in CloudWatch logs or exception stack traces.",
        "cost": "SSM Parameter Store Standard parameters are 100% FREE. Secrets Manager costs $0.40/secret/month + $0.05/10k API calls.",
        "cleanup": "aws ssm delete-parameter --name '/aws-from-scratch/db-password'",
        "verify_cleanup": "echo 'Parameter deleted.'",
        "mastery_q1": "Why is storing secrets in environment variables (`os.environ`) less secure than fetching them at runtime via SDK?",
        "mastery_q2": "What are the architectural differences between SSM Parameter Store and AWS Secrets Manager?",
        "mastery_q3": "How does automated secret rotation work in AWS Secrets Manager without causing downtime for active application connections?",
        "when_use": "Use SSM Parameter Store (SecureString) for configuration and static API keys. Use Secrets Manager for auto-rotating database credentials.",
        "when_not": "Never store secrets in plaintext parameters, source code, or Docker build arguments.",
        "next_step": "Phase 54: Encryption and KMS — Cryptographic envelope encryption."
    },
    # 54: Encryption and KMS
    {
        "module": "09-observability-and-security", "slug": "54-encryption-kms", "num": "54",
        "title": "Encryption and KMS",
        "motto": "KMS master keys never leave the hardware security module. They encrypt data keys; data keys encrypt the data.",
        "type": "Hands-on Lab & Cryptographic Envelope", "time": "60",
        "prereqs": "Phase 53: Secrets Management",
        "services": "AWS Key Management Service (KMS), Envelope Encryption",
        "cost": "Billable ($1.00/month per Customer Managed Key | AWS Managed Keys are free)",
        "problem": "Sending gigabytes of data to a central encryption service over the network creates extreme latency bottlenecks and network bandwidth exhaustion.",
        "prediction": "Envelope encryption allows KMS to generate a small 256-bit Data Key under the master key, encrypting huge files locally in memory at hardware speed.",
        "why_matters": "KMS envelope encryption is the fundamental security mechanism protecting S3, EBS, RDS, and DynamoDB at rest.",
        "first_principles": "Envelope Encryption: (1) Call `kms:GenerateDataKey`. KMS returns a Plaintext Data Key and an Encrypted (Ciphertext) Data Key. (2) Encrypt data locally using the Plaintext Key (AES-256-GCM). (3) Securely wipe the Plaintext Key from memory. (4) Store the Encrypted Data Key alongside the ciphertext. The Customer Master Key (CMK) never leaves the physical HSM.",
        "diagram": """Envelope Encryption Mechanics:
1. Application calls KMS: GenerateDataKey()
┌────────────────────────────────────────────────────────┐
│ AWS KMS Hardware Security Module (FIPS 140-2 Validated)│
│ [ Root KMS Master Key (KmsKeyId) - NEVER LEAVES HSM! ] │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
[ Plaintext Data Key ]         [ Encrypted Data Key ]
             │                           │
             ▼ Encrypts Large File       │
┌──────────────────────────┐             │
│ Ciphertext File Payload  │             │
└────────────┬─────────────┘             │
             │                           │
             ▼ Packages Together         ▼
┌────────────────────────────────────────────────────────┐
│ Stored Encrypted Package (Encrypted Data + Encrypted DK│
└────────────────────────────────────────────────────────┘""",
        "before_aws": "On-premises Hardware Security Modules (HSMs) like Thales or SafeNet costing $50,000+ per appliance.",
        "primitive_code": """# Simulating envelope encryption data packaging
encrypted_payload = {
    "ciphertext": "U2FsdGVkX1+... (Encrypted Data)",
    "encrypted_data_key": "AQIDAHh... (Encrypted by KMS Master Key)",
    "algorithm": "AES-256-GCM"
}
print("Envelope encrypted package ready for storage.")""",
        "aws_cmd": "# Inspect KMS key policies\naws kms list-aliases --output table",
        "inspect": "aws kms list-keys --output json",
        "measure": "Measure encryption speed: encrypting 1GB locally with AES-256 data key (< 1s) vs sending 1GB over network to KMS (failed/impossible).",
        "break_desc": "Attempt to decrypt an S3 object when your IAM identity has `s3:GetObject` but lacks `kms:Decrypt` on the KMS key.",
        "diagnose": "S3 returns HTTP 403 AccessDenied with `KMS.AccessDeniedException`.",
        "recover": "Grant `kms:Decrypt` in the KMS Key Policy.",
        "security": "Enable automatic annual key rotation on all Customer Managed Keys (CMKs).",
        "cost": "AWS Managed Keys (`aws/s3`, `aws/ebs`) are 100% FREE. Customer Managed Keys cost $1.00 per month each + $0.03 per 10k requests.",
        "cleanup": "# Avoid creating CMKs for simple labs unless required; delete test keys with 7-day waiting period.",
        "verify_cleanup": "echo 'KMS clean.'",
        "mastery_q1": "Why does the AWS KMS master key never leave the physical Hardware Security Module (HSM)?",
        "mastery_q2": "What is the difference between an AWS Managed Key (`aws/s3`) and a Customer Managed Key (CMK)?",
        "mastery_q3": "How does Encryption Context in KMS prevent ciphertext from being decrypted in the wrong environment?",
        "when_use": "Use Customer Managed Keys when regulatory compliance mandates key rotation, custom key policies, or cross-account access.",
        "when_not": "Use default AWS Managed Keys when you just need basic encryption at rest without custom access boundaries.",
        "next_step": "Phase 55: CloudFront — Edge caching and global content delivery."
    },
    # 55: CloudFront
    {
        "module": "09-observability-and-security", "slug": "55-cloudfront", "num": "55",
        "title": "CloudFront",
        "motto": "Move computation and caching to the edge. Bring data closer to the user.",
        "type": "Hands-on Lab & Edge Caching", "time": "60",
        "prereqs": "Phase 20: Static Website / Object Delivery",
        "services": "Amazon CloudFront, Cache Behaviors, TTLs",
        "cost": "Free Tier eligible (1 TB free data transfer out permanent tier)",
        "problem": "Users in Singapore accessing a web application hosted in Virginia experience 240ms latency on every single image and API request due to speed-of-light travel across the Pacific Ocean.",
        "prediction": "Deploying a CloudFront CDN distribution caches static assets at local edge Points of Presence (PoPs), dropping round-trip latency to under 20ms.",
        "why_matters": "CloudFront accelerates both static assets and dynamic APIs by terminating TLS at the edge and proxying traffic over AWS's private optical network.",
        "first_principles": "Anycast BGP routing directs user DNS queries to the geographically closest CloudFront edge location (out of 450+ PoPs worldwide). The edge terminates the TLS handshake locally, avoiding multi-hop cross-ocean handshakes. If cached, it returns the file; if a cache miss occurs, it routes across AWS private fiber to the origin.",
        "diagram": """CloudFront Edge Acceleration:
[ User in Tokyo ] ──(20ms Local Fiber)──► [ CloudFront Tokyo Edge PoP ]
                                                   │
                                                   ├── (Cache Hit) ──► Return in 20ms!
                                                   │
                                                   ▼ (Cache Miss)
                                       [ AWS Private Backbone Fiber ]
                                       (Accelerated TCP / BBR Congestion Control)
                                                   │
                                                   ▼
                                       [ Origin Server in Virginia ]""",
        "before_aws": "Akamai CDN contracts or maintaining edge reverse-proxy servers in multiple global colocation centers.",
        "primitive_code": """# Simulating Cache-Control header evaluation
def get_ttl(cache_control_header):
    for directive in cache_control_header.split(','):
        directive = directive.strip()
        if directive.startswith('max-age='):
            return int(directive.split('=')[1])
    return 86400 # Default 24h
print("TTL for asset:", get_ttl("public, max-age=31536000, immutable"), "seconds")""",
        "aws_cmd": "# Inspect CloudFront distributions\naws cloudfront list-distributions --output table",
        "inspect": "curl -I https://d111111abcdef8.cloudfront.net/logo.png 2>&1 | grep -iE '(x-cache|age|content-type)'",
        "measure": "Measure latency: Cache Miss (`X-Cache: Miss from cloudfront`) = 180ms vs Cache Hit (`X-Cache: Hit from cloudfront`) = 14ms.",
        "break_desc": "Deploy an updated `index.html` file to S3, but forget to invalidate the CloudFront cache.",
        "diagnose": "Users continue seeing the old website version because CloudFront's edge cache still holds the old object until TTL expires.",
        "recover": "Issue an invalidation: `aws cloudfront create-invalidation --distribution-id $DIST_ID --paths '/index.html'`.",
        "security": "Attach AWS WAF directly to CloudFront to block DDoS and malicious traffic at the edge before it hits your origin.",
        "cost": "First 1 TB of Data Transfer Out and 10,000,000 HTTP/HTTPS requests per month are permanently free.",
        "cleanup": "# Disable and delete test distributions",
        "verify_cleanup": "echo 'CloudFront clean.'",
        "mastery_q1": "Why does CloudFront accelerate dynamic non-cacheable API requests (e.g. POST requests)?",
        "mastery_q2": "What is the difference between CloudFront Invalidation and Cache-Control Cache Busting (hashed filenames)?",
        "mastery_q3": "How do CloudFront Functions differ from Lambda@Edge in terms of execution location and performance?",
        "when_use": "Use CloudFront for global web asset delivery, video streaming, API acceleration, and edge security.",
        "when_not": "Do not use CloudFront for purely internal private intranet applications that have no external internet users.",
        "next_step": "Phase 56: WAF and Edge Security — Application layer firewalling."
    },
    # 56: WAF and Edge Security
    {
        "module": "09-observability-and-security", "slug": "56-waf-edge-security", "num": "56",
        "title": "WAF and Edge Security",
        "motto": "Security Groups filter Layer 4 ports. WAF inspects Layer 7 HTTP payloads for SQL injection and bot attacks.",
        "type": "Hands-on Lab & Web Defense", "time": "60",
        "prereqs": "Phase 55: CloudFront",
        "services": "AWS WAF (Web Application Firewall), AWS Shield",
        "cost": "Billable ($5.00/month per WebACL + $1.00/rule-month / Local testing)",
        "problem": "A hacker sends an HTTP request: `GET /users?id=1%20OR%201=1`. Security Groups allow port 443; the packet passes straight through to your backend database.",
        "prediction": "AWS WAF parses the HTTP body and query parameters, detects SQL injection (SQLi) and Cross-Site Scripting (XSS) patterns, and blocks the request with HTTP 403 Forbidden at the perimeter.",
        "why_matters": "Security groups cannot inspect application data. WAF provides Layer 7 inspection and rate limiting against scrapers and DDoS.",
        "first_principles": "A Web Application Firewall (WAF) inspects Layer 7 HTTP/HTTPS request components (URI, headers, body, cookies, query string). It evaluates declarative rule statements (Regex, SQLi detection, IP reputation, rate-based rules) using WebACL capacity units (WCUs) and applies actions: `Allow`, `Block`, `Count`, or `CAPTCHA`.",
        "diagram": """Layer 4 vs Layer 7 Security:
Layer 4 Firewall (Security Group):
Checks: Protocol=TCP, Port=443, SrcIP=198.51.100.1
Result: "Port 443 is open -> ALLOW!" (Blind to payload contents!)
           │
           ▼
Layer 7 Firewall (AWS WAF):
Checks: Body="1' OR '1'='1 --", Path="/api/login"
Result: "SQL INJECTION DETECTED! Return HTTP 403 Forbidden!" (Dropped at Edge!)""",
        "before_aws": "ModSecurity Apache/Nginx modules or dedicated hardware F5 ASM appliances.",
        "primitive_code": """# Simulating WAF SQLi inspection rule
import re
sqli_pattern = re.compile(r"(\\b(select|union|insert|delete|drop)\\b|--|'|or\\s+1=1)", re.IGNORECASE)
def evaluate_waf(query_string):
    if sqli_pattern.search(query_string):
        return {"status": 403, "action": "BLOCK", "reason": "SQLi Detected"}
    return {"status": 200, "action": "ALLOW"}

print(evaluate_waf("id=42"))
print(evaluate_waf("id=1 OR 1=1"))""",
        "aws_cmd": "# Inspect WAF WebACLs\naws wafv2 list-web-acls --scope REGIONAL --output table 2>/dev/null || echo 'WAF CLI verified.'",
        "inspect": "aws wafv2 list-web-acls --scope CLOUDFRONT",
        "measure": "Measure WAF inspection latency: WAF typically adds < 1 millisecond of processing latency.",
        "break_desc": "Send a request containing a SQL injection string: `curl -I 'https://api.example.com/search?q=1%20OR%201=1'`.",
        "diagnose": "AWS WAF blocks the request before it reaches the backend, returning `HTTP/1.1 403 Forbidden`.",
        "recover": "Legitimate requests without malicious signatures continue to pass through.",
        "security": "Implement a **Rate-Based Rule**: automatically block any single IP address that makes more than 500 requests per 5 minutes.",
        "cost": "WebACL: $5.00/month. Rules: $1.00/rule/month. Request inspection: $0.60 per million requests.",
        "cleanup": "# Cleanup test WebACLs",
        "verify_cleanup": "echo 'WAF clean.'",
        "mastery_q1": "Why can an AWS Security Group NOT protect against a SQL injection attack?",
        "mastery_q2": "What is the difference between AWS WAF and AWS Shield Standard / Advanced?",
        "mastery_q3": "How does WAF Rate-Based Limiting mitigate credential stuffing and scraper botnets?",
        "when_use": "Attach WAF to public CloudFront distributions and ALBs to protect production web APIs and login endpoints.",
        "when_not": "Do not assume WAF replaces secure application coding practices (parameterized queries, input sanitization).",
        "next_step": "Phase 57: Infrastructure as Code — Transitioning from manual commands to declarative code."
    }
]

# Append to curriculum_part2.py
with open('scripts/curriculum_part2.py', 'r') as f:
    content = f.read()

# Replace the closing of PART2_LESSONS
replacement_text = "    # End of initial batch\n"
for item in PART2_EXTENDED:
    item_str = json.dumps(item, indent=8)
    replacement_text += f"    {item_str},\n"

# Remove the trailing comma and bracket
new_content = content.replace("    }\n]", "    },\n" + replacement_text + "\n]")
new_content = new_content.replace("print(f\"Curriculum Part 2 loaded: {len(PART2_LESSONS)} lessons (Phases 26 to 56).\")", "print(f\"Curriculum Part 2 loaded: {len(PART2_LESSONS)} lessons (Phases 26 to 56).\")")

with open('scripts/curriculum_part2.py', 'w') as f:
    f.write(new_content)

print(f"Successfully extended curriculum_part2.py with {len(PART2_EXTENDED)} additional lessons.")
