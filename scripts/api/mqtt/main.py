import json
import time
import threading
import logging
from paho.mqtt import client as mqtt

import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from api_read import apply_config_from_api, GLOBAL_CONFIG
from poll import set_interval_frequency, pull_data


# -------------------------------------
# Logging Setup
# -------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# -------------------------------------
# MQTT Settings
# -------------------------------------
BROKER = "127.0.0.1"
PORT = 1883

REQUEST_TOPIC = "imod32/pull"
RESPONSE_TOPIC = "imod32/pull/response"


mqtt_client = mqtt.Client()

running_thread = None
stop_flag = False


def mqtt_publish(data: dict):
    """Publish JSON back to MQTT broker."""
    mqtt_client.publish(RESPONSE_TOPIC, json.dumps(data))


def mqtt_on_message(client, userdata, msg):
    """Handle incoming MQTT request."""
    global running_thread, stop_flag

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        logging.info(f"MQTT REQUEST RECEIVED on {REQUEST_TOPIC}: {payload}")

        apply_config_from_api(payload)

        if "interval_ms" in payload:
            set_interval_frequency(payload["interval_ms"])
            logging.info(f"Polling interval set by MQTT: {payload['interval_ms']} ms")

        stop_flag = True
        if running_thread:
            running_thread.join()

        stop_flag = False
        running_thread = threading.Thread(
            target=poll_loop, args=(GLOBAL_CONFIG,)
        )
        running_thread.start()
        logging.info("Started new MQTT polling thread")

    except Exception as e:
        logging.error(f"MQTT Error: {e}")
        mqtt_publish({"error": str(e)})


def poll_loop(config):
    """Blocking loop that polls sensor and publishes result."""
    global stop_flag

    logging.info("MQTT polling loop started")

    while not stop_flag:
        try:
            result = pull_data(config)
            mqtt_publish({
                "record": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            logging.info(f"Published sensor record: {result}")

        except Exception as e:
            logging.error(f"Polling error: {e}")
            mqtt_publish({"error": str(e)})

        time.sleep(0.01)


def start_mqtt():
    mqtt_client.on_message = mqtt_on_message

    try:
        mqtt_client.connect(BROKER, PORT, 60)
        logging.info(f"Connected to MQTT broker at {BROKER}:{PORT}")
    except Exception as e:
        logging.error(f"Failed to connect MQTT Broker: {e}")
        return

    mqtt_client.subscribe(REQUEST_TOPIC)
    logging.info(f"Subscribed to topic: {REQUEST_TOPIC}")

    mqtt_client.loop_start()
    logging.info("MQTT Loop started")


if __name__ == "__main__":
    start_mqtt()
    while True:
        time.sleep(1)
