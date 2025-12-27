import logging

from src.downloader import DownloaderConfig, AudioDownloader


url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Exemplo de URL


def example():
    """
    Exemplo de uso do módulo downloader para baixar áudio via yt-dlp.
    """
    # Configuração personalizada do downloader
    config = DownloaderConfig(
        output_directory="downloads",
        filename="id",
        overwrite_existing=False,
        create_subdirectories=True,
        create_result_file=True,
        audio_quality="best",
        preferred_codec="opus",
        retries=3,
        timeout_seconds=30
    )

    # Inicializa o downloader com a configuração personalizada
    downloader = AudioDownloader(config)

    # Realiza o download a partir da URL fornecida
    result = downloader.download(url)

    if result.success:
        print(f"Download bem-sucedido: {result.title}")
        print(f"Caminho do arquivo: {result.file_path}")
        print(f"Tamanho do arquivo: {result.file_size_bytes} bytes")

    else:
        print(f"Falha no download: {result.error_message}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)s [%(levelname)s] - %(message)s")
    example()