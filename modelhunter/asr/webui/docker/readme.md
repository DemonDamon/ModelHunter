**注意由于其中一些环境在不同设备上可能报错不一样，需要重新编译安装。**

# 0 注意 
**为了确保环境正确搭建，请将克隆的项目均放在modelhunter/asr/thirdparty目录下，并进行对应替换**
具体环境搭建如下：
环境准备
  建议下列clone git都放置于同一目录下。
# 1 前置要求
    - PyTorch version >= 1.13.0
    - Python version >= 3.8
    - gcc >= 4.8.5
    - paddlepaddle <= 2.5.1
    - linux(推荐), mac, windows
# 2 安装kaldi
github下来项目：

    git clone https://github.com/kaldi-asr/kaldi.git kaldi --origin upstream


进入tools目录/INSTALL安装

    cd tools/
    cat INSTALL

依次执行并检查INSTALL里的要求：

    cd extras/
    ./check_dependencies.sh

这一步可能会出现很多问题，需要仔细核查，如果是mac和windows可能报错不同，mac建议直接用homebrew安装，不要使用pip」，只需要在最后一行大概率会出现：

    ...
    extras/check_dependencies.sh: neither libtoolize nor glibtoolize is installed
    extras/check_dependencies.sh: subversion is not installed
    extras/check_dependencies.sh: python2.7 is not installed
    extras/check_dependencies.sh: Intel MKL does not seem to be installed.
    ... Run extras/install_mkl.sh to install it. Some distros (e.g., Ubuntu 20.04) provide
    ... a version of MKL via the package manager, but verify that it is up-to-date.
    ... You can also use other matrix algebra libraries. For information, see:
    ...   http://kaldi-asr.org/doc/matrixwrap.html
    extras/check_dependencies.sh: Some prerequisites are missing; install them using the command:
      sudo apt-get install automake autoconf unzip sox gfortran libtool subversion pyth

根据最后一行执行：

    sudo apt-get install automake autoconf unzip sox gfortran libtool subversion pyth

再次执行./check_dependencies.sh，应当会出现all is ok。「所有步骤，出现all is ok 证明该步骤没有问题，已经正确安装」继续执行：
    
    cd .. 
    #tools 目录下
    make
    #结束后执行，-j 后面可以加数字，代表你的电脑cpu线程数量
    make -j 4
    *如果出现某一个包git不下来，被服务器墙了，直接把该项目压缩包下载到tool这个目录下，再次执行*

中间可能提示缺少安装irstlm可以安装，也可以不安装，稳妥起见建议安装。切换到src目录继续安装：
      
    cd ../src/
    cat INSTALL 
    #同样依次执行
    ./configure --shared
    make depend -j 8
    make -j 8

至此安装完成。
# 3 安装fairseq
  首先执行：
  
    $ git clone https://github.com/pytorch/fairseq
    $ cd fairseq
    $ pip install --editable ./
  
此处如果出现编译器出错如：

    subprocess.CalledProcessError: Command '['ccache', '-v']' returned non-zero exit status 1.

可以通过手动设置环境变量，例如

    export CC=gcc export CXX=g++

切换编辑器。


# 4 安装fairseq额外依赖以及wenet表征训练任务运行所需依赖
  首先克隆项目：
  
    git clone https://github.com/Tele-AI/TeleSpeech-ASR.git
  
  安装fairseq额外依赖以及wenet表征训练任务运行所需依赖pip install -r requirements.txt
# 5 配置PaddlePaddle Speech
  首先安装PaddlePaddle，参考https://www.paddlepaddle.org.cn，选择合适安装文件，
  例如适合gpu的服务器 ：
    
    python -m pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
  
  这里可能会报错：
      
    ImportError: cannot import name 'kaiser' from 'scipy.signal' (/data/anaconda3/envs/gaozigeng_asr/lib/python3.10/site-packages/scipy/signal/__init__.py)
  
  这是底层编码问题需要修改源码，paddlepaddle还未修复，执行：
    
    vi /data/anaconda3/envs/gaozigeng_asr/lib/python3.10/site-packages/paddlespeech/t2s/modules/pqmf.py

  修改 from scipy.signal import kaiser，改为
    
    from scipy.signal.windows import kaiser
  
  然后执行编译：
   
    git clone https://github.com/PaddlePaddle/PaddleSpeech.git
    cd PaddleSpeech
    pip install pytest-runner
    pip install .