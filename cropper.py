from PIL import Image
import os
from tqdm import tqdm
import re


def main():
    examguru_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'morderns_11_math')

    input_folder = os.path.join(examguru_folder, 'unedited')
    output_folder = os.path.join(examguru_folder, 'cropped')
    left_crop_percent = 30
    right_crop_percent = 30
    top_crop_percent = 0
    bottom_crop_percent = 0

    files = (os.listdir(input_folder))
    
    sorted_files = sorted(files, key=lambda filename: int(re.search(r'\((\d+)\)', filename).group(1)) if re.search(r'\((\d+)\)', filename) else 0)
    
    first_file_number = sorted_files[0].replace("Screenshot (", "").replace(").png", "")
    page_correction = int(first_file_number)

    crop_images_in_folder(input_folder, sorted_files, output_folder, left_crop_percent, right_crop_percent, top_crop_percent, bottom_crop_percent, page_correction)


def crop_horizontal(image_path, left_crop_percent, right_crop_percent,top_crop_percent, bottom_crop_percent, output_path):
    image = Image.open(image_path)
    original_width, original_height = image.size
    left_crop = int(original_width * (left_crop_percent / 100))
    right_crop = int(original_width * (right_crop_percent / 100))
    top_crop = int(original_width * (top_crop_percent / 100))
    bottom_crop = int(original_width * (bottom_crop_percent / 100))
    #cropped_image = image.crop((left_crop, top_crop, original_width - right_crop, original_height-bottom_crop))
    cropped_image = image.crop((left_crop, 0, original_width - right_crop, original_height))
    cropped_image.save(output_path)

def crop_images_in_folder(input_folder, sorted_files, output_folder, left_crop_percent, right_crop_percent,top_crop_percent, bottom_crop_percent, page_correction):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in tqdm(sorted_files):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_filename = get_output_filename(filename, page_correction)
            output_path = os.path.join(output_folder, output_filename)
            crop_horizontal(input_path, left_crop_percent, right_crop_percent,top_crop_percent, bottom_crop_percent, output_path)


def get_output_filename(filename, page_correction):
    page_number = str(filename).replace("Screenshot (", "").replace(").png", "")
    page_number = str(int(page_number) - page_correction + 1)
    return (page_number + ".png")

if __name__ == "__main__":
    main()