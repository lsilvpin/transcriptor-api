import sys, os, pytest

from main.library.utils.core.path_helper import get_root_dir

sys.path.insert(0, os.path.abspath("."))
import pytest
from main.library.utils.core.audio_helper import get_audio_duration


def test_should_return_duration():
    # Arrange
    root_dir = get_root_dir()
    audio_path = os.path.join(root_dir, "files", "test.wav")
    audio = open(audio_path, "rb").read()

    # Act
    duration = get_audio_duration(audio)

    # Assert
    assert 7 < duration < 8
