import os
from tkinter import messagebox
from yt_dlp import YoutubeDL

# Função para baixar o vídeo ou áudio
def baixar():
    url = input("Digite a URL do vídeo: ")  # Pega a URL inserida

    if not url:
        print("Erro: Por favor, insira uma URL válida.")
        return
    
    try:
        # Caminho do FFmpeg
        ffmpeg_path = r'C:\Users\Douglas Oliveira\Documents\GitHub\PROGRAMA-DE-DOWNLOAD\ffmpeg\bin\ffmpeg.exe'

        # Configuração inicial para listar as opções de formatos
        ydl_opts = {'ffmpeg_location': ffmpeg_path}

        # Extrair informações do vídeo
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
        
        # Escolher entre áudio ou vídeo
        media_type = input("Escolha o tipo de mídia (audio/video): ").lower()

        if media_type == 'audio':
            # Opções de qualidade para áudio
            qualidade_audio = input("Escolha a qualidade do áudio (128, 192, 256, 320): ")
            
            # Filtrar os formatos de áudio
            audio_formats = [fmt for fmt in formats if fmt.get('vcodec') == 'none']
            if not audio_formats:
                print("Erro: Nenhum formato de áudio está disponível para este vídeo.")
                return

            # Selecionar o formato de áudio mais próximo da qualidade desejada
            chosen_format = next(
                (fmt for fmt in audio_formats if qualidade_audio in fmt.get('format', '')), 
                audio_formats[-1]  # Escolhe o último formato disponível se a qualidade exata não for encontrada
            )

            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',  # Extrai apenas o áudio
                'preferredcodec': 'mp3',  # Converte para MP3
                'preferredquality': qualidade_audio,  # Qualidade do áudio
            }]
            print(f"Baixando apenas o áudio em MP3 com a qualidade {qualidade_audio} kbps...")

        else:
            # Opções de qualidade para vídeo
            qualidade_video = input("Escolha a qualidade do vídeo (360p, 480p, 720p, 1080p): ")
            
            # Filtrar formatos de vídeo
            video_formats = [fmt for fmt in formats if fmt.get('vcodec') != 'none']
            if not video_formats:
                print("Erro: Nenhum formato de vídeo está disponível para este vídeo.")
                return

            # Selecionar o formato de vídeo com base na qualidade desejada
            chosen_format = next(
                (fmt for fmt in video_formats if qualidade_video in fmt.get('format', '')), 
                video_formats[-1]  # Escolhe o último formato disponível se a qualidade exata não for encontrada
            )

            ydl_opts['format'] = chosen_format['format_id']
            ydl_opts['merge_output_format'] = 'mp4'  # Formato MP4 para vídeo
            print(f"Baixando o vídeo em MP4 com a qualidade {qualidade_video}...")

        # Configurar a pasta de saída
        ydl_opts['outtmpl'] = './downloads/%(title)s.%(ext)s'

        # Fazer o download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Download concluído!")

    except Exception as e:
        print(f"Erro: Ocorreu um erro: {e}")


# Chama a função para iniciar o processo de download
baixar()
