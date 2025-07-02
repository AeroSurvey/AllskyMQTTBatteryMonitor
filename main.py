"""This is the main entry point for the allskymqttbatterymonitor application."""

import json
import logging

from mqtt import MQTTClient

log = logging.getLogger(__name__)


class AllSkyMQTTBatteryMonitor(MQTTClient):
    """AllSkyMQTTBatteryMonitor class that extends MQTTClient."""

    def __init__(
        self,
        broker: str,
        topic: str,
        filepath: str,
        port: int = 1883,
        keepalive: int = 60,
    ) -> None:
        """Initialize the AllSkyMQTTBatteryMonitor with broker details.

        Args:
            broker (str): The MQTT broker address.
            topic (str): The MQTT topic to monitor.
            filepath (str): The path to the file to update on MQTT message
                receipt.
            port (int): The MQTT broker port. Defaults to 1883.
            keepalive (int): Keepalive interval in seconds. Defaults to 60.
        """
        super().__init__(broker, topic, port, keepalive)
        self.filepath = filepath

    def handle_message(
        self,
        topic: str,
        payload: str,
    ) -> None:
        """Handle incoming messages on the monitored topic.

        Args:
            topic (str): The MQTT topic on which the message was received.
            payload (str): The message payload received.
        """
        logging.info(f"Message received on {topic}: {payload}")
        # TODO: Add logic to process the message as needed
        # access the file at self.filepath and update it with the payload
        data = json.loads(payload)
        battery_soc = int(data.get("battery_state_of_charge", "unknown"))
        battery_voltage = float(data.get("battery_voltage", "unknown"))
        logging.info(battery_soc)
        logging.info(f"{battery_voltage:.1f}")

    def __str__(self) -> str:
        """String representation of the AllSkyMQTTBatteryMonitor instance."""
        return (
            f"AllSkyMQTTBatteryMonitor(broker={self.broker}:{self.port}, "
            f"topic={self.topic}, filepath={self.filepath})"
        )


def main() -> None:
    """Main function to run the allskymqttbatterymonitor application."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AllSky MQTT Battery Monitor Application"
    )
    parser.add_argument(
        "--broker",
        type=str,
        required=True,
        help="MQTT broker address",
    )
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="MQTT topic to monitor",
    )
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the file to update on MQTT message receipt",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=1883,
        help="MQTT broker port (default: 1883)",
    )
    parser.add_argument(
        "--keepalive",
        type=int,
        default=60,
        help="MQTT keepalive interval in seconds (default: 60)",
    )

    args = parser.parse_args()

    with AllSkyMQTTBatteryMonitor(
        args.broker, args.topic, args.filepath, args.port, args.keepalive
    ) as client:
        log.info(f"{client}")
        try:
            while True:
                pass  # Keep the client running
        except KeyboardInterrupt:
            log.info("Exiting MQTT client.")


if __name__ == "__main__":
    log_fmt = (
        "%(asctime)s - %(levelname)s - %(module)s.py:%(lineno)d - %(message)s"
    )
    logging.basicConfig(
        level=logging.INFO,
        format=log_fmt,
    )
    main()
