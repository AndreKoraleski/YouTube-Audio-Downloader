import logging

from pathlib import Path
from typing import Any

from .config import DownloaderConfig


logger = logging.getLogger(__name__)


class YtDlpOptionsBuilder:
    """
    Constrói o dicionário de opções para yt-dlp com base na configuração fornecida.
    """
    def __init__(self, config: DownloaderConfig):
        self.config = config

    
    def build_options(self, destination_path: Path) -> dict[str, Any]:
        """
        Constrói o dicionário de opções para passar ao yt-dlp com base na configuração.

        Args:
            destination_path (Path): Caminho completo do arquivo de destino.

        Returns:
            dict[str, Any]: Dicionário de opções para yt-dlp.
        """
        options = {
            'format': self._resolve_format_string(),
            'outtmpl': str(destination_path),
            'overwrites': self.config.overwrite_existing,
            'retries': self.config.retries,
            'socket_timeout': self.config.timeout_seconds,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }
        logger.debug(f"Opções yt-dlp construídas: {options}")
        return options


    def _resolve_format_string(self) -> str:
        """
        Resolve a string de formato para yt-dlp com base na configuração.

        Returns:
            str: String de formato para yt-dlp.
        """
        quality_map = {
            "best": "bestaudio/best",
            "balanced": "bestaudio[abr<=128]/bestaudio",
            "worst": "worstaudio/worst"
        }

        base_format = quality_map.get(self.config.audio_quality, "bestaudio/best")

        if self.config.preferred_codec:
            codec = self.config.preferred_codec
            return f"bestaudio[ext={codec}]/{base_format}"
        
        return base_format