## Run Dockerfile and Start Docker Image ##

```bash
docker build -t colmat:v1 .
docker run --gpus "device=1" -it colmat:v1
```

## Run script ##

`scripts.py` contains codes to run Background Matting V2 and COLMap.

### Now supports two kinds of inputs and outputs ###
1. - **Input**: folders of images with naming convention `img_n`
   - The first image of each folder will be used as input to COLMap
   - Perform background matting for all images
   - **Output**: a folder `matting_all` of all images and a `.json` file `transforms.json`
2. - **Input**: a folder containing image folders with objects from multiple views and a folder containing background images of each view 
   - **Output**: a folder `matting_all` of all images and a `.json` file `transforms.json`

```bash
python script.py --src <path_to_image_folder> [--bgr <path_to_bgr_folder>]
```
## Other resources ##

- The suggested model to use for background matting is `pytorch_resnet50`

    - other models can be downloaded at https://drive.google.com/drive/folders/1cbetlrKREitIgjnIikG1HdM4x72FtgBh
    - detailed usage of each model: https://github.com/PeterL1n/BackgroundMattingV2/blob/master/doc/model_usage.md 

