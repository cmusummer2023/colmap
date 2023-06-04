# Running Background Matting V2 and COLMAP #

## Background Matting V2 ##

### Cloning repo and downloading model ###
1. 
    ```
    docker run --gpus "device=1" -it  -v /home/username:/home/username nvidia/cuda:11.8.0-devel-ubuntu22.04

    cd home/username/
    ```
2. 
    ```
    git clone https://github.com/PeterL1n/BackgroundMattingV2.git
    ```
3. suggested model to use is `pytorch_resnet50`
    - download it using this link: https://drive.google.com/file/d/1ErIAsB_miVhYL9GDlYUmfbqlV293mSYf/view?usp=drive_link and upload to the server through `scp`. Suggested command is:
        ```
        scp <LOCAL_PATH_TO_MODEL> <server name>:<PATH_TO_BGMATTING_REPO>
        ```
    - (trying to see if `gdown` works)
- other models can be downloaded at https://drive.google.com/drive/folders/1cbetlrKREitIgjnIikG1HdM4x72FtgBh
- detailed usage of each model: https://github.com/PeterL1n/BackgroundMattingV2/blob/master/doc/model_usage.md 
    

### Running Background Matting V2 ###
1. Install Conda environment and other dependencies

    - Download Miniconda3-latest-Linux-x86_64.sh:

        https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        ```
        bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda
        source /opt/miniconda/bin/activate
        ```
    - 
        ```
        pip install torch torchvision opencv-python tqdm
        apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
        ```
2. Inside `BackgroundMattingV2`, make two directories `videos` and `bgr` to store the videos and background images of the videos 
    - suggested video types: mp4, mov
    - suggested background image types: png

3. 
    ```
    python inference_video.py \
            --model-type mattingrefine \
            --model-backbone resnet50 \
            --model-backbone-scale 0.25 \
            --model-refine-mode sampling \
            --model-refine-sample-pixels 80000 \
            --model-checkpoint "<path-to-model>.pth" \
            --video-src "<path-to-video>.mp4" \
            --video-bgr "<path-to-bgr>.png" \
            --output-dir "output/" \
            --output-type com fgr pha err ref
    ```
    - The `output/com.mp4` will contain the video with background subtracted

## COLMAP ##
### Download and start the Colmap Docker image ###
```
docker pull colmap/colmap

docker run --gpus "device=1" -it -v /home/username:/home/username colmap/colmap
```
### Automatic 3D reconstruction ###

```
colmap automatic_reconstructor --workspace_path <PATH_TO_RESULTS> --image_path <PATH_TO_IMAGES> [--dense 0]
```
- It is suggested that the workspace path and the image path are different to avoid confusing colmap with unknown file types.

- Activate the `--dense` flag if don't want dense reconstruction (may take a long time)

### Convert binary reconstruction to raw text ###
```
colmap model_converter --input_path <PATH_TO_BIN_DIRECTORY> --output_path <PATH_TO_RESULTS> --output_type TXT
```
### Retrieve JSON file for camera poses ###
1. Clone the Instant-ngp repository:
    ```
    git clone https://github.com/NVlabs/instant-ngp.git
    ```
2. Make sure conda is installed:
    ```
    conda create -n colmap2nerf python=3.8
    conda activate colmap2nerf
    conda install numpy scipy opencv -c conda-forge
    ```
3. Run colmap2nerf:
```
python <PATH_TO_INSTANT_NGP>/scripts/colmap2nerf.py --text <PATH_TO_RAW_TEXTS_DIRECTORY>
```
- It will output a `transform.json` (default) with camera poses.
