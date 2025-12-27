from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator


class DownloadResult(BaseModel):
    """
    Representa o resultado de uma tentativa de download de áudio.

    Attributes:
        success (bool): Indica se o download foi bem-sucedido.
        video_id (str): ID do vídeo baixado.
        title (str): Título do vídeo baixado.
        file_path (Optional[Path]): Caminho do arquivo baixado, se bem-sucedido.
        error_message (Optional[str]): Mensagem de erro, se o download falhou.
        duration_seconds (Optional[int]): Duração do áudio em segundos, se disponível.
        file_size_bytes (Optional[int]): Tamanho do arquivo em bytes, se disponível.

    """
    success: bool
    video_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    file_path: Path | None = None
    error_message: str | None = None
    duration_seconds: int | None = Field(None, ge=0)
    file_size_bytes: int | None = Field(None, ge=0)
    uploader: str | None = None
    upload_date: str | None = None


    @model_validator(mode='after')
    def validate_success_state(self) -> 'DownloadResult':
        """
        Valida a coerência dos campos com base no estado de sucesso do download.

        Returns:
            DownloadResult: A instância validada.
        """    
        if self.success and not self.file_path:
            raise ValueError("file_path é obrigatório quando success=True")
        
        if not self.success and not self.error_message:
            raise ValueError("error_message é obrigatório quando success=False")
        
        return self


    @field_validator('file_path')
    @classmethod
    def validate_file_exists(cls, v: Path | None) -> Path | None:
        """
        Valida se o arquivo existe no sistema de arquivos.

        Args:
            v (Path | None): Caminho do arquivo.
        """
        if v is not None and not v.exists():
            raise ValueError(f"Arquivo não existe: {v}")
        
        return v


    def save_json(self, output_path: Path | None = None) -> Path | None:
        """Salva o resultado como um arquivo JSON.
        
        Args:
            output_path: Caminho personalizado para o arquivo JSON. Se None, usa
                        o caminho do arquivo de vídeo com extensão .json.
        
        Returns:
            Caminho para o arquivo JSON salvo, ou None se falhou.
            
        Raises:
            ValueError: Se o download não foi bem-sucedido ou file_path está ausente.
        """
        if not self.success or not self.file_path:
            raise ValueError("Não é possível salvar JSON para download sem sucesso")
        
        json_path = output_path or self.file_path.with_suffix(".json")
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        json_path.write_text(
            self.model_dump_json(indent=2, exclude_none=True),
            encoding='utf-8'
        )
        return json_path
    

    @classmethod
    def from_error(cls, video_id: str, title: str, error: str) -> 'DownloadResult':
        """ 
        Cria um resultado de download com erro.

        Args:
            video_id (str): ID do vídeo.
            title (str): Título do vídeo.
            error (str): Mensagem de erro.

        Returns:
            DownloadResult: Instância representando o erro de download.
        """
        return cls(
            success=False,
            video_id=video_id,
            title=title,
            error_message=error
        )
    

    @classmethod
    def from_success(cls, video_id: str, title: str, file_path: Path, duration_seconds: int | None = None, file_size_bytes: int | None = None, uploader: str | None = None, upload_date: str | None = None) -> 'DownloadResult':
        """
        Cria um resultado de download bem-sucedido.

        Args:
            video_id (str): ID do vídeo.
            title (str): Título do vídeo.
            file_path (Path): Caminho do arquivo baixado.
            duration_seconds (Optional[int]): Duração do áudio em segundos.
            file_size_bytes (Optional[int]): Tamanho do arquivo em bytes.
            uploader (Optional[str]): Nome do uploader do vídeo.
            upload_date (Optional[str]): Data de upload do vídeo.
    
        Returns:
            DownloadResult: Instância representando o download bem-sucedido.
        """
        return cls(
            success=True,
            video_id=video_id,
            title=title,
            file_path=file_path,
            duration_seconds=duration_seconds,
            file_size_bytes=file_size_bytes
        )