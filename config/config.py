# config.py
import yaml

# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

test_model = config["Test_Model"]
test_camera = config["Test_Camera"]
backEnd_ip = config["backEnd_ip"]
backEnd_Port = config["backEnd_Port"]
device_id = config["device_id"]
enable_websocket = config["enable_websocket"]
enable_RestAPI = config["enable_RestAPI"]
inference_ip = config["inference_ip"]
inference_port = config["inference_port"]
Roboflow_api_key = config["Roboflow_api_key"]
Roboflow_workspace = config["Roboflow_workspace"]
Roboflow_project = config["Roboflow_project"]
Roboflow_version = config["Roboflow_version"]
confidence_threshold = config["confidence_threshold"]
debug = config["debug"]
websocket_url = config["websocket_url"]