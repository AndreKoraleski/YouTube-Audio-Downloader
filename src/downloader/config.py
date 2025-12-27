from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class DownloaderConfig:
    """
    Configurações para download de áudio via yt-dlp (sem pós-processamento).

    Attributes:
        output_directory (str): Diretório onde os arquivos baixados serão salvos.
        filename (Literal["title", "id"]): Esquema de nomenclatura do arquivo.
        overwrite_existing (bool): Se deve sobrescrever arquivos existentes.
        create_subdirectories (bool): Se deve criar subdiretórios para organizar downloads.
        create_result_file (bool): Se deve criar um arquivo de resultados após o download.

        audio_quality (Literal["best", "balanced", "worst"]): Qualidade do áudio a ser baixado.
        preferred_codec (Literal["opus", "aac", "mp3"] | None): Codec de áudio preferido.

        retries (int): Número de tentativas em caso de falha no download.
        timeout_seconds (int): Tempo limite para cada tentativa de download em segundos.
    """

    # --- Salvamento ---
    output_directory: str = "downloads"
    filename: Literal["title", "id"] = "title"
    overwrite_existing: bool = False
    create_subdirectories: bool = True
    create_result_file: bool = True

    # --- Seleção de Stream ---
    audio_quality: Literal["best", "balanced", "worst"] = "best"
    preferred_codec: Literal["opus", "aac", "mp3"] | None = "opus"

    # --- Robustez ---
    retries: int = 3
    timeout_seconds: int = 30
