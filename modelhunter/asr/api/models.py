import subprocess
import os
from api.settings import Paths
from components.logger import Logger
from utils import *
# 实例化日志记录器
logger = Logger.get_logger(__name__)

def training():
    """
    在 USER_DIR 目录下执行 training_finetune_script 指定的脚本。
    """
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["USER_DIR"] = Paths.USER_DIR
        env["PRETRAINED_MODEL_PATH"] = Paths.PRETRAINED_MODEL_PATH
        env["FAIRSEQ_PATH"] = Paths.FAIRSEQ_PATH
        env["CONFIG_DIR"] = Paths.CONFIG_DIR
        env["CONFIG_NAME"] = Paths.CONFIG_NAME
        env["TRAIN_DATA_PATH"] = Paths.TRAIN_DATA_PATH

        # 打印当前环境变量和训练脚本路径
        logger.info(f"User Directory: {Paths.USER_DIR}")
        logger.info(f"Running training script: {Paths.training_finetune_script}")

        # 使用 subprocess 在 USER_DIR 目录下执行训练脚本
        result = subprocess.run(
            ["bash", Paths.training_finetune_script],
            cwd=Paths.USER_DIR,
            env=env,
            check=True
        )
        
        logger.info(f"Training completed successfully with exit code {result.returncode}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Training failed with exit code {e.returncode}")
        raise
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise


def inference():
    """
    用于推理 (输入数据无需标签, 直接返回识别结果)。
    """
    try:
        logger.info("Starting inference...")
        logger.info(f"Model path: {Paths.inference_model_path}")
        logger.info(f"Inference script: {Paths.inference_script}")
        logger.info(f"Audio path: {Paths.INFERENCE_DATA_PATH}")

        result = subprocess.run(
            [
                "bash", "-c",
                f"PYTHONPATH=$PWD python {Paths.inference_script} --model_path {Paths.inference_model_path} --audio_path {Paths.INFERENCE_DATA_PATH}"
            ],
            cwd=Paths.inference_dir,
            check=True
        )

        logger.info("Inference completed successfully.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Inference failed with exit code {e.returncode}")
        raise
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise


def evaluation():
    """
    在 USER_DIR 目录下执行 evaluation_decode_script 指定的脚本。
    """
    try:
        env = os.environ.copy()
        env["USER_DIR"] = Paths.USER_DIR
        env["PRETRAINED_MODEL_PATH"] = Paths.PRETRAINED_MODEL_PATH
        env["FAIRSEQ_PATH"] = Paths.FAIRSEQ_PATH
        env["CONFIG_DIR"] = Paths.CONFIG_DIR
        env["CONFIG_NAME"] = Paths.CONFIG_NAME
        env["EVALUATION_DATA_PATH"] = Paths.EVALUATION_DATA_PATH

        logger.info(f"User Directory: {Paths.USER_DIR}")
        logger.info(f"Running evaluation script: {Paths.evaluation_decode_script}")

        result = subprocess.run(
            ["bash", Paths.evaluation_decode_script],
            cwd=Paths.USER_DIR,
            env=env,
            check=True
        )

        logger.info(f"Evaluation completed successfully with exit code {result.returncode}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Evaluation failed with exit code {e.returncode}")
        raise
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        raise



def process_data_workflow(mode="train", generate_audio=False, text_input_file="data_train.txt", input_dir=None, output_dir=None):
    """
    处理数据的工作流。可以选择是否生成音频，支持 train 和 dev 两种模式。

    参数:
    - mode: 选择 'train' 或 'dev' 模式，影响文件夹路径和命名。
    - generate_audio: 是否生成音频片段，默认为 False。
    - text_input_file: 输入的文本文件名，默认是 'data_train.txt'。
    - input_dir: 输入音频文件的目录。如果不指定，则使用默认路径。
    - output_dir: 输出音频文件的目录。如果不指定，则使用默认路径。
    """
    
    # 确定输入输出目录
    base_data_dir = f"/data/Gaozigeng/ASR/Data/{mode}/"
    audio_input_dir = input_dir or f"{base_data_dir}cantonese_audio_output_origin"
    audio_output_dir = output_dir or f"{base_data_dir}cantonese_audio_output"
    text_output_dir = os.path.join(base_data_dir, f"text_annotations_{mode}")
    wav_scp_path = os.path.join(base_data_dir, f"wav_{mode}.scp")
    datalist_output_file = os.path.join(base_data_dir, f"data_{mode}.list")
    tsv_train_path = os.path.join(base_data_dir, f"{mode}.tsv")

    # 1. 生成文本标注文件
    print(f"生成 {mode} 模式的标注文件...")
    generate_text_annotations(text_input_file, text_output_dir)

    # 2. 根据选择生成音频片段
    if generate_audio:
        print(f"生成 {mode} 模式的音频片段...")
        generate_audio_clips(os.path.join(text_output_dir, "data.list"), audio_output_dir)

    # 3. 检查并转换采样率
    print(f"检查并转换 {mode} 模式的音频采样率...")
    convert_wav_sample_rate(audio_input_dir, audio_output_dir)

    # 4. 生成 wav.scp 文件
    print(f"生成 {mode} 模式的 wav.scp 文件...")
    generate_wav_scp(audio_output_dir, wav_scp_path)

    # 5. 调用特征提取脚本
    print(f"提取 {mode} 模式的特征...")
    execute_kaldi_feats_script()

    # 6. 生成 data.list 文件
    print(f"生成 {mode} 模式的 data.list 文件...")
    update_text_and_generate_data_list(base_data_dir, audio_output_dir, f"{base_data_dir}/utt2len", wav_scp_path)

    # 7. 生成训练或验证数据的 tsv 文件
    print(f"生成 {mode} 模式的 tsv 文件...")
    link_files(datalist_output_file, tsv_train_path, datalist_output_file, tsv_train_path)

    print(f"{mode} 模式的数据处理工作流已完成。")