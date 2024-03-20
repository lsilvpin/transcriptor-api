import base64
import json
import platform
from dependency_injector.wiring import inject, Provide
from main.library.di_container import Container
from main.library.tools.core.log_tool import LogTool
from fastapi import APIRouter, Depends, HTTPException
from main.library.tools.core.speech_to_text_tool import SpeechToTextTool
from main.library.utils.core.settings_helper import get
from main.library.utils.models.validation_exception import ValidationException
from fastapi import File, UploadFile

router = APIRouter()


@router.get(
    "/info",
    tags=["Info"],
    responses={
        200: {"description": "Success", "content": {"application/json": {}}},
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {}},
        },
    },
)
@inject
async def get_info(logger: LogTool = Depends(Provide[Container.log_tool])):
    """
    Retorna informações básicas deste micro-serviço.

    Retorna um objeto JSON com o nome, a versão e outras informações úteis do micro-serviço.

    Retorna:
        - 200: Sucesso com as informações básicas do micro-serviço.
        - 500: Erro interno do servidor com a mensagem de erro.
    """
    try:
        name = "Meu Micro-serviço"
        version = "1.0.0"
        system = platform.system()
        machine = platform.machine()
        processor = platform.processor()
        python_version = platform.python_version()
        environment = get("environment")
        logger.info(
            "Informações sobre a API foram requisitadas e retornadas com sucesso."
        )
        return {
            "name": name,
            "version": version,
            "system": system,
            "machine": machine,
            "processor": processor,
            "python_version": python_version,
            "environment": environment,
        }
    except Exception as e:
        logger.error(f"Erro ao obter informações sobre a API: {str(e)}")
        return {"error": str(e)}, 500


@router.post(
    "/trancription",
    tags=["Audio"],
    responses={
        200: {"description": "Success", "content": {"application/json": {}}},
        400: {
            "description": "Bad Request",
            "content": {"application/json": {}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {}},
        },
    },
)
@inject
async def process_audio(
    audio: UploadFile = File(...),
    logger: LogTool = Depends(Provide[Container.log_tool]),
    speech_to_text_tool: SpeechToTextTool = Depends(
        Provide[Container.speech_to_text_tool]
    ),
):
    """
    Processa um arquivo de áudio.

    Recebe um arquivo de áudio e retorna uma mensagem de sucesso.

    Args:
        - audio: O arquivo de áudio a ser processado.
    """
    try:
        audio.seek(0)
        audio_as_wav = audio.file.read()
        speech_to_text_tool.issue_token()
        text = speech_to_text_tool.convert(audio_as_wav)
        logger.info("Arquivo de áudio recebido com sucesso.")
        return text
    except ValidationException as e:
        logger.error(f"Erro de integração com Azure Speech Services: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao processar o arquivo de áudio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
