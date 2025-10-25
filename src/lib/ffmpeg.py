from base64 import b64decode, b64encode

import ffmpeg


def speed_and_compress_b64(
    b64_in: str, speed=1.25, codec="libopus", bitrate="64k", fmt="opus"
) -> str:
    audio = b64decode(b64_in)

    proc = (
        ffmpeg.input("pipe:0")
        .output(
            "pipe:1",
            **{"filter:a": f"atempo={speed}"},
            acodec=codec,
            **({"b:a": bitrate} if codec != "libmp3lame" else {"q:a": 4}),
            f=fmt,
            vn=None,
        )
        .run(capture_stdout=True, capture_stderr=True, input=audio)
    )
    out_bytes, _ = proc
    return b64encode(out_bytes).decode()
