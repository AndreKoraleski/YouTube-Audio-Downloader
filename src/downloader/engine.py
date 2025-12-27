import logging
import yt_dlp

from .config import DownloaderConfig
from .filesystem import FileSystemManager
from .options import YtDlpOptionsBuilder
from .result import DownloadResult


logger = logging.getLogger(__name__)


class AudioDownloader:
    """
    Classe principal para gerenciar downloads de áudio via yt-dlp com base na configuração fornecida.

    Attributes:
        config (DownloaderConfig): Configurações para o downloader.
        fs_manager (FileSystemManager): Gerenciador do sistema de arquivos.
        options_builder (YtDlpOptionsBuilder): Construtor de opções para yt-dlp.
    """
    def __init__(self, config: DownloaderConfig = DownloaderConfig()):
        self.config = config
        self.fs_manager = FileSystemManager(self.config)
        self.options_builder = YtDlpOptionsBuilder(self.config)


    def download(self, url: str) -> DownloadResult:
        """
        Realiza o download de áudio a partir de uma URL.

        Args:
            url (str): URL do vídeo/áudio a ser baixado.

        Returns:
            DownloadResult: Objeto contendo o status e metadados do download.
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise ValueError("Não foi possível extrair informações da URL.")

            video_id = info.get("id", "unknown")
            title = info.get("title", "unknown")
            
            extension = self.config.preferred_codec or "webm"
            destination_path = self.fs_manager.resolve_destination_path(
                title=title,
                video_id=video_id,
                extension=extension
            )

            ydl_opts = self.options_builder.build_options(destination_path)

            logger.info(f"Iniciando download: {title} ({video_id})")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([url])
                if error_code != 0:
                    return DownloadResult.from_error(
                        video_id, title, f"Erro no processo do yt-dlp (código {error_code})"
                    )

            file_size = self.fs_manager.get_file_size(destination_path)
            
            result = DownloadResult(
                success=True,
                video_id=video_id,
                title=title,
                file_path=destination_path,
                duration_seconds=info.get("duration"),
                file_size_bytes=file_size,
                uploader=info.get("uploader"),
                upload_date=info.get("upload_date")
            )

            if self.config.create_result_file:
                result.save_json()

            return result

        except Exception as e:
            logger.exception(f"Erro ao processar download para {url}")
            return DownloadResult.from_error("unknown", "unknown", str(e))