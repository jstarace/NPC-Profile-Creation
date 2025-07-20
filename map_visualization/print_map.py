from PIL import Image, ImageDraw, ImageFont

def print_map(map_layout):
    image_size = (500, 575)  # Increase height to accommodate legend
    square_size = (image_size[0] // 5, 500 // 5)  # Maintain square size for the map

    image = Image.new('RGB', image_size, 'white')  # Create a new blank image
    draw = ImageDraw.Draw(image)  # Create a draw object to modify the image

    font_path = "./Fonts/Roboto-Regular.ttf"
    font = ImageFont.truetype(font_path, size=12)  # Load a font

    vertical_offset = 4  # Define a vertical offset for spacing between items

    for i in range(len(map_layout)):
        for j in range(len(map_layout[i])):
            square_position = (j * square_size[0], i * square_size[1])  # Calculate the position of the square

            # Check for content and set fill color
            contains_entrance = any('entrance' in t for t in map_layout[i][j])
            contains_exit = any('exit' in t for t in map_layout[i][j])
            contains_L = any(t.startswith('L') for t in map_layout[i][j])
            contains_RE = any(t.startswith('RE') for t in map_layout[i][j])

            if contains_entrance:
                fill_color = '#2bef5f'  # Green for entrance
            elif contains_exit:
                fill_color = '#ed264d'  # Red for exit
            elif contains_L and contains_RE:
                fill_color = 'lightblue'  # Light blue if both 'L' and 'RE' are present
            elif contains_L:
                fill_color = '#f5fba2'  # Light yellow for loot only
            elif contains_RE:
                fill_color = '#e6e6fa'  # Light purple for random encounter only
            else:
                fill_color = 'white'  # Default color

            # Draw the square with the determined fill color
            draw.rectangle(
                [square_position, (square_position[0] + square_size[0], square_position[1] + square_size[1])],
                outline='black', fill=fill_color)

            total_height = 0  # Total height of all previous items in the same square
            for k in range(len(map_layout[i][j])):
                text = map_layout[i][j][k][:4]  # Get the first four characters of the text
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]  # Calculate the width of the bounding box
                text_height = bbox[3] - bbox[1]  # Calculate the height of the bounding box

                # Calculate the text position with the vertical offset for spacing
                text_position = ((j * square_size[0]) + (square_size[0] - text_width) // 2 - bbox[0],
                                 (i * square_size[1]) + total_height + (square_size[1] - text_height) // 2 - bbox[1])

                # Draw the text in black
                draw.text(text_position, text, font=font, fill='black')

                total_height += text_height + vertical_offset  # Update total height with the current item's height

    # Add legend
    legend_items = [
        ("Loot & Random Encounter", "lightblue"),
        ("Loot Only", "#f5fba2"),
        ("Random Encounter Only", "#e6e6fa"),
        ("Entrance", "#2bef5f"),
        ("Exit", "#ed264d")
    ]

    legend_x = 10
    legend_y = 510
    legend_box_size = 20
    legend_spacing = 10  # Space between legend items

    # Draw the first three legend items horizontally
    for label, color in legend_items[:3]:
        draw.rectangle([legend_x, legend_y, legend_x + legend_box_size, legend_y + legend_box_size], fill=color, outline="black")
        draw.text((legend_x + legend_box_size + legend_spacing, legend_y), label, font=font, fill="black")
        bbox = font.getbbox(label)
        text_width = bbox[2] - bbox[0]  # Calculate the width of the bounding box
        legend_x += legend_box_size + text_width + legend_spacing + 10 # Move to the next legend item horizontally

    # Reset legend_x and move legend_y down for the next line
    legend_x = 10
    legend_y += legend_box_size + legend_spacing

    # Draw the remaining legend items horizontally on the next line
    for label, color in legend_items[3:]:
        draw.rectangle([legend_x, legend_y, legend_x + legend_box_size, legend_y + legend_box_size], fill=color, outline="black")
        draw.text((legend_x + legend_box_size + legend_spacing, legend_y), label, font=font, fill="black")
        bbox = font.getbbox(label)
        text_width = bbox[2] - bbox[0]  # Calculate the width of the bounding box
        legend_x += legend_box_size + text_width + legend_spacing + 10 # Move to the next legend item horizontally

    # Save the image as 'map.png'
    image.save('map.png')
