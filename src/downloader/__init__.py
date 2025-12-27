"""
Módulo downloader: Configurações e funcionalidades para download de áudio via yt-dlp.
"""

from .config import DownloaderConfig
from .engine import AudioDownloader
from .result import DownloadResult


__all__ = [
    "AudioDownloader",
    "DownloaderConfig",
    "DownloadResult",
]