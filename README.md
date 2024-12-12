# Kafka Hackathon Starter Repo

Leveraging [Conduktor.io](https://www.conduktor.io/), a graphical desktop user interface for Apache Kafka and the [Conduktor starter GitHub repo](https://github.com/conduktor/kafka-stack-docker-compose).

## Stack versions

  - Conduktor Platform: latest
  - Zookeeper version: 3.6.3 (Confluent 7.3.2)
  - Kafka version: 3.3.0 (Confluent 7.3.2)
  - Kafka Schema Registry: Confluent 7.3.2
  - Kafka Rest Proxy: Confluent 7.3.2
  - Kafka Connect: Confluent 7.3.2
  - ksqlDB Server: Confluent 7.3.2
  - Zoonavigator: 1.1.1

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker-Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (Optional)
- [Java](https://www.java.com/en/download/) (Optional)

## Getting Started

1. Clone the repo
2. Create Python virtual environment
   1. `python3 -m venv venv`
   2. `source venv/bin/activate`
   3. `pip install -r requirements.txt`
   4. `deactivate` (when done)
3. Start the stack with the below docker compose commands
   1. `docker compose -f full-stack.yml up`
4. Access the Conduktor platform at [localhost:8080](http://localhost:8080/)
5. Login with the following credentials:
   - login: `admin@admin.io`
   - password: `admin`
6. Produce events with Python
7. Consume and transform events with Python/Kafka Consumers
8. Save and view the data

## Hackathon Instructions

### Pick a Project

- Easy:
  - Basic producers and consumers created
  - Project idea and goals available
- Medium:
  - Create your own producers and consumers. These could be scripts or Java/Python/other applications
  - Project idea and goals available
- Hard:
  - Start from scratch and build your own adventure

#### Easy: Music Streaming and Listening History

Produce and consume your "application users" listening history.

```bash
# Generate reusable mock users and songs
python3 ./projects/music-streaming/generate-streaming-files.py

# Run the producer script to start sending mock streaming data
python3 ./projects/music-streaming/kafka-producer.py

# Run the consumer script to start reading and processing the mock streaming data
python3 ./projects/music-streaming/kafka-consumer.py
```

#### Medium: Real-time Analytics Dashboard

Create a real-time analytics dashboard that displays important data for your company.

1. View the [Kafka Real-time Analytics Dashboard](./projects/real-time-dashboard/README.md) project README file
2. Create new processors/consumers/applications in `./projects/real-time-dashboard`

#### Hard: Build Your Own Adventure

Create your own project using Apache Kafka.

[Apache Kafka use cases](https://kafka.apache.org/uses)

## Full Conduktor Configurations Options

### Single Zookeeper / Single Kafka (Development)

This configuration fits most development requirements.

 - Zookeeper will be available at `$DOCKER_HOST_IP:2181`
 - Kafka will be available at `$DOCKER_HOST_IP:9092`
 - (experimental) JMX port at `$DOCKER_HOST_IP:9999`

Run with:
```bash
docker compose -f zk-single-kafka-single.yml up
docker compose -f zk-single-kafka-single.yml down
```

### Single Zookeeper / Multiple Kafka

If you want to have three brokers and experiment with kafka replication / fault-tolerance.

- Zookeeper will be available at `$DOCKER_HOST_IP:2181`
- Kafka will be available at `$DOCKER_HOST_IP:9092,$DOCKER_HOST_IP:9093,$DOCKER_HOST_IP:9094`

Run with:
```bash
docker compose -f zk-single-kafka-multiple.yml up
docker compose -f zk-single-kafka-multiple.yml down
```

## Multiple Zookeeper / Single Kafka

If you want to have three zookeeper nodes and experiment with zookeeper fault-tolerance.

- Zookeeper will be available at `$DOCKER_HOST_IP:2181,$DOCKER_HOST_IP:2182,$DOCKER_HOST_IP:2183`
- Kafka will be available at `$DOCKER_HOST_IP:9092`
- (experimental) JMX port at `$DOCKER_HOST_IP:9999`

Run with:
```bash
docker compose -f zk-multiple-kafka-single.yml up
docker compose -f zk-multiple-kafka-single.yml down
```


## Multiple Zookeeper / Multiple Kafka (Production like)

If you want to have three zookeeper nodes and three kafka brokers to experiment with production setup.

- Zookeeper will be available at `$DOCKER_HOST_IP:2181,$DOCKER_HOST_IP:2182,$DOCKER_HOST_IP:2183`
- Kafka will be available at `$DOCKER_HOST_IP:9092,$DOCKER_HOST_IP:9093,$DOCKER_HOST_IP:9094`

Run with:
```bash
docker compose -f zk-multiple-kafka-multiple.yml up
docker compose -f zk-multiple-kafka-multiple.yml down
```

# FAQ

## Kafka

**Q: Kafka's log is too verbose, how can I reduce it?**

A: Add the following line to your docker compose environment variables: `KAFKA_LOG4J_LOGGERS: "kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO"`. Full logging control can be accessed here: https://github.com/confluentinc/cp-docker-images/blob/master/debian/kafka/include/etc/confluent/docker/log4j.properties.template

**Q: How do I delete data to start fresh?**

A: Your data is persisted from within the docker compose folder, so if you want for example to reset the data in the full-stack docker compose, do a `docker compose -f full-stack.yml down`.

**Q: Can I change the zookeeper ports?**

A: yes. Say you want to change `zoo1` port to `12181` (only relevant lines are shown):
```
  zoo1:
    ports:
      - "12181:12181"
    environment:
        ZOO_PORT: 12181

  kafka1:
    environment:
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:12181"
```

**Q: Can I change the Kafka ports?**

A: yes. Say you want to change `kafka1` port to `12345` (only relevant lines are shown). Note only `LISTENER_DOCKER_EXTERNAL` changes:
```
  kafka1:
    image: confluentinc/cp-kafka:7.2.1
    hostname: kafka1
    ports:
      - "12345:12345"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka1:19092,EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:12345,DOCKER://host.docker.internal:29092
```

**Q: Kafka is using a lot of disk space for testing. Can I reduce it?**

A: yes. This is for testing only!!! Reduce the KAFKA_LOG_SEGMENT_BYTES to 16MB and the KAFKA_LOG_RETENTION_BYTES to 128MB

```
  kafka1:
    image: confluentinc/cp-kafka:7.2.1
    ...
    environment:
      ...
      # For testing small segments 16MB and retention of 128MB
      KAFKA_LOG_SEGMENT_BYTES: 16777216
      KAFKA_LOG_RETENTION_BYTES: 134217728
```

**Q: How do I expose kafka?**

A: If you want to expose kafka outside of your local machine, you must set `KAFKA_ADVERTISED_LISTENERS` to the IP of the machine so that kafka is externally accessible. To achieve this you can set `LISTENER_DOCKER_EXTERNAL` to the IP of the machine.
For example, if the IP of your machine is `50.10.2.3`, follow the sample mapping below:

```
  kafka1:
    image: confluentinc/cp-kafka:7.2.1
    ...
    environment:
      ...
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka2:19093,EXTERNAL://50.10.2.3:9093,DOCKER://host.docker.internal:29093
```

**Q: How do I add connectors to kafka connect?**

Create a `connectors` directory and place your connectors there (usually in a subdirectory) `connectors/example/my.jar`

The directory is automatically mounted by the `kafka-connect` Docker container

OR edit the bash command which pulls connectors at runtime

```
confluent-hub install --no-prompt debezium/debezium-connector-mysql:latest
        confluent-hub install
```

**Q: How to disable Confluent metrics?**

Add this environment variable
```
KAFKA_CONFLUENT_SUPPORT_METRICS_ENABLE=false
```
