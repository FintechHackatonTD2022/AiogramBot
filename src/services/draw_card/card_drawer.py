from io import BytesIO
from PIL import Image
from aiogram.types.input_file import InputFile

from . import draw_card


class CardDrawer:
    __template_card = Image.open(r'src/assets/card.png')
    __font_path = 'src/assets/kredit.ttf'

    @classmethod
    def draw_to_input_file(cls, card_16number: int,
                           card_expiry: str, card_holder: str) -> InputFile:
        image = cls.__draw_card(card_16number, card_expiry, card_holder)
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format='PNG')
        image_bytes_io = BytesIO(image_bytes_io.getvalue())
        return InputFile(image_bytes_io, filename='card.png')

    @classmethod
    def __draw_card(cls, card_16number: int,
                    card_expiry: str, card_holder: str) -> Image:
        return draw_card.draw_card(cls.__template_card, cls.__font_path,
                                   card_16number, card_expiry, card_holder)
