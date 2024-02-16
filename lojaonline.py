import http.client
import json
import time

#importadas as bibliotecas que vou usar, faço um request para pegar o tkn de validação necessário para fazer o API funcionar.

conn = http.client.HTTPSConnection("merchant-api.ifood.com.br")

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/x-www-form-urlencoded" 
}

payload = "grantType=client_credentials&clientId=xxx"

conn.request("POST", "/authentication/v1.0/oauth/token", payload, headersList)
response = conn.getresponse()
result = response.read()

#para facilitar o uso do token, dou uma crio uma variável para atribuir ele e usar nas outras funções que vou fazer.

tkn = "Bearer " + json.loads(result.decode("utf-8"))['accessToken']

#vou fazer um request de status da loja teste para poder ver se a loja está online ou offline

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Authorization": tkn
}

payload = ""

conn.request("GET", "/merchant/v1.0/merchants/xxx/status", payload, headersList)
response = conn.getresponse()
result = response.read()
status = json.loads(result.decode("utf-8"))[0]['state']

#caso a loja retorne como offline, vou fazer um request de eventos da loja que faz com que a loja fique online.

if status == 'ERROR':
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Authorization": tkn 
    }

    payload = ""

    conn.request("GET", "/order/v1.0/events:polling", payload, headersList)
    response = conn.getresponse()
    result1 = response.read()
    time.sleep(2)

#agora com a loja online, faço mais um request de status e dou print com o status ao fim para ter certeza de que funcionou.

headersList = {
"Accept": "*/*",
"User-Agent": "Thunder Client (https://www.thunderclient.com)",
"Authorization": tkn
}

payload = ""

conn.request("GET", "/merchant/v1.0/merchants/xxx", payload, headersList)
response = conn.getresponse()
result = response.read()

print(json.loads(result.decode("utf-8"))[0]['state'])