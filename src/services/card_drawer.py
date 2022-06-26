from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from aiogram.types.input_file import InputFile


class CardDrawer:
    __template_card = Image.open(r'src/assets/card.png')
    __font_path = 'src/assets/kredit.ttf'
    __font_color = (255, 255, 255)

    @ classmethod
    def draw_to_input_file(cls, card_16number: int,
                           card_expiry: str) -> InputFile:
        image = cls.__draw_card(card_16number, card_expiry)
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format='PNG')
        image_bytes_io = BytesIO(image_bytes_io.getvalue())
        return InputFile(image_bytes_io, filename='card.png')

    @ classmethod
    def __draw_card(cls, card_16number: int,
                    card_expiry: str,
                    card_holder: str = 'PREPAID CARD') -> Image:
        FONT_COLOR = cls.__font_color
        template_card = cls.__template_card.copy()
        card = ImageDraw.Draw(template_card)
        font_16number = ImageFont.truetype(cls.__font_path, 107)
        font_other = ImageFont.truetype(cls.__font_path, 65)
        card_16number_str = '   '.join(
            [str(card_16number)[i:i + 4] for i
             in range(0, len(str(card_16number)), 4)])
        card.text((375, 710), card_16number_str,
                  fill=FONT_COLOR, font=font_16number)
        card.text((350, 860), card_expiry, fill=FONT_COLOR, font=font_other)
        card.text((350, 920), card_holder, fill=FONT_COLOR, font=font_other)
        return template_card
