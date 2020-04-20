import http.client

conn = http.client.HTTPSConnection("dtradd.auth0.com")

payload = "{\"client_id\":\"3ron7ysjNH4J0RadmjUFNlRCQvWaxC8L\",\"client_secret\":\"YxKivX7z7daMhgKoFsLQuF-Yp09UaLogPzSfcKefkR_bb-IJ4A3116ek6EJ2uLZv\",\"audience\":\"CoffeeShop\",\"grant_type\":\"client_credentials\"}"
headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)
res = conn.getresponse()

data = res.read()


print(data.decode("utf-8"))