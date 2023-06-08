import os
import shutil
import argparse
import subprocess
import json

parser = argparse.ArgumentParser()

# input expect to be a folder with background images and a folder with folders from different views
parser.add_argument("--src", type=str,
                    help="path to input images", required=True)
parser.add_argument("--bgr", type=str, help="path to background images")

args = parser.parse_args()

# Define the paths
SRC_FLDR = args.src
COLMAP_INPUT = args.bgr if args.bgr is not None else "colmap_inputs/"
MATTING_SCRIPT = os.path.join(
    os.getcwd(), "BackgroundMattingV2/inference_images.py")
MATTING_MODEL = os.path.join(
    os.getcwd(), "BackgroundMattingV2/pytorch_resnet50.pth")

# Take the first image from each folder to be inputs to COLMAP
if args.bgr is None:
    if os.path.exists(COLMAP_INPUT):
        shutil.rmtree(COLMAP_INPUT)
    os.makedirs(COLMAP_INPUT, mode=0o777)

    # Iterate over the source folders
    for folder_name in os.listdir(SRC_FLDR):
        folder_path = os.path.join(SRC_FLDR, folder_name)
        if os.path.isdir(folder_path):
            image_files = os.listdir(folder_path)
            if image_files:
                first_image_path = os.path.join(folder_path, image_files[0])
                destination_path = os.path.join(
                    COLMAP_INPUT, f"{folder_name}.jpg")
                shutil.copy(first_image_path, destination_path)

if os.path.exists("colmap/results/"):
    shutil.rmtree("colmap/results/")
os.makedirs("colmap/results/", mode=0o777)

# Run colmap on colmap_inputs images
subprocess.run(
    [
        "colmap",
        "automatic_reconstructor",
        "--workspace_path",
        "colmap/results",
        "--image_path",
        COLMAP_INPUT,
        "--dense",
        "0",
    ]
)
# output will be at colmap/results/sparse/0

# convert to txt files
if os.path.exists("colmap/results/txts"):
    shutil.rmtree("colmap/results/txts")
os.makedirs("colmap/results/txts", mode=0o777)

subprocess.run(
    [
        "colmap",
        "model_converter",
        "--input_path",
        "colmap/results/sparse/0",
        "--output_path",
        "colmap/results/txts",
        "--output_type",
        "TXT",
    ]
)

# # get transform.json
subprocess.run(
    [
        "python",
        "instant-ngp/scripts/colmap2nerf.py",
        "--images",
        "colmap/images",
        "--text",
        "colmap/results/txts",
        "--out",
        "colmap/original.json",
    ]
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Run background matting
bgr_images = os.listdir(COLMAP_INPUT)

if os.path.exists("matting_all"):
    shutil.rmtree("matting_all")
os.makedirs("matting_all", mode=0o777)

for idx, folder_name in enumerate(os.listdir(SRC_FLDR)):
    folder_path = os.path.join(SRC_FLDR, folder_name)
    if os.path.isdir(folder_path):
        # create bgr directory
        if os.path.exists("bgr_img"):
            shutil.rmtree("bgr_img")
        os.makedirs("bgr_img", mode=0o777)
        bgr_path = os.path.join(COLMAP_INPUT, bgr_images[idx])
        bgr_dest_path = "bgr_img/bgr.jpg"
        shutil.copy(bgr_path, bgr_dest_path)

        ori_images = os.listdir(folder_path)
        for i, image in enumerate(ori_images):
            # create src directory
            if os.path.exists("src_img"):
                shutil.rmtree("src_img")
            os.makedirs("src_img", mode=0o777)
            img_path = os.path.join(folder_path, ori_images[i])
            img_dest_path = "src_img/src.jpg"
            shutil.copy(img_path, img_dest_path)

            subprocess.run(
                [
                    "python",
                    MATTING_SCRIPT,
                    "--model-type",
                    "mattingrefine",
                    "--model-backbone",
                    "resnet50",
                    "--model-backbone-scale",
                    "0.25",
                    "--model-refine-mode",
                    "sampling",
                    "--model-refine-sample-pixels",
                    "80000",
                    "--model-checkpoint",
                    MATTING_MODEL,
                    "--images-src",
                    "src_img/",
                    "--images-bgr",
                    "bgr_img/",
                    "--output-dir",
                    "matting_temp/".format(idx),
                    "--output-type",
                    "com",
                ]
            )

            matted_path = "matting_temp/com/src.png"
            shutil.copy(
                matted_path, "matting_all/matted{}_{}.png".format(idx, i))
            shutil.rmtree("matting_temp")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# recreate json
with open("colmap/original.json", "r") as file:
    data = json.load(file)

# Create a new dictionary to store the updated data
new_data = {
    "camera_angle_x": data["camera_angle_x"],
    "camera_angle_y": data["camera_angle_y"],
    "frames": [],
}


# # Iterate through the frames
def max_length_dir(path):
    max = 0
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        cur_len = len(os.listdir(folder_path))
        if cur_len > max:
            max = cur_len
    return max


frames = data["frames"]
n = max_length_dir(SRC_FLDR)

for idx, folder_name in enumerate(os.listdir(SRC_FLDR)):
    folder_path = os.path.join(SRC_FLDR, folder_name)

    if os.path.isdir(folder_path):
        for i, image in enumerate(os.listdir(folder_path)):
            new_file_path = os.path.join(folder_path, image)
            time = i / (n - 1)
            new_frame = {
                "file_path": new_file_path,
                "time": time,
                "transform_matrix": frames[idx]["transform_matrix"],
            }
            new_data["frames"].append(new_frame)

# # Save the updated JSON data to a new file
with open("transforms.json", "w") as file:
    json.dump(new_data, file, indent=4)
