from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def print_ingame_map(the_map):
    image_size = (500, 500)
    square_size = (image_size[0] // 5, image_size[1] // 5)

    image = Image.new('RGB', image_size, 'white')
    draw = ImageDraw.Draw(image)

    font_path = "./Fonts/Roboto-Regular.ttf"
    font = ImageFont.truetype(font_path, size=12)

    for i in range(len(the_map)):
        x = (i % 5) * square_size[0]
        y = (i // 5) * square_size[1]
        square_position = (x, y)

        if the_map[i].player_active:
            fill_color = '#2bef5f'
        elif the_map[i].visited:
            fill_color = '#f5fba2'
        else:
            fill_color = 'white'

        draw.rectangle([square_position, (square_position[0] + square_size[0], square_position[1] + square_size[1])],
                       outline='black', fill=fill_color)



    image.save('ingame_map.png')
    # Convert PIL Image to OpenCV Image (BGR to RGB conversion)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    cv2.imshow('Game Map', opencvImage)
    cv2.waitKey(1)  # This will refresh the window
