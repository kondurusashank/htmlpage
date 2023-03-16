import requests
import xml.etree.ElementTree as ET

# Print environment variables
print("applicationnameid:", os.environ.get("applicationnameid"))
print("controllerurl:", os.environ.get("controllerurl"))
print("minutessincenotreported:", os.environ.get("Minutessincenotreported"))

# Get access token
token_url = "https://tedt.com/accesstoken"
client_id = "appidsf@customer1"
client_secret = "secrettest"
grant_type = "client_credentials"
data = {"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret}
response = requests.post(token_url, data=data)
access_token = response.json()["access_token"]

# Login
login_url = os.environ.get("controllerurl") + "/controller/auth?action=login"
headers = {"Authorization": "Bearer " + access_token}
session = requests.Session()
session.post(login_url, headers=headers)

# Get nodes
nodes_url = os.environ.get("controllerurl") + "/controller/rest/application/" + os.environ.get("applicationnameid") + "/nodes/"
response = session.get(nodes_url)
with open("nodes.xml", "wb") as f:
    f.write(response.content)

# Get historical node IDs
historical_node_ids = []
tree = ET.parse("nodes.xml")
root = tree.getroot()
for node in root.findall(".//node"):
    node_name = node.get("name")
    node_id = node.get("id")
    tier_name = node.get("tierName")
    node_health_url = os.environ.get("controllerurl") + "/controller/rest/application/" + os.environ.get("applicationnameid") + "/metric/"
    response = session.get(node_health_url)
    with open("nodehealth.xml", "wb") as f:
        f.write(response.content)
    node_health = ET.fromstring(response.content).find(".//metric-datas")
    if node_health is None or node_health.find(".//metricname").text == "metric data not found":
        historical_node_ids.append(node_id)

# Mark nodes as historical if there are any
if historical_node_ids:
    mark_historical_url = os.environ.get("controllerurl") + "/controller/rest/mark-nodes-historical"
    data = {"nodeIds": ",".join(historical_node_ids)}
    response = session.post(mark_historical_url, data=data)
