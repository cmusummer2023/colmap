FROM colmap/colmap

WORKDIR /home/user

RUN git clone https://github.com/PeterL1n/BackgroundMattingV2.git
RUN git clone https://github.com/NVlabs/instant-ngp.git

RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
RUN apt-get update && apt-get install wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda
RUN rm Miniconda3-latest-Linux-x86_64.sh

SHELL ["/bin/bash", "-c"]

RUN source /opt/miniconda/etc/profile.d/conda.sh && conda activate base && \
    mkdir colmap && \
    /opt/miniconda/bin/pip install torch torchvision opencv-python tqdm numpy scipy

RUN /opt/miniconda/bin/pip install gdown

RUN /opt/miniconda/bin/gdown https://drive.google.com/uc?id=1ErIAsB_miVhYL9GDlYUmfbqlV293mSYf -O BackgroundMattingV2/
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

ENV PATH=/opt/miniconda/bin:$PATH

COPY script.py /home/user/script.py

ENTRYPOINT ["conda", "run", "--no-capture-output", "/bin/bash", "-c"]
CMD ["bash"]