from PIL import Image


def watermark_with_transparency(input_image_path, watermark_image_path, output_image_path=None,  position=None):
    input_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    if watermark.mode != 'RGBA':
        watermark = watermark.convert("RGBA")
    while watermark.size > input_image.size:
        watermark = watermark.resize(tuple(map(lambda x: x/2, watermark.size)))
    width_of_input_image, height_of_input_image = input_image.size
    width_of_watermark, height_of_watermark = watermark.size
    if not position or not isinstance(position, tuple):
        position = (int(width_of_input_image / 2 - width_of_watermark / 2),
                    int(height_of_input_image / 2 - height_of_watermark / 2))
    input_image_copy = input_image.copy()
    input_image_copy.paste(watermark, position, mask=watermark)
    input_image_copy.save(output_image_path if output_image_path else input_image_path)
