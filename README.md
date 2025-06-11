# Kafka vs Pub/Sub System Design Guide

This repository explains how to design a real-world event driven project using **Apache Kafka** and **Google Cloud Pub/Sub**. It covers core concepts, system components, and differences between the two technologies.

## Project Scenario: E-commerce Order Processing

Imagine an online store that needs to handle high volumes of orders, payments, and shipping updates. An event-driven architecture lets services communicate asynchronously through a messaging system.

### Core Services

1. **Order Service** – receives purchase requests and emits order events.
2. **Payment Service** – processes payments and emits success or failure events.
3. **Inventory Service** – updates product stock when orders complete.
4. **Shipping Service** – handles shipping labels and status notifications.
5. **Notification Service** – sends emails or SMS messages to customers.

Each service publishes events that other services subscribe to, creating a loosely coupled system.

## Using Kafka

- **Brokers and Topics**: Kafka clusters store events in topics. Each service publishes to relevant topics such as `orders`, `payments`, or `shipments`.
- **Partitions and Offsets**: Topics can be partitioned for scalability. Consumers track offsets to process events exactly once.
- **Consumer Groups**: Services can scale horizontally by running multiple instances in a group. Kafka distributes partitions among them for parallel processing.
- **Retention Policies**: Kafka retains data for a configurable period, letting new consumers rewind to reprocess events if needed.
- **Deployment**: Self-managed clusters require monitoring, storage management, and tuning for throughput and replication.

## Using Pub/Sub

- **Managed Service**: Google Cloud Pub/Sub provides a fully managed message broker. There is no need to operate your own cluster.
- **Topics and Subscriptions**: Publishers send messages to topics. Subscribers acknowledge each message so Pub/Sub can handle at-least-once delivery.
- **Push vs. Pull**: Subscriptions can push messages to HTTP endpoints or allow clients to pull them.
- **Scaling**: Pub/Sub automatically scales with demand and stores messages until they are acknowledged or expire.
- **Integration**: Works natively with other Google Cloud services for data processing and analytics pipelines.

## Key Differences

| Feature                     | Kafka                                    | Pub/Sub                                     |
|-----------------------------|-------------------------------------------|---------------------------------------------|
| **Management**              | Self-hosted or managed via Confluent      | Fully managed by Google                     |
| **Ordering Guarantees**     | Strong ordering within partitions         | Best effort ordering unless using ordering keys |
| **Retention Control**       | Configurable retention; consumers can replay | Messages deleted after acknowledged or TTL expiry |
| **Ecosystem**               | Rich open-source community and tooling    | Integrated with Google Cloud products       |
| **Use Cases**               | High-throughput event streaming, log aggregation | Cloud-native event ingestion and fan-out    |

## Choosing Between Them

- Use **Kafka** when you need fine-grained control over retention, strong ordering, and on-prem or hybrid deployments.
- Choose **Pub/Sub** for a serverless approach that scales automatically with minimal operational overhead in Google Cloud.

## Running Locally

This repository contains documentation only. There is no runnable code, but you can adapt these concepts to your own implementation.

