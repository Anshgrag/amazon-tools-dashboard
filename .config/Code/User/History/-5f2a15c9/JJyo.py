from tuya_connector import TuyaOpenAPI

ACCESS_ID = "m3negp3fvw7ugp7cqae8"
ACCESS_SECRET = "45b5bc2934f7437bb52739090eb96c5c"

ENDPOINT = "https://openapi.tuya.in"

api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
result = api.connect()

print("CONNECT RESULT:", result)
