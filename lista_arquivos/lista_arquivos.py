import os
from time import time

def listar_arquivos(pasta_origem):
    arquivos_origem = os.listdir(pasta_origem)
    
    with open(f"lista_arquivos_{time()}.txt", "w") as arq:
        for arquivo in arquivos_origem:
            arq.write(arquivo + "\n")

if __name__ == "__main__":
    pasta_origem = "C:/Users/gomes/Videos/imagens_mi9t"

    listar_arquivos(pasta_origem)
