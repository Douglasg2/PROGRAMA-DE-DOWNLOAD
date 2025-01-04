import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import messagebox

def iniciar_download():
    # Caminho do FFmpeg
    ffmpeg_path = r'ffmpeg\bin\ffmpeg.exe'

    # Configuração inicial para listar as opções de formatos
    ydl_opts = {'ffmpeg_location': ffmpeg_path}

    # Variavel que recebe a url e o tipo
    url = url_entry.get()
    media = media_type.get()

    # Extrair informações do vídeo
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    # Verificar se é playlist
    if 'entries' in info_dict:
        # É uma playlist
        entries = info_dict['entries']
        total_videos = len(entries)
        messagebox.showinfo("Playlist detectada", f"Playlist detectada com {total_videos} vídeos.")
            

        # Baixar todos os vídeos da playlist
        for video in entries:
            processar_download(video, ydl_opts, media)
    else:
        # É um único vídeo
        processar_download(info_dict, ydl_opts, media)

def processar_download(info_dict, ydl_opts, media):

    formats = info_dict.get('formats', [])

    if media == 'audio':
        qualidade = audio_quality.get().lower()
        # filtro de qualidade do audio
        if qualidade == 'alta qualidade':
            qualidade = '320'
        elif qualidade == 'média qualidade':
            qualidade = '256'
        elif qualidade == 'baixa qualidade':
            qualidade = '128'

        # Filtrar os formatos de áudio
        audio_formats = [fmt for fmt in formats if fmt.get('vcodec') == 'none']
        if not audio_formats:
            print("Erro: Nenhum formato de áudio está disponível para este vídeo.")
            return
        # Selecionar o formato de áudio mais próximo da qualidade desejada
        chosen_format = next(
            (fmt for fmt in audio_formats if qualidade in fmt.get('format', '')), 
            audio_formats[-1]  # Escolhe o último formato disponível se a qualidade exata não for encontrada
        )
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',  # Extrai apenas o áudio
            'preferredcodec': 'mp3',  # Converte para MP3
            'preferredquality': qualidade,  # Qualidade do áudio
        }]

        print(f"URL: {info_dict}, Tipo: {media}, Qualidade: {qualidade}")
    else:
        qualidade = video_quality.get()

        # Filtrar formatos de vídeo
        video_formats = [fmt for fmt in formats if fmt.get('vcodec') != 'none']
        if not video_formats:
            print("Erro: Nenhum formato de vídeo está disponível para este vídeo.")
            return

        # Selecionar o formato de vídeo com base na qualidade desejada
        chosen_format = next(
            (fmt for fmt in video_formats if qualidade in fmt.get('format', '')), 
            video_formats[-1]  # Escolhe o último formato disponível se a qualidade exata não for encontrada
        )

        ydl_opts['format'] = chosen_format['format_id']
        ydl_opts['merge_output_format'] = 'mp4'  # Formato MP4 para vídeo
        print(f"Baixando vídeo: {info_dict['title']} em qualidade {qualidade}...")

    # Configurar a pasta de saída
    ydl_opts['outtmpl'] = f"./downloads/{info_dict['title']}.%(ext)s"

    # Fazer o download
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([info_dict['webpage_url']])

    print("Download concluído!")


# Janela principal
# Douglas Downloader Media Audio/Video
root = tk.Tk()
root.title("DDM Audio/video")
root.geometry("600x500") # Tamanho da janela

# Adição de campos de entrada da URL
tk.Label(root, text="Digite a URL do video: ").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Escolha de tipo de midia
media_type = tk.StringVar(value='undefined')
tk.Radiobutton(root, text="Áudio", variable=media_type, value='audio').pack(pady=5)
tk.Radiobutton(root, text="Vídeo", variable=media_type, value='video').pack(pady=5)

# Escolha de qualidade para audio
tk.Label(root, text="Qualidade de Áudio").pack(pady=10)
audio_quality = tk.StringVar(value='undefined')
audio_options = tk.OptionMenu(root, audio_quality, 'Baixa qualidade', 'Média qualidade', 'Alta qualidade')
audio_options.pack()

# Escolha a qualidade para o vídeo
tk.Label(root, text="Qualidade do Vídeo:").pack(pady=10)
video_quality = tk.StringVar(value='undefined')
video_menu = tk.OptionMenu(root, video_quality, '360p', '480p', '720p', '1080p')
video_menu.pack()

# Botão de download
tk.Button(root, text="Baixar", command=iniciar_download).pack(pady=20)

root.mainloop()