from PIL import Image, ImageDraw, ImageFont
import os
import math
from tqdm import tqdm
import re


def main():
    folders = ['morderns_11_math']
    for i in folders:
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), i)
        print(f"Processing: {folder}")
        process_folder(folder)
        print(f"{folder} Completed")

def process_folder(folder):
    input_folder = os.path.join(folder, 'cropped')
    output_folder = os.path.join(folder, 'edited')
    box_height = 90  # Set the desired height of the white box
    text_position = 20  # Adjust as needed
    watermark_text = "Isucceed Coaching Class"  # Replace with your watermark text
    opacity = 0.4  # Set opacity for the watermark
    angle = 58  # Set the rotation angle for the diagonal watermark
    box_position = "top"
    #box_position = "bottom"


    process_images_in_folder(input_folder, output_folder, box_height, text_position, watermark_text, opacity, angle, box_position)


def superimpose_page_number(image, filename):
    page_number = str(filename).replace(".png", "")
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font = ImageFont.truetype(font_path, 15)
    text = f"Page {page_number}"
    text_width, text_height = draw.textsize(text, font)
    text_position = ((image_width - text_width) // 2, image_height - text_height - 10)
    text_color = (0, 0, 0)
    draw.text(text_position, text, font=font, fill=text_color)
    return image

def superimpose_white_box(image, box_height, box_position):
    image_width, image_height = image.size
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    box = Image.new("RGBA", (image_width, box_height), (255, 255, 255, 255))
    if box_position == "top":
        overlay.paste(box, (0, 0))
    else:
        overlay.paste(box, (0, image_height - box_height))
    result = Image.alpha_composite(image.convert("RGBA"), overlay)
    return result

def superimpose_text(image, text, font_path, font_size, text_color, position):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(text, font)
    text_position = ((image.width - text_width) // 2, position)
    draw.text(text_position, text, font=font, fill=text_color)
    return image

def superimpose_diagonal_watermark(image, watermark_text, font_path, font_size, text_color, opacity, angle):
    image_with_watermark = image.copy()
    watermark = Image.new("RGBA", image_with_watermark.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark, "RGBA")
    font = ImageFont.truetype(font_path, 85)
    text_width, text_height = draw.textsize(watermark_text, font)
    diagonal_length = math.sqrt(text_width**2 + text_height**2)
    rotated_text_image = Image.new("RGBA", (int(diagonal_length), 85), (0, 0, 0, 0))
    rotated_draw = ImageDraw.Draw(rotated_text_image)
    rotated_draw.text((0, 0), watermark_text, font=font, fill=text_color + (int(255 * opacity),))
    rotated_text = rotated_text_image.rotate(angle, expand=True)
    watermark.paste(rotated_text, (0, 0), rotated_text)
    image_with_watermark = Image.alpha_composite(image_with_watermark.convert("RGBA"), watermark)
    return image_with_watermark

def process_images_in_folder(input_folder, output_folder, box_height, text_position, watermark_text, opacity, angle, box_position):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    text_to_add = "Isucceed Coaching Class"
    text_color = (0, 0, 0)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font_size = 15
    sorted_files = sorted(os.listdir(input_folder), key=lambda filename: int(filename.replace(".png", "")))
    for filename in tqdm(sorted_files):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            image = Image.open(input_path)
            image_with_white_box = superimpose_white_box(image, box_height, box_position)
            #image_with_white_box = superimpose_white_box(image_with_white_box, 50, "bottom")
            image_with_page_number = superimpose_page_number(image_with_white_box, filename)
            image_with_text = superimpose_text(image_with_page_number, text_to_add, font_path, font_size, text_color, text_position)
            image_with_watermark = superimpose_diagonal_watermark(image_with_text, watermark_text, font_path, font_size, text_color, opacity, angle)
            image_with_watermark.save(os.path.join(output_folder, filename))

if __name__ == "__main__":
    main()