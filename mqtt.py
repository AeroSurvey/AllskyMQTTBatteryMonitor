#! .venv/bin/python
"""MQTT client base class for acting on MQTT messages."""

import logging
from abc import ABC, abstractmethod
from typing import Any

import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)


class MQTTClient(ABC):
    """A simple MQTT client base class for monitoring a topic."""

    def __init__(
        self,
        broker: str,
        topic: str,
        port: int = 1883,
        keepalive: int = 60,
    ) -> None:
        """Initialize the MQTT client.

        Args:
            broker (str): The MQTT broker address.
            topic (str): The topic to subscribe to.
            port (int): The MQTT broker port. Defaults to 1883.
            keepalive (int): Keepalive interval in seconds. Defaults to 60.
                Lower values make last will trigger faster but increase
                network traffic.
        """
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self.topic = topic

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2  # type: ignore
        )
        self._connected: bool = False
        self._setup_callbacks()

        log.info(
            f"Initialized MQTT client for {broker}:{port}, topic '{topic}'"
        )

    def __enter__(self) -> "MQTTClient":
        """Enter the runtime context related to this object.

        Returns:
            MQTTClient: The MQTT client instance.
        """
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type (Any): The exception type, if an exception occurred.
            exc_value (Any): The exception value, if an exception occurred.
            traceback (Any): The traceback object, if an exception occurred.
        """
        self.disconnect()
        if exc_type is not None:
            log.error(f"An error occurred: {exc_value}")
        log.info("Disconnected from MQTT broker.")

    def _setup_callbacks(self) -> None:
        """Set up MQTT client callbacks."""

        def on_connect(
            client: mqtt.Client,
            userdata: Any,
            flags: Any,
            rc: int,
            properties: Any = None,
        ) -> None:
            if rc == 0:
                self._connected = True
                log.info(
                    f"Connected to MQTT broker at {self.broker}:{self.port}"
                )
                client.subscribe(self.topic)
                log.info(f"Subscribed to topic: {self.topic}")
            else:
                self._connected = False
                log.error(
                    f"Failed to connect to MQTT broker. Return code: {rc}"
                )

        def on_disconnect(
            client: mqtt.Client,
            userdata: Any,
            disconnect_flags: Any,
            reason_code: Any,
            properties: Any = None,
        ) -> None:
            self._connected = False
            if hasattr(reason_code, "value") and reason_code.value == 0:
                log.info(
                    f"Disconnected from MQTT broker. Reason code: {reason_code}"
                )
            else:
                log.warning(
                    "Unexpected disconnection from MQTT broker. "
                    f"Reason code: {reason_code}",
                )

        def on_message(
            client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage
        ) -> None:
            log.info(
                f"Received message on topic {message.topic}: "
                f"{message.payload.decode()}"
            )
            self.handle_message(message.topic, message.payload.decode())

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message

    def connect(self) -> None:
        """Connect to the MQTT broker."""
        if self._connected:
            log.warning("Already connected to MQTT broker.")
            return

        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()
        except Exception as e:
            log.error(f"Error connecting to MQTT broker: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()
        log.info(f"Disconnecting from MQTT broker at {self.broker}:{self.port}")
        self.client.disconnect()

    @property
    def is_connected(self) -> bool:
        """Check if the client is connected to the MQTT broker."""
        return self._connected

    @abstractmethod
    def handle_message(self, topic: str, payload: str) -> None:
        """Handle a message received on the monitored topic."""
        pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="",
    )

    class ExampleMQTTClient(MQTTClient):
        """Example implementation of the MQTTClient abstract class."""

        def handle_message(self, topic: str, payload: str) -> None:
            """Example message handler that just logs the message."""
            log.info(f"Handling message on topic {topic}: {payload}")

    with ExampleMQTTClient("172.17.204.35", "solar/dev-pi/data") as client:
        log.info("MQTT client is running. Press Ctrl+C to exit.")
        try:
            while True:
                pass  # Keep the client running
        except KeyboardInterrupt:
            log.info("Exiting MQTT client.")
