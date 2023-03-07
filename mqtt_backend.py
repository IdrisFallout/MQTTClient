import paho.mqtt.client as mqtt


class MqttClient:
    the_topic = None

    def __init__(self, broker_address, broker_port):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topics = []
        self.latest_message = [None, None]
        self.the_message = None
        self.display_message = []
        self.disconnection_callback = None
        self.is_connected = False
        self.topics_state = []

    def update_logins(self, broker_address, broker_port):
        self.broker_address = broker_address
        self.broker_port = broker_port

    def on_message(self, client, userdata, message):
        try:
            self.the_message = [message.topic, str(message.payload.decode("utf-8"))]
            self.get_latest_message()
        except:
            pass

    def get_latest_message(self):
        self.display_message[0](self.the_message[1], self.the_message[0])
        self.display_message[1]()

    def set_display_message(self, display_message):
        self.display_message = display_message

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.is_connected = True
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        for topic_dict in self.topics_state:
            if topic_dict["state"] == 1:
                self.client.subscribe(topic_dict["topic"])

    def disconnect(self):
        self.client.disconnect()
        self.is_connected = False
        self.handle_disconnection()

    def on_disconnect(self, client, userdata, rc):
        pass

    def set_disconnection_callback(self, disconnection_callback):
        self.disconnection_callback = disconnection_callback

    def handle_disconnection(self):
        if self.disconnection_callback is not None:
            self.disconnection_callback()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topics):
        self.topics = topics
        for topic in self.topics:
            self.client.subscribe(topic)

    def subscribe_to_topic(self, topic):
        self.client.subscribe(topic)

    def unsubscribe(self, topic):
        if topic in self.topics:
            self.client.unsubscribe(topic)

    def update_topics(self, topics):
        self.topics = list(set(topics))

    def update_topics_state(self, topics):
        self.topics_state = topics

    def loop_stop(self):
        self.client.loop_stop()
