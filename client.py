#!/usr/bin/env python3

from sys import argv
import socket
import json

sock = None
ipPort = None
host = None
port = None


def main():
    # modifica variáveis no escopo global
    global sock
    global ipPort
    global host
    global port

    # pega entrada
    ipPort = argv[1]
    host, port = ipPort.split(':')
    opt = int(argv[2])
    port = int(port)

    # abre socket e conecta ao servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # escolhe opção
    if opt == 0:
        result = analysis0()
    else:
        result = analysis1()

    # imprime resultados em formato TSV
    printTSV(result)
    # fecha socket
    sock.close()


# faz a análise 0 (IPXs por rede)
def analysis0():
    # dicionário onde a chave é um net_id e cada valor é outro dicionário com
    # nome e contador
    result = {}

    response = ix()
    for item in response:
        restartSocket()
        ix_ids = ixnets(item['id'])

        for item2 in ix_ids:
            if item2 not in result:
                restartSocket()

                result[item2] = {
                    'name': netname(item2),
                    'count': 1}
            else:
                result[item2]['count'] += 1

    return result


# faz a análise 1 (redes por IPX)
def analysis1():
    # dicionário onde a chave é um net_id e cada valor é outro dicionário com
    # nome e contador
    result = {}

    response = ix()
    for item in response:
        result[item['id']] = {
            'name': item['name'],
            'count': 0}

    for id in result.keys():
        restartSocket()
        result[id]['count'] = len(ixnets(id))

    return result


# problemas com requisições seguidas me obrigaram a reiniciar o socket depois
# de cada requisição
def restartSocket():
    global sock

    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))


# requisita endpoint do tipo 1: todos os IXPs
def ix():
    # cabeçalho
    request = 'GET /api/ix HTTP/1.1\r\nHost: http://' + ipPort + '\r\n\r\n'
    sock.send(bytes(request, 'utf-8'))

    # concatena toda resposta obtida
    response = ''
    while True:
        recv = sock.recv(1024)
        if not recv:
            break
        if len(recv) > 0:
            response += recv.decode('utf-8')

    # testa se resposta é válida
    if len(response) == 0:
        return None

    # remove header e retorna só o importante da resposta
    response = response.split('\r\n\r\n')
    response = json.loads(response[1])
    return response['data']


# requisita endpoint do tipo 2: identificadores das redes de um IXP
def ixnets(ix_id):
    # cabeçalho
    request = 'GET /api/ixnets/' + str(ix_id) + ' HTTP/1.1\r\nHost: ' + ipPort + '\r\n\r\n'
    sock.send(bytes(request, 'utf-8'))

    # concatena toda resposta obtida
    response = ''
    while True:
        recv = sock.recv(1024)
        if not recv:
            break
        if len(recv) > 0:
            response += recv.decode('utf-8')

    # testa se resposta é válida
    if len(response) == 0:
        return None

    # remove header e retorna só o importante da resposta
    response = response.split('\r\n\r\n')
    response = json.loads(response[1])
    return set(response['data'])


# requisita endpoint do tipo 3: nome de uma rede
def netname(net_id):
    # cabeçalho
    request = 'GET /api/netname/' + str(net_id) + ' HTTP/1.1\r\nHost: ' + ipPort + '\r\n\r\n'
    sock.send(bytes(request, 'utf-8'))

    # concatena toda resposta obtida
    response = ''
    while True:
        recv = sock.recv(1024)
        if not recv:
            break
        if len(recv) > 0:
            response += recv.decode('utf-8')

    # testa se resposta é válida
    if len(response) == 0:
        return None

    # remove header e retorna só o importante da resposta
    response = response.split('\r\n\r\n')
    response = response[1].replace('"', '')
    return response


# imprime saída das análises em formato TSV
def printTSV(result):
    for key, value in result.items():
        print(key, value['name'], value['count'], sep='\t')


if __name__ == '__main__':
    main()
