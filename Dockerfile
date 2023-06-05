FROM colmap/colmap

ENV USERNAME myusername

WORKDIR /home/${USERNAME}

RUN git clone https://github.com/PeterL1n/BackgroundMattingV2.git
RUN git clone https://github.com/NVlabs/instant-ngp.git

RUN apt-get update && apt-get install wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda
RUN echo "source /opt/miniconda/bin/activate" >> /root/.bashrc

SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

RUN pip install pytorch torchvision opencv-python tqdm numpy scipy

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

ENTRYPOINT ["bash"]