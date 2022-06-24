# from ast import Bytes
# from typing import Any
from PIL import Image, ImageDraw, ImageFont

# TODO: Return as BytesIO, for now draw_card() returns a PIL.Image
# from io import BytesIO

FONT_COLOR = (255, 255, 255)


def draw_card(card_16number: int,
              card_expiry: str, card_holder: str, card_cvv: int):
    template_card = Image.open(r'src/assets/card.png')
    font_path = 'src/assets/kredit.ttf'
    card = ImageDraw.Draw(template_card)
    font_16number = ImageFont.truetype(font_path, 107)
    font_other = ImageFont.truetype(font_path, 65)
    card_16number_str = '   '.join(
        [str(card_16number)[i:i + 4] for i
         in range(0, len(str(card_16number)), 4)])
    card.text((375, 710), card_16number_str,
              fill=FONT_COLOR, font=font_16number)
    card.text((350, 860), card_expiry, fill=FONT_COLOR, font=font_other)
    card.text((350, 920), card_holder, fill=FONT_COLOR, font=font_other)
    # TODO: Decide what to do with this.
    # card.text((1350, 860), f"CVV: {card_cvv}",
    #           fill=FONT_COLOR, font=font_other)
    # result = BytesIO()
    # template_card = template_card.save(result, format="png")

    return template_card


if __name__ == "__main__":
    img = Image.open(r'assets/card.png')
    font_path = 'assets/kredit.ttf'
    result = draw_card(img, font_path, 1234567890991337,
                       "13/37", "DOOM SLAYER", 228)
