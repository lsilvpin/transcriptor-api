from dependency_injector import providers, containers
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.speech_to_text_tool import SpeechToTextTool


class Container(containers.DeclarativeContainer):
    """
    Container class for dependency injection.

    This class extends the `containers.DeclarativeContainer` class from the `dependency_injector` module.
    It provides instances for each services of the system.
    """

    log_tool = providers.Factory(LogTool)
    speech_to_text_tool = providers.Factory(SpeechToTextTool, logTool=log_tool)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "main.entrypoint.controllers.main_controller",
        ]
    )
