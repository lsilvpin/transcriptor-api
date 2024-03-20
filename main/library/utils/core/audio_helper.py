import io
import wave


def get_audio_duration(audio: bytes) -> float:
    assert audio is not None
    assert isinstance(audio, bytes)
    assert len(audio) > 0
    with wave.open(io.BytesIO(audio), "rb") as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
