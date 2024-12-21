import subprocess
import os

def compress_video(pasta_origem, pasta_destino, bitrate="2M", preset="medium"):
    """
    Compress a video file using FFmpeg while keeping the original resolution.

    Parameters:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the compressed video.
        bitrate (str): Target video bitrate (e.g., '500k', '1M', '2M'). Default is '2M'.
        preset (str): Compression speed preset ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'). Default is 'medium'.
    """
    arquivos_ignorados = []

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivos_origem = [arq for arq in os.listdir(pasta_origem) if arq.endswith(".mp4") and not arq.endswith("_c.mp4")]
    arquivos_destin = [arq.replace("_c.mp4", ".mp4") for arq in os.listdir(pasta_destino)]

    arq_faltantes = set(arquivos_origem).difference(set(arquivos_destin))

    qtd_arquivos = len(arq_faltantes)
    print(f"- {qtd_arquivos} arquivos encontrados!")

    for i, arquivo in enumerate(arq_faltantes):
        print(f"\n  - iniciando processamento em {arquivo} - {i} de {qtd_arquivos}...")

        if not arquivo.endswith('.mp4'):
            print(f" - arquivo ignorado {arquivo}")
            # arquivos_ignorados.append(arquivo)
            continue

        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        if not os.path.isfile(caminho_arquivo):
            continue

        nome_arquivo = os.path.splitext(arquivo)[0] + "_c.mp4"
        caminho_destino = os.path.join(pasta_destino, nome_arquivo)

        try:
            command = [
                "ffmpeg",
                "-i", caminho_arquivo,
                "-vcodec", "libx264",
                "-b:v", bitrate,
                "-preset", preset,
                "-acodec", "aac",
                "-b:a", "97k",
                "-map_metadata", "0",
                "-loglevel", "error",
                caminho_destino
            ]
            subprocess.run(command, check=True)
            print(f"Video compressed successfully and saved to '{caminho_destino}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error compressing video: {e}")
            arquivos_ignorados.append(arquivo)

    print("\n\n", "="*50, "\nArquivos ignorados:")
    for arq in arquivos_ignorados:
        print(arq)

if __name__ == "__main__":
    input_video = "C:/Users/gomes/Videos/imagens_mi9t"
    output_video = "C:/Users/gomes/Videos/imagens_mi9t_compressed"
    bitrate = "5000k"

    compress_video(input_video, output_video, bitrate)
