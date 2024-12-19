import os
from PIL import Image
import piexif

def corrigir_metadados(exif_data):
    """
    Corrige metadados inconsistentes removendo entradas incompatíveis.
    """
    exif_corrigido = {}
    for ifd in exif_data:
        if isinstance(exif_data[ifd], dict):
            exif_corrigido[ifd] = {}
            for tag, value in exif_data[ifd].items():
                try:
                    piexif.dump({ifd: {tag: value}})
                    exif_corrigido[ifd][tag] = value
                except Exception as e:
                    print(f"Tag inválida removida: IFD={ifd}, Tag={tag}, Value={value}, Tipo={type(value)}, Erro={e}")
        else:
            exif_corrigido[ifd] = exif_data[ifd]
    return exif_corrigido

def compactar_imagens(pasta_origem, pasta_destino, qualidade=85):
    """
    Compacta todas as imagens em uma pasta, redimensiona e mantém os metadados EXIF.
    """
    arquivos_ignorados = []

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivos_origem = os.listdir(pasta_origem)
    arquivos_destin = os.listdir(pasta_destino)
    arquivos_destin = [arq.replace("_c.jpg", ".jpg") for arq in arquivos_destin]

    arq_faltantes = set(arquivos_origem).difference(set(arquivos_destin))

    qtd_arquivos = len(arq_faltantes)
    print(f"- {qtd_arquivos} arquivos encontrados!")

    for i, arquivo in enumerate(arq_faltantes):
        print(f"\n  - iniciando processamento em {arquivo} - {i} de {qtd_arquivos}...")
        
        if arquivo.rsplit(".", 1)[1] != "jpg":
            print(f" - arquivo ignorado {arquivo}")
            # arquivos_ignorados.append(arquivo)
            continue
        
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        if not os.path.isfile(caminho_arquivo):
            continue

        try:
            imagem = Image.open(caminho_arquivo)

            exif_data = piexif.load(imagem.info.get("exif", b""))
            exif_corrigido = corrigir_metadados(exif_data)

            exif_bytes = piexif.dump(exif_corrigido)

            nome_arquivo = os.path.splitext(arquivo)[0] + "_c.jpg"
            caminho_destino = os.path.join(pasta_destino, nome_arquivo)
            imagem.save(caminho_destino, "JPEG", quality=qualidade, exif=exif_bytes)

            print(f"Imagem processada e salva: {caminho_destino}")
        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")
            arquivos_ignorados.append(arquivo)

    print("\n\n", "="*50, "\nArquivos ignorados:")
    for arq in arquivos_ignorados:
        print(arq)

if __name__ == "__main__":
    pasta_origem = input("- Pasta de Origem: ")
    pasta_destino = input("- Pasta de Destino: ")

    input("\nTem certeza que os caminhos estão corretos? [Ctrl + C para sair]")

    compactar_imagens(pasta_origem, pasta_destino, qualidade=70)
