# Kafka Music Streaming and Listening History

Create a music streaming workflow that generates and processes mock user music listening history

## Goals

- [ ] Generate mock songs and users `json` files
  - Review the `generate-streaming-files.py` script to see how the mock data is generated and the arguments that can be passed
- [ ] Start the `kafka-producer.py` script to send mock streaming data to a Kafka topic
- [ ] Start the `kafka-consumer.py` script in another terminal to read and process the mock streaming data from the Kafka topic

## Extra

- Modify the processor and consumer files to customize the fields and data passed to the Kafka topic
- [ ] Create a simple dashboard to display the mock streaming data
  - Example: Build a Java/Python application to read data from the topic and display it in a dashboard
  - Look into using a library like [Dash](https://dash.plotly.com/minimal-app) to create the dashboard
  - Look into using streams to update events
