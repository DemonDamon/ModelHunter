import os
import re
import sentencepiece as spm
import subprocess
from paddlespeech.cli.tts import TTSExecutor

# 如果PaddlePaddle报错，请启用这一行，用于声明lib地址，设置 LD_LIBRARY_PATH，
#os.environ['LD_LIBRARY_PATH'] = '/data/anaconda3/envs/gaozigeng_asr/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

class LoggerUtils:
    pass


def read_json():
    pass


def read_yaml():
    pass

def convert_wav_sample_rate(input_dir, output_dir, target_sample_rate=16000):
    """
    将指定目录中的.wav文件转换为目标采样率并保存到输出目录
    """
    os.makedirs(output_dir, exist_ok=True)

    # 列出输入目录中的文件
    print("Files in input directory:")
    files = os.listdir(input_dir)
    wav_files = [f for f in files if f.endswith('.wav')]
    if not wav_files:
        print(f"No .wav files found in {input_dir}")
        return
    
    for file in wav_files:
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, file)

        # 检查当前文件的采样率
        try:
            result = subprocess.run(["sox", "--i", "-r", input_file], capture_output=True, text=True, check=True)
            sample_rate = int(result.stdout.strip())
            if sample_rate == target_sample_rate:
                print(f"{file} already has the correct sample rate of {target_sample_rate} Hz, skipping conversion.")
                continue
        except subprocess.CalledProcessError as e:
            print(f"Error checking sample rate for {input_file}: {e}")
            continue
        
        # 转换采样率
        try:
            subprocess.run(["sox", input_file, "-r", str(target_sample_rate), output_file], check=True)
            print(f"Converted {input_file} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {input_file}: {e}")
    
    print("All files have been checked and converted if needed.")
    
def generate_text_annotations(text_input_file, text_output_dir):
    """
    生成文本标注文件
    """
    os.makedirs(text_output_dir, exist_ok=True)
    utt2txt = {}
    with open(text_input_file, "r") as f:
        paragraphs = f.readlines()

    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if paragraph:
            utt_id = f"utt_{i + 1}"
            utt2txt[utt_id] = paragraph

    output_file = os.path.join(text_output_dir, "data.list")
    with open(output_file, "w") as fout:
        for utt_id, text in utt2txt.items():
            fout.write(f"{utt_id} {text}\n")
    print(f"标注文件已生成并保存至 {output_file}")


def generate_audio_clips(voice_input_file, voice_output_dir):
    """
    根据标注文件生成音频片段
    """
    os.makedirs(voice_output_dir, exist_ok=True)
    tts_executor = TTSExecutor()

    with open(voice_input_file, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                utt_id, text = parts
                output_audio_path = os.path.join(voice_output_dir, f"{utt_id}.wav")

                tts_executor(
                    text=text,
                    am='fastspeech2_canton',
                    voc='hifigan_csmsc',
                    lang='canton',
                    spk_id=10,
                    use_onnx=True,
                    output=output_audio_path,
                    cpu_threads=2
                )
                print(f"生成音频文件: {output_audio_path}")
    print("粤语发音音频已生成并保存。")


def generate_wav_scp(wav_dir, wav_scp_path):
    """
    生成 wav.scp 文件
    """
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.endswith('.wav')])

    with open(wav_scp_path, 'w') as f:
        for wav_file in wav_files:
            utt_id = os.path.splitext(wav_file)[0]
            wav_path = os.path.join(wav_dir, wav_file)
            f.write(f"{utt_id} {wav_path}\n")

    print(f"wav.scp 文件已生成，路径为: {wav_scp_path}")


def update_text_and_generate_data_list(data_dir, feat_dir, len_file, feat_scp, use_bpe=False, vocab_size=5000, feat_dim=40):
    """
    处理文本文件并生成 data.list
    """
    text_file = os.path.join(data_dir, "data.txt")
    output_file = os.path.join(data_dir, "data_with_ids.txt")
    datalist_file = os.path.join(data_dir, "data.list")

    utt2ark = {}
    utt2len = {}
    utt2txt = {}

    # Step 1: 更新文本文件
    with open(text_file, "r") as f:
        paragraphs = f.readlines()

    with open(output_file, "w") as fout:
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if paragraph:
                utt_id = f"utt_{i + 1}"
                fout.write(f"{utt_id} {paragraph}\n")

    print(f"文本文件已更新并保存至 {output_file}")

    # Step 2: 读取文本文件构建数据字典
    with open(output_file, "r") as f:
        for line in f:
            line = line.strip().split()
            utt, text = line[0], " ".join(line[1:])
            utt2txt[utt] = text

    with open(len_file, "r") as f:
        for line in f:
            utt, feat_len = line.strip().split()
            utt2len[utt] = int(feat_len)

    sp = spm.SentencePieceProcessor()
    if use_bpe:
        bpe_model = sp.load(bpemodel_dir)
        vocab_size = sp.get_piece_size()

    # Step 3: 生成数据列表
    with open(feat_scp, "r") as fin, open(datalist_file, "w") as fout:
        for line in fin:
            utt, ark = line.strip().split()
            txt, feat_len = utt2txt.get(utt, ""), utt2len.get(utt, 0)
            token_shape = len(txt.split())
            if use_bpe:
                token = " ".join(sp.EncodeAsPieces(txt))
            else:
                token = " ".join(re.sub(" ", "", txt))
            res_feat = f"utt:{utt}\tfeat:{ark}\tfeat_shape:{feat_len},{feat_dim}"
            res_text = f"text:{txt}\ttoken:{token}\ttokenid:[TOKENID]\ttoken_shape:{token_shape},{vocab_size}"
            fout.write(f"{res_feat}\t{res_text}\n")

    print(f"数据列表已生成并保存至 {datalist_file}")


def link_files(train_list, train_tsv, dev_list, dev_tsv):
    """
    生成训练和验证数据链接文件
    """
    os.symlink(train_list, train_tsv)
    os.symlink(dev_list, dev_tsv)
    print("生成 train.tsv 和 dev.tsv 完成")
    
def execute_kaldi_feats_script():
    """
    执行 Kaldi 的特征准备脚本 prepare_kaldi_feats.sh
    """
    # 获取相对路径
    kaldi_s5_dir = os.path.join(os.getcwd(), 'thirdparty/kaldi/egs/aishell/s5')
    
    # 切换到 Kaldi 的 s5 目录
    os.chdir(kaldi_s5_dir)
    
    # 执行 prepare_kaldi_feats.sh 脚本
    try:
        subprocess.run(['sudo', 'bash', 'prepare_kaldi_feats.sh'], check=True)
        print("Successfully executed the Kaldi feature preparation script.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing the script: {e}")
