from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class DownloaderConfig:
    """
    Configurações para download de áudio via yt-dlp (sem pós-processamento).

    Attributes:
        output_directory (Path): Diretório onde os arquivos baixados serão salvos.
        filename (Literal["title", "id"]): Esquema de nomenclatura do arquivo.
        overwrite_existing (bool): Se deve sobrescrever arquivos existentes.
        create_subdirectories (bool): Se deve criar subdiretórios para organizar downloads.

        audio_quality (Literal["best", "balanced", "worst"]): Qualidade do áudio a ser baixado.
        preferred_codec (Literal["opus", "aac", "mp3"] | None): Codec de áudio preferido.
        maximum_bitrate_kbps (int | None): Taxa máxima de bits para o áudio.

        retries (int): Número de tentativas em caso de falha no download.
        timeout_seconds (int): Tempo limite para cada tentativa de download em segundos.
    """

    # --- Salvamento ---
    output_directory: Path = Path("downloads")
    filename: Literal["title", "id"] = "title"
    overwrite_existing: bool = False
    create_subdirectories: bool = True

    # --- Seleção de Stream ---
    audio_quality: Literal["best", "balanced", "worst"] = "best"
    preferred_codec: Literal["opus", "aac", "mp3"] | None = "opus"
    maximum_bitrate_kbps: int | None = None

    # --- Robustez ---
    retries: int = 3
    timeout_seconds: int = 30
