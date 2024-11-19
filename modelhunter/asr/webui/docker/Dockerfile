FROM centos:7

# 安装系统依赖和 Miniconda
RUN yum install -y wget bzip2 && \
    yum clean all && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    /opt/conda/bin/conda clean -tipsy

# 设置环境变量
ENV PATH=/opt/conda/bin:$PATH

# 复制环境文件并创建 Conda 环境
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean -a

# 配置启动时的环境激活
RUN echo "source activate your_env_name" > ~/.bashrc && \
    echo "conda activate your_env_name" >> ~/.bashrc

# 设置工作目录并启动容器
CMD ["bash"]
