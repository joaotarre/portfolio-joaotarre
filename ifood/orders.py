import http.client
import json
import time
from lojaonline import tkn, conn, headersList

#dentro da loja teste, para que os pedidos andem até o final é necessário que de aceite, comece o preparo e finalize todos, então é o que vou automatizar nesse algoritmo documento.

#fazendo um GET para pegar todos os eventos de um momento X


payload = ""

conn.request("GET", "/order/v1.0/events:polling", payload, headersList)
response = conn.getresponse()
result = response.read()

#vouu realizar um try pra que caso haja alguma inconsistencia nos pedidos eu tenha um retorno
#dentro do TRY vou fazer um POST pra iterar pela resposta do GET para que consiga movimentar os pedidos até a conclusão.
#dando tudo certo retorno que foi concluido e caso o contrario retorno que houve um erro

try:
    x = json.loads(result.decode("utf-8"))
    for i in range(len(x)):
        if x[i]['fullCode'] == 'CANCELLED':
            print('pedido: '+ x[i]['orderId'] +' cancelado')
        else:
            payload = ""

            conn.request("POST", "/order/v1.0/orders/"+str(x[i]['orderId'])+"/confirm", payload, headersList)
            response = conn.getresponse()
            result = response.read()

            time.sleep(1)

            payload = ""

            conn.request("POST", "/order/v1.0/orders/"+str(x[i]['orderId'])+"/startPreparation", payload, headersList)
            response = conn.getresponse()
            result = response.read()

            time.sleep(1)

            payload = ""

            conn.request("POST", "/order/v1.0/orders/"+str(x[i]['orderId'])+"/readyToPickup", payload, headersList)
            response = conn.getresponse()
            result = response.read()
            
    print('todos os pedidos atualizados')
except:
    print("erro no retorno dos pedidos")