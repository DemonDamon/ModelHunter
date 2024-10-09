# Date    : 2024/8/30 17:03
# File    : settings.py
# Desc    : 
# Author  : Damon
# E-mail  : bingzhenli@hotmail.com
import torch
import os

class LoggerSettings:
    """日志配置"""
    log_file_path = "/var/log/app.log"
    log_level = "INFO"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_to_console = True
    max_log_file_size = 10485760  # 10 MB
    backup_count = 5

class ServiceSettings:
    """服务配置"""
    port = 8080
    host = "0.0.0.0"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #model_path = "/path/to/model"
    inference_router = "/"
    inference_service_port = 8081
    max_workers = 4
    timeout = 120

class ModelSettings:
    """模型配置"""
    model_name = "SpeechRecognitionModel"
    model_version = "v1.0"
    input_format = "wav"
    output_format = "text"
    batch_size = 32
    max_sequence_length = 512

class BusinessSettings:
    """业务配置"""
    supported_languages = ["zh", "en"]
    min_confidence_threshold = 0.75
    retry_attempts = 3
    enable_batch_processing = True
    allowed_file_types = ["wav"]


class Paths:
    """路径相关配置"""
    # 根目录
    ROOT_DIR = os.path.abspath("modelhunter/asr/thirdparty")

    # 微调框架目录
    USER_DIR = os.path.join(ROOT_DIR, "TeleSpeech-ASR/data2vec_dialect")

    # 训练和评估脚本的路径
    training_finetune_script = os.path.join(USER_DIR, "run_scripts", "run_d2v_finetune.sh")  # 训练脚本路径
    evaluation_decode_script = os.path.join(USER_DIR, "run_scripts", "decode.sh")             # 评估脚本路径

    # 推理路径
    inference_dir = os.path.join(ROOT_DIR,"telespeech-asr-python")
    inference_model_path = os.path.join(inference_dir, "telespeechasr/model/torch_checkpoint.pt")
    inference_script = os.path.join(inference_dir, "telespeechasr/torch/infer.py")
    #inference_model_path = "/telespeech-asr-python/telespeechasr/model/torch_checkpoint.pt"
    #inference_audio_path = "/data/Gaozigeng/ASR/Data/dev/cantonese_audio_output/utt_9.wav"
    #inference_script = os.path.join(USER_DIR, "torch", "infer.py")  # 推理脚本路径

    # 预训练模型、配置文件路径
    PRETRAINED_MODEL_PATH = os.path.join(USER_DIR, "Model", "large.pt")
    FAIRSEQ_PATH = os.path.join(ROOT_DIR, "fairseq", "fairseq_cli", "hydra_train.py")
    CONFIG_DIR = os.path.join(USER_DIR, "config", "v2_dialect_asr")
    CONFIG_NAME = "base_audio_finetune_140h"

    # 数据路径
    DATA_PATH = os.path.abspath("modelhunter/asr/trainer")
    TRAIN_DATA_PATH = os.path.join(DATA_PATH, "training_data")
    INFERENCE_DATA_PATH = os.path.join(DATA_PATH, "inference_data")
    EVALUATION_DATA_PATH = os.path.join(DATA_PATH, "evaluation_data")