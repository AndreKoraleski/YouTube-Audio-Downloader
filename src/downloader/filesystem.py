import logging
import re

from pathlib import Path

from .config import DownloaderConfig


logger = logging.getLogger(__name__)


class FileSystemManager:
    """
    Responsável por gerenciar a estrutura de diretórios e resolução de caminhos
    de arquivos para downloads.
    """
    def __init__(self, config: DownloaderConfig):
        self.config = config
        self.base_directory = Path(self.config.output_directory)
        self._ensure_base_directory()


    def _ensure_base_directory(self) -> None:
        """
        Garante que o diretório base para downloads exista.
        """
        try:
            self.base_directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Diretório base garantido: {self.base_directory}")

        except Exception as e:
            logger.critical(f"Falha ao criar diretório base {self.base_directory}: {e}")
            raise PermissionError(
                f"Não foi possível criar o diretório base: {self.base_directory}"
            ) from e


    def sanitize_filename(self, name: str) -> str:
        """
        Remove caracteres inválidos do nome do arquivo.

        Args:
            name (str): Nome original do arquivo.

        Returns:
            str: Nome sanitizado.
        """
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
        sanitized = re.sub(r"\s+", " ", sanitized).strip()
        logger.debug(f"Nome original: '{name}' -> Nome sanitizado: '{sanitized}'")
        return sanitized


    def resolve_destination_path(self, title: str, video_id: str, extension: str = "webm") -> Path:
        """
        Resolve o caminho completo do arquivo de destino com base na configuração.

        Args:
            title (str): Título do vídeo.
            video_id (str): ID do vídeo.
            extension (str): Extensão do arquivo (padrão: "webm").

        Returns:
            Path: Caminho completo do arquivo de destino.

        Raises:
            FileExistsError: Se o arquivo já existir e overwrite_existing for False.
        """
        if self.config.filename == "title":
            base_name = self.sanitize_filename(title)
        
        else:
            base_name = self.sanitize_filename(video_id)

        filename = f"{base_name}.{extension}"


        if self.config.create_subdirectories:
            target_directory = self.base_directory / base_name
        
        else:
            target_directory = self.base_directory

        try:
            target_directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Diretório alvo garantido: {target_directory}")
        
        except Exception as e:
            logger.error(f"Falha ao criar diretório {target_directory}: {e}")
            raise PermissionError(
                f"Não foi possível criar o diretório: {target_directory}"
            ) from e

        destination = target_directory / filename

        if destination.exists() and not self.config.overwrite_existing:
            logger.warning(f"Arquivo já existe e não será sobrescrito: {destination}")
            raise FileExistsError(
                f"O arquivo já existe e overwrite_existing=False: {destination}"
            )

        logger.debug(f"Caminho de destino resolvido: {destination}")
        return destination


    def prepare_for_download(self, title: str, video_id: str) -> Path:
        """
        Ponto de entrada para preparar o sistema de arquivos para um novo download.

        Args:
            title (str): Título do vídeo.
            video_id (str): ID do vídeo.

        Returns:
            Path: Caminho final pronto para receber o arquivo baixado.
        """
        destination = self.resolve_destination_path(
            title=title,
            video_id=video_id,
        )

        logger.info(f"Sistema de arquivos preparado para download: {destination}")
        return destination
