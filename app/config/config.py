import os
import shutil
import socket
import toml
import streamlit as st
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
config_file = f"{root_dir}/config.toml"

def load_config():
    # If running on Streamlit Cloud, try to load config from secrets
    if "PEXELS_API_KEY" in st.secrets:
        logger.info("Loading config from Streamlit secrets")
        # Build minimal config dict from secrets
        config_from_secrets = {
            "app": {
                "video_source": st.secrets.get("VIDEO_SOURCE", "pexels"),
                "pexels_api_keys": [st.secrets["PEXELS_API_KEY"]],
                "pixabay_api_keys": [],
                "ollama_base_url": st.secrets.get("OLLAMA_BASE_URL", ""),
                "ollama_model_name": st.secrets.get("OLLAMA_MODEL_NAME", ""),
                "imagemagick_path": "",
                "ffmpeg_path": "",
                # add other keys if needed
            },
            "whisper": {
                "model_size": st.secrets.get("WHISPER_MODEL_SIZE", "large-v3"),
                "device": st.secrets.get("WHISPER_DEVICE", "CPU"),
                "compute_type": st.secrets.get("WHISPER_COMPUTE_TYPE", "int8"),
            },
            "ui": {
                "hide_log": False,
            },
        }
        return config_from_secrets

    # Local environment: fix directory config file issue if needed
    if os.path.isdir(config_file):
        shutil.rmtree(config_file)

    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            shutil.copyfile(example_file, config_file)
            logger.info("Copied config.example.toml to config.toml")

    logger.info(f"Loading config from file: {config_file}")

    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"Load config failed: {str(e)}, trying utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_


_cfg = load_config()
app = _cfg.get("app", {})
whisper = _cfg.get("whisper", {})
proxy = _cfg.get("proxy", {})
azure = _cfg.get("azure", {})
siliconflow = _cfg.get("siliconflow", {})
ui = _cfg.get(
    "ui",
    {
        "hide_log": False,
    },
)

hostname = socket.gethostname()

log_level = _cfg.get("log_level", "DEBUG")
listen_host = _cfg.get("listen_host", "0.0.0.0")
listen_port = _cfg.get("listen_port", 8080)
project_name = _cfg.get("project_name", "MoneyPrinterTurbo")
project_description = _cfg.get(
    "project_description",
    "<a href='https://github.com/harry0703/MoneyPrinterTurbo'>https://github.com/harry0703/MoneyPrinterTurbo</a>",
)
project_version = _cfg.get("project_version", "1.2.6")
reload_debug = False

imagemagick_path = app.get("imagemagick_path", "")
if imagemagick_path and os.path.isfile(imagemagick_path):
    os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path

ffmpeg_path = app.get("ffmpeg_path", "")
if ffmpeg_path and os.path.isfile(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

logger.info(f"{project_name} v{project_version}")
