import yt_dlp

def list_specific_formats(video_url, audio_only=False):
    """
    Lista formatos disponíveis: vídeo ou apenas áudio.
    """
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            print(f"\nFormatos disponíveis para: {info['title']}\n")
            print("{:<10} {:<10} {:<20}".format("Código", "Resolução/Taxa", "Extensão"))
            print("="*40)

            formats_dict = {}
            for stream in info['formats']:
                if audio_only:
                    if stream['vcodec'] == "none":  # Apenas streams de áudio
                        print("{:<10} {:<10} {:<20}".format(stream['format_id'], f"{stream.get('abr', 'N/A')}kbps", stream['ext']))
                        formats_dict[stream['format_id']] = f"{stream.get('abr', 'N/A')}kbps"
                else:
                    if stream['vcodec'] != "none":  # Apenas streams de vídeo
                        print("{:<10} {:<10} {:<20}".format(stream['format_id'], stream['resolution'], stream['ext']))
                        formats_dict[stream['format_id']] = stream['resolution']

            print("\nEscolha o código do formato desejado.")
            return formats_dict
    except Exception as e:
        print(f"Ocorreu um erro ao listar os formatos: {e}")
        return {}

def download_youtube_content(video_url, format_code, audio_only=False, ffmpeg_location=None):
    """
    Faz o download do conteúdo do YouTube no formato especificado.
    """
    try:
        ydl_opts = {
            'format': format_code,  # Código do formato desejado
            'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo de saída
        }

        if audio_only:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Baixar como MP3
                'preferredquality': '192',  # Qualidade do áudio
            }]
            if ffmpeg_location:
                ydl_opts['ffmpeg_location'] = ffmpeg_location

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando o {'áudio' if audio_only else 'vídeo'} no formato {format_code}...")
            ydl.download([video_url])
            print("Download concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro durante o download: {e}")

if __name__ == "__main__":
    # Solicitar URL do vídeo
    video_url = input("Digite o link do vídeo do YouTube: ").strip()

    # Escolher entre vídeo ou apenas áudio
    choice = input("Digite 'v' para baixar o vídeo ou 'a' para baixar apenas o áudio: ").strip().lower()

    ffmpeg_path = None  # Altere para o caminho do FFmpeg, se necessário, ex.: r"C:\ffmpeg\bin"

    if choice == 'v':
        # Listar formatos de vídeo
        formats_dict = list_specific_formats(video_url, audio_only=False)

        # Mostrar resoluções disponíveis no momento de inserir o código
        if formats_dict:
            print("\nOpções de vídeo disponíveis:")
            for code, resolution in formats_dict.items():
                print(f"Código: {code} | Resolução: {resolution}")

            # Escolher o formato desejado
            format_code = input("\nDigite o código do formato de vídeo que deseja baixar: ")

            # Fazer o download no formato escolhido
            if format_code in formats_dict:
                download_youtube_content(video_url, format_code, audio_only=False)
            else:
                print("Código de formato inválido. Tente novamente.")
    elif choice == 'a':
        # Listar formatos de áudio
        formats_dict = list_specific_formats(video_url, audio_only=True)

        # Mostrar opções de áudio disponíveis no momento de inserir o código
        if formats_dict:
            print("\nOpções de áudio disponíveis:")
            for code, bitrate in formats_dict.items():
                print(f"Código: {code} | Taxa: {bitrate}")

            # Escolher o formato desejado
            format_code = input("\nDigite o código do formato de áudio que deseja baixar: ")

            # Fazer o download no formato escolhido
            if format_code in formats_dict:
                download_youtube_content(video_url, format_code, audio_only=True, ffmpeg_location=ffmpeg_path)
            else:
                print("Código de formato inválido. Tente novamente.")
    else:
        print("Opção inválida. Execute novamente e escolha 'v' ou 'a'.")
