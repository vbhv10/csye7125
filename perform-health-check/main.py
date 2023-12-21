import os
import json
import sys
from kafka import KafkaProducer
import requests
from time import sleep
from datetime import datetime
import logging
import subprocess


# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

DEFAULT_KAFKA_BROKER = "localhost"
DEFAULT_KAFKA_TOPIC = "healthcheck"

# Get the logger
logger = logging.getLogger(__name__)

def get_broker_names(): 
    """
    Fetches the names of broker pods in a Kubernetes namespace and constructs a list of their addresses.

    Returns:
        list: A list of broker pod addresses, where each address is in the format
            "broker-name.namespace-controller-headless.namespace.svc.cluster.local".

    Raises:
        Exception: If an error occurs during the execution of the Kubernetes API request.
    
    Example:
        # Call the function to get the list of broker names and addresses
        broker_list = get_broker_names()
    """

    try:
        namespace = os.environ.get("KAFKA_NAMESPACE")

        cmd = """curl -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces/{}/pods 2>/dev/null | grep -o '"hostname": "[^"]*' | cut -d " " -f 2 | sed 's/"//g' | grep 'controller'""".format(namespace)
        broker_names = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip().split("\n")

        broker_list = ["{}.{}controller-headless.{}.svc.cluster.local".format(i,i.split("controller")[0],namespace) for i in broker_names]

        return broker_list

    except Exception as e:
        logger.error(str(e))
        return []


def publish_to_kafka(result):
    """
    Publish data to a Kafka topic.

    :param result: The data to be published to Kafka.
    :type result: dict

    This function publishes the provided data to a Kafka topic, using the KafkaProducer.
    """

    try:
        broker_list = get_broker_names()
        logger.info("Brokers list : {}".format(broker_list))
        kafka_topic = os.environ.get("KAFKA_TOPIC", DEFAULT_KAFKA_TOPIC)
        logger.info("Kafka Topic : {}".format(kafka_topic))
        producer = KafkaProducer(bootstrap_servers=broker_list if broker_list else ["localhost"],
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        producer.send(kafka_topic, value=result)
        producer.flush()
        logger.info("Message published to kafka".format(kafka_topic))
    except Exception as e:
        logger.error("Error while publishing to kafka : {}".format(str(e)))
        raise Exception(str(e))


def http_check(data: dict):
    """
    Perform an HTTP check with retries and return the response.

    :param data: Configuration data for the HTTP check.
    :type data: dict

    :return: The HTTP response object.
    :rtype: requests.Response

    This function performs an HTTP check using the provided configuration data. It includes retries based on the number of retries specified in the configuration.
    """

    try:
        url = data["uri"].split("//").pop()
        method = "https://" if data["use_ssl"] else "http://"
        retries = data["num_retries"]
        response = None
        exception_response = None
        return_data = {}

        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        count_retries = 0
        try:
            for i in range(retries):
                count_retries += 1
                logger.info("retring ({})...".format(i))
                response = requests.get(method + url, timeout=60)
                if response.status_code != data.get("response_status_code") and i < retries - 1:
                    logger.warning("Retrying ...")
                else:
                    break
        except Exception as e:
            logger.error("Error while hitting url : {}".format(str(e)))
            exception_response = {"Status": str(e)}

        return_data["start_time"] = start_time
        return_data["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            return_data["content"] = json.loads(response.content)
        except:
            return_data["content"] = exception_response if exception_response else {"Status": "HTTP Check successful"}
        return_data["status_code"] = response.status_code if response else 503
        return_data["content_length"] = response.headers.get("Content-Length") if response else 0
        return_data["url"] = method + url

        return return_data

    except Exception as e:
        logger.error("Error while running health check : {}".format(str(e)))
        raise Exception(str(e))

if __name__ == "__main__":
    try:
        logger.info("Starting check...")
        http_check_data = json.loads(os.environ.get("HTTP_CHECK_DATA"))
        logger.info("http_check_data : {}".format(http_check_data))
        return_data = http_check(http_check_data)
        logger.info("data to publish in kafka : {}".format(return_data))
        publish_to_kafka(return_data)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        logger.info("Exiting proxy...")
        cmd = """curl --max-time 2 -s -f -XPOST http://127.0.0.1:15000/quitquitquit"""
        subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
