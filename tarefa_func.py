import sys
import argparse
import requests
import os
ip_server = os.environ['IPADDR']
tarefa_end_point = ip_server+"Tarefa"


def adiciona(args):
    # filtrando e formatando
    tarefas = args[2:]
    tarefas = (" ".join(tarefas))
    tarefas = tarefas.split(", ")
    # cada tarefa sendo adicionada
    for tarefa in tarefas:
        payload = {'tarefa': tarefa, 'ativo': "1"}
        r = requests.post(tarefa_end_point, params=payload)
        if(r.status_code == 201):
            print("#"*50)
            print("Tarefa : {} \n foi adicionada com sucesso. status code: {}".format(
                tarefa, r.status_code))
        else:
            print("Problema ao tentar adicionar a tarefa {}. status code: {}".format(
                tarefa, r.status_code))


def lista():
    print("Estas são suas tarefas: \n")
    r = requests.get(tarefa_end_point)
    tarefas = r.json()
    for tarefa in tarefas:
        print(tarefa["tarefa"])


def busca(args):
    tarefa_id = args[2]
    r = requests.get(tarefa_end_point+"/{}".format(tarefa_id))
    print("Essa é a tarefa com id  {} : \n {}".format(tarefa_id, r.json()))


def apaga(args):
    print("Apagando: \n")
    tarefa_id = args[2]
    requests.delete(tarefa_end_point+"/{}".format(tarefa_id))
    print("Tarefa: {} \n".format(tarefa_id))


def atualiza(args):
    print("atualiza")
    tarefa_id = args[2]
    nova_tarefa = args[3]
    requests.put(tarefa_end_point +
                 "/{}?tarefa={}".format(tarefa_id, nova_tarefa))
    print("Tarefa: {} \n atualizada para : {}".format(tarefa_id, nova_tarefa))


def main():
    actions = {
        "adicionar": (lambda x: adiciona(x)),
        "listar": (lambda x: lista()),
        "buscar": (lambda x: busca(x)),
        "apagar": (lambda x: apaga(x)),
        "atualizar": (lambda x: atualiza(x))}

    if(len(sys.argv) >= 2):
        if(sys.argv[1] in actions):
            try:
                actions[sys.argv[1]](sys.argv)
            except Exception as e:
                print("Algum problema ao tentar execultar {} \n ERRO: {} ".format(
                    sys.argv[1], e))
        else:
            print("ERRO: Não foi possivel encontrar seu argumento {}\n Para verificar os comandos não coloque argumento".format(
                sys.argv[1]))

    else:
        print("""Parametros: \n\
            adicionar - Funciona para adicionar as tarefas. Pode separar diferentes tafefas utilizando a virgula \n\
                exemplo : adicionar levar cachorro para passiar, tirar o lixo\n\
            listar - Lista todas as tarefas ativas\n\
            buscar - Busca tarefa ativa pelo seu id  \n\
            apagar - Desativa tarefa (logicamente)  \n\
            atualizar - Atualiza o conteudo da terefa pelo id \n\
                exemplo: atualizar 1 nao levar o cachorro\n 

            """)


if __name__ == '__main__':
    main()
