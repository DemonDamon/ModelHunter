api
- post
    - 推理 /inference
    - 训练  /training
    - 批量测试 /evaluation
- get
    - 服务可用 /status
  

# components
公共组件（和业务完全解耦）

# metrics
模型指标定义以及运算模板、批测统计效果

# thirdparty
直接调包的第三方插件、库等
kaldi、fbank、pp-speech

# trainer
pytorch、paddlepaddle、tensorflow
####################################################
# modelhunter_asr 项目概述
该项目可以将「」秒以下的音频识别为文字。适用于语音对话、语音控制、语音输入等场景。

· 接口类型：通过「」的方式提供通用的「」接口。适用于任意操作系统，任意编程语言

· 接口限制：需要上传完整的录音文件，或者通过gradio界面进行操作「」

「一键搭建环境」


「使用paddlepaddle时候如果出现报错缺少GLIBCXX_3.4.30，这是PP的BUG，请进入utils文件夹，启用路径生命，将export LD_LIBRARY_PATH=/path/to\lib:$LD_LIBRARY_PATH，改为自己的libstdc++.so.6的父级地址」 