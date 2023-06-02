# Running Background Matting V2 and COLMAP #

## Background Matting V2 ##

To be added

## COLMAP ##
### Download and start the Colmap Docker image ###
```
docker pull colmap/colmap

docker run --gpus "device=1" -it -v <USER_HOME>:<CONTAINER_HOME> colmap/colmap
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
2. (optional) Install Conda environment, Python and other dependencies

- Download Miniconda3-latest-Linux-x86_64.sh:

    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    ```
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda
    source /opt/miniconda/bin/activate
    conda create -n colmap2nerf python=3.8
    conda activate colmap2nerf
    conda install numpy scipy opencv -c conda-forge
    ```
3. Run colmap2nerf:
```
python <PATH_TO_INSTANT_NGP>/scripts/colmap2nerf.py --text <PATH_TO_RAW_TEXTS_DIRECTORY>
```
- It will output a `transform.json` (default) with camera poses.