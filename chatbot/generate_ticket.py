# -*- coding: utf-8 -*-
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "files/ticket_base.png"
FONT_PATH = "files/Roboto-Regular.ttf"

FONT_SIZE = 20
BLACK = (0, 0, 0, 255)
NAME_OFFSET = (48, 120)
EMAIL_OFFSET = (250, 298)
FLIGHT_OFFSET = (48, 185)
NUMBER_OFFSET = (48, 250)


def generate_ticket(name, email, flight_number, number_of_seats):
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)
    draw.text(FLIGHT_OFFSET, flight_number, font=font, fill=BLACK)
    draw.text(NUMBER_OFFSET, number_of_seats, font=font, fill=BLACK)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file
