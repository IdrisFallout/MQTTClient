# MQTTClient
[![wakatime](https://wakatime.com/badge/github/IdrisFallout/MQTTClient.svg)](https://wakatime.com/badge/github/IdrisFallout/MQTTClient)
## Introduction
This project is a MQTT client for the ESP8266 and other IOT devices. It is based on the [PubSubClient](https://pypi.org/project/paho-mqtt/) library.
The mqtt technology is used to connect devices to the internet. The devices can be sensors, actuators, or other devices that can be connected to the internet. The mqtt protocol is a publish/subscribe protocol. The devices can publish data to a topic and other devices can subscribe to that topic. The devices can also subscribe to topics and receive data from other devices.

## Why MQTT?
> Lightweight: MQTT is a lightweight protocol and is designed to work efficiently over low bandwidth, high latency networks. This makes it ideal for IoT and other resource-constrained applications.

> Low power consumption: MQTT's lightweight nature means that it can be used on devices with limited processing power and memory, making it ideal for battery-powered devices.

>Pub/Sub model: MQTT uses a publish/subscribe messaging model, which means that devices can subscribe to specific topics and receive only the messages they are interested in. This helps to reduce network traffic and conserve bandwidth.

>Quality of Service: MQTT provides different Quality of Service (QoS) levels for message delivery, allowing devices to choose the appropriate level of reliability for their application.

>Scalability: MQTT is designed to be scalable and can handle large numbers of devices and messages, making it suitable for enterprise-level applications.

>Security: MQTT supports TLS encryption and authentication, providing a secure messaging environment.

>Flexibility: MQTT is a protocol that can be used for a wide range of applications, from simple sensor networks to complex enterprise systems. It is also open-source and has a large community of developers, making it easy to find support and resources.

## Features
- Connect to a mqtt broker
- Publish data to a topic
- Subscribe to a topic
- Receive data from subscribed topics
## Installation
The mqtt client can be installed using pip:
```bash
pip install -r requirements.txt
```
## Usage
To run this project, run the following command:
```bash
python MQTTClient.py
```
> **Note** 
> Make sure you run `pip install -r requirements.txt` before running the project.

## Screenshots
### Dashboard
![DASHBOARD...](screenshots/dashboard.png?raw=true "Dashboard")
### Demo
![DEMO...](screenshots/demo.gif?raw=true "Demo")


## Limitations
- The project is still in development and is not yet complete.
- The project is only tested on the ESP8266.
- I have not implemented security features like TLS encryption and authentication so no need to use the username and password parameters.

## License
[MIT](https://choosealicense.com/licenses/mit/)
## Authors
- [@IdrisFallout](https://www.github.com/IdrisFallout)
