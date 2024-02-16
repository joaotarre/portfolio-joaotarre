import http.client
import json
import time
from lojaonline import tkn,conn,headersList
import mysql.connector

#nesse arquivo eu armazeno as informações dos pedidos em um banco de dados sql para que
#possa ser feita uma analise dos pedidos no futuro e entender melhor como o negócio e os clientes vem se comportando

#colocando as credenciais de conexão com banco de dados SQL

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="teste123",
    database="ifood"
)

#fazer um GET pra pegar todos os eventos no momento retratado

payload = ""

conn.request("GET", "/order/v1.0/events:polling", payload, headersList)
response = conn.getresponse()
result = response.read()

orderList = []

#com o for in, vou adicionar os ids dos pedidos em uma lista para poder iterar ela pelo GET de detalhes.

x = json.loads(result.decode("utf-8"))
for i in range(len(x)):
    if x[i]['orderId'] not in orderList:
        orderList.append(x[i]['orderId'])

#tendo a lista de orderId vou poder iterar pelo GET de detalhes

#for i in range(len(orderList)):
for i in range(len(orderList)):
    payload = ""

    conn.request("GET", "/order/v1.0/orders/"+orderList[i], payload, headersList)
    response = conn.getresponse()
    result = response.read()
    x = dict(json.loads(result.decode('utf-8')))
    
    y = (x['id'],x['delivery']['deliveryAddress']['neighborhood'],x['createdAt'],x['customer']['name'],x['total']['subTotal'],x['total']['deliveryFee'],x['total']['benefits'],x['total']['additionalFees'])
    y = str(y)

    sql = "INSERT INTO 4fpedidos (orderId, bairro, dataPedido, cliente, subtotal, txentrega, beneficios, txAdicional) VALUES "+(y)
    sql = str(sql)
    try:
        cursor = conexao.cursor()
        # Execute o comando SQL
        cursor.execute(sql)

        # Faça commit para confirmar a inserção
        conexao.commit()

        # Feche o cursor e a conexão
        cursor.close()
    except:
        pass
conexao.close()