import os
import re
import io
import urllib.request
from PIL import Image, ImageFont, ImageDraw, ImageFilter
# debug
from django.conf import settings

# setup colors
palette = {
    "primary": (255, 255, 255, 230),
    "secondary": (255, 255, 255, 178),
    "red": (255, 0, 0),
}
default_font_path = 'config/templates/static/SuisseIntl-Regular.otf'
fonts = {
    "xxs": 65,
    "xs": 70,
    "sm": 80,
    "lg": 128,
}


def to_coords(
        image,
        position,  # (0.75, 0.25) - % or in pixels
        rect,  # (x, y) - size in pixels
        margins=(0, 0),  # (x, y) - margin in pixels or percents from borders
):
    coords = [0, 0]
    margins = list(margins)

    for i in range(2):
        if not isinstance(position[i], float):
            coords[i] = int(position[i])
            continue

        coord = image.size[i] * position[i]

        if isinstance(margins[i], float):
            margins[i] = image.size[i] * margins[i]

        if position[i] < 0.5:
            if coord - rect[i] // 2 < margins[i]:
                coord = margins[i] + rect[i] // 2
        else:
            if coord + rect[i] // 2 > image.size[i] - margins[i]:
                coord = image.size[i] - margins[i] - rect[i] // 2

        coords[i] = int(coord - rect[i] // 2)

    return coords


def load_image(url, default="config/templates/static/default.png"):
    try:
        path = os.path.join(settings.BASE_DIR, url)
        if os.path.exists(path):
            avatar = Image.open(path)
        else:
            avatar = Image.open(io.BytesIO(urllib.request.urlopen(
                urllib.request.Request(url,
                                       headers={'User-Agent': 'Mozilla/5.0'})
            ).read()))
    except Exception:
        avatar = Image.open(os.path.join(settings.BASE_DIR, default))
    return avatar


def get_circle_mask(size):
    size = (size, size)
    mask = Image.new("L", size, 0)
    mask_drawer = ImageDraw.Draw(mask)
    mask_drawer.ellipse((0, 0, *size), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0))
    return mask


def crop_image_cube(image):
    cube_side = min(image.size)
    width, height = image.size
    image = image.crop(((width - cube_side) // 2, (height - cube_side) // 2,
                        (width + cube_side) // 2, (height + cube_side) // 2))
    return image


# converts text to list of its words with style properties using formatters
# formatters key represents placeholder in text (like :u:) to format following text
#
# formatters = {
#   "u": lambda styles: {**styles, "font_size": fonts["xxs"], "new_line": False}, # small font size
#   "s": lambda styles: {**styles, "fill": palette["secondary"]}, # make text color secondary
#   "n": lambda styles: {**styles, "new_line": True}, # add new line before word
#   "N": lambda styles: {}, # reset additional styles
# }
#
# possible typography styles:
# font
# font_path
# font_size
# fill - color
# new_line
#
# possible image styles:
# margin_r - right
# margin_t - top
#
def get_styled_words(text, formatters={}, initial_styles={},
                     additional_styles={}):
    delimiter = re.search(":[a-zA-Z]:", text)
    left = text
    right = None
    if delimiter:
        delimiter = delimiter.group()
        right_additional_styles = additional_styles
        splitted = text.split(delimiter)
        left = splitted[0].strip()
        if delimiter[1] in formatters:
            right = get_styled_words(
                delimiter.join(splitted[1:]).strip(),
                formatters,
                initial_styles,
                formatters[delimiter[1]](right_additional_styles)
            )
        else:
            right = get_styled_words(
                " ".join(splitted[1:]),
                formatters,
                initial_styles,
                additional_styles
            )

    words_with_style = []
    for word in left.split():
        words_with_style.append({
            "word": word,
            "styles": {
                **initial_styles,
                **additional_styles,
            }
        })
        if "new_line" in additional_styles:
            del additional_styles["new_line"]
    if right:
        words_with_style += right
    return words_with_style


def get_text_image(words, max_row_width=None, line_spacing=30, space=0.2):
    image_rows_list = [[]]
    for word in words:
        # setup word font
        if not word["styles"].get('font', False):
            font_path = word["styles"].get("font_path", default_font_path)
            font_file = os.path.join(settings.BASE_DIR, font_path)
            font = ImageFont.truetype(font_file,
                                      word["styles"].get("font_size",
                                                         fonts["sm"]))
            word["styles"]["font"] = font

        # calculate word image size
        sizingKwargs = {
            "font": word["styles"]["font"],
        }

        size = ImageDraw.Draw(
            Image.new("RGBA", (0, 0), 0)
        ).textbbox((0, 0), word["word"], **sizingKwargs)[2:]

        # create word image
        word_image = Image.new("RGBA", size, 0)
        word_drawer = ImageDraw.Draw(word_image)

        # new line handler
        if "new_line" in word["styles"] and word["styles"]["new_line"]:
            image_rows_list.append([])  # add new line
            del word["styles"]["new_line"]

        # draw word
        wordImageKwargs = {
            "font": word["styles"]["font"],
            "fill": word["styles"].get("fill", palette["primary"]),
        }
        word_drawer.text(
            to_coords(word_image, (0.5, 0.5), size), word["word"],
            **wordImageKwargs
        )

        # determine where to put wort in order to respect max_row_width
        if max_row_width:
            row_width = sum([r["image"].size[0] for r in image_rows_list[-1]])
            if row_width + size[0] > max_row_width and row_width != 0:
                image_rows_list.append([])  # add new line

        image_rows_list[-1].append({
            "image": word_image,
            "styles": {
                "margin_r": word["styles"].get("margin_r", 0),
                "margin_t": word["styles"].get("margin_t", 0),
            },
        })

    rows_images = []
    for row in image_rows_list:
        # calculate sum width of spaces in text
        space_width = space * (len(row) - 1)
        if isinstance(space, float):
            space_width = int(sum([w["image"].size[1] for w in row]) * space)

        # create row image
        row_width = sum(
            [(w["image"].size[0] + w["styles"]["margin_r"]) for w in row]
        )
        row_height = max(
            [(w["image"].size[1] + w["styles"]["margin_t"]) for w in row]
        )
        row_image = Image.new("RGBA", (row_width + space_width, row_height), 0)

        # draw words on row image
        paste_x = 0
        for word in row:
            if paste_x != 0:
                space_width = space
                if isinstance(space, float):
                    space_width = int(word["image"].size[1] * space)
                paste_x += space_width

            paste_x += word["styles"]["margin_r"]
            paste_rel(
                row_image, word["image"], (paste_x, word["styles"]["margin_t"])
            )
            paste_x += word["image"].size[0]

        rows_images.append(row_image)

    # create whole text image
    max_width = max(map(lambda i: i.size[0], rows_images))
    max_height = sum(map(lambda i: i.size[1], rows_images)) \
                 + line_spacing * (len(rows_images) - 1)

    text_image = Image.new("RGBA", (max_width, max_height), 0)
    text_drawer = ImageDraw.Draw(text_image)

    # paste row images
    paste_y = 0
    for i, row in enumerate(rows_images):
        paste_rel(text_image, row, (0.5, paste_y))
        paste_y += line_spacing + row.size[1]

    return text_image


def draw_text(
        text,
        color=palette["primary"],
        font_size=fonts["sm"],
        font_path=default_font_path,
        line_spacing=24,
        space_width=0.3,
        max_width=4096,
):
    font_file = os.path.join(settings.BASE_DIR, font_path)
    font = ImageFont.truetype(font_file, font_size)

    formatters = {
        "u": lambda styles: {**styles, "font_size": fonts["xxs"],
                             "new_line": False, "margin_t": 15,
                             "margin_r": -10},  # small font fize
        "s": lambda styles: {**styles, "fill": palette["secondary"]},
        # make text color secondary
        "n": lambda styles: {**styles, "new_line": True},
        # add new line before word
        "N": lambda styles: {},  # reset additional styles
    }
    words = get_styled_words(text.strip(), formatters, {
        "font_size": font_size,
        "font_path": font_path,
        "fill": color,
    })
    text_image = get_text_image(
        words,
        max_row_width=max_width,
        line_spacing=line_spacing,
        space=space_width
    )

    return text_image


# just wrapper
def paste_rel(src_img, target_img, position, margins=(0, 0)):
    coords = to_coords(src_img, position, target_img.size, margins)
    if src_img.mode == 'RGB' and target_img.mode == 'RGBA':
        src_img.paste(target_img, coords, target_img.split()[-1])
    else:
        src_img.paste(target_img, coords)
    return coords


def get_locale(
        country_iso, country, color, flag_size=80,  # px
        spacing=30,  # px
):
    country_text_image = draw_text(country, color, fonts["xs"])

    locale_image = Image.new("RGBA", (
        flag_size + spacing + country_text_image.size[0],
        max([country_text_image.size[1], flag_size]),
    ), 0)
    locale_drawer = ImageDraw.Draw(locale_image)

    flag_image = load_image(
        f"https://flagcdn.com/h80/{country_iso.lower()}.png")
    flag_image = crop_image_cube(flag_image).resize(
        (flag_size, flag_size), Image.Resampling.LANCZOS
    )
    flag_image.putalpha(get_circle_mask(flag_size))

    paste_rel(locale_image, flag_image, (0.0, 0.0))
    paste_rel(locale_image, country_text_image, (1.0, -3))

    return locale_image


def make_image(
        user, text, background_path='config/templates/static/blue.png',
        background_size=(2048, 2048), avatar_size=(760, 760),
        avatar_coords=None,  # (x, y)
        as_bytes=True
):
    # setup base image
    background_path = os.path.join(settings.BASE_DIR, background_path)
    image = Image.open(background_path).convert("RGB").resize(
        background_size, Image.Resampling.LANCZOS
    )
    image_drawer = ImageDraw.Draw(image)

    # add avatar
    avatar_image = load_image(f"media/{user.avatar}").resize(
        avatar_size, Image.Resampling.LANCZOS
    )
    avatar_image.putalpha(get_circle_mask(avatar_size[0]))
    paste_rel(image, avatar_image, avatar_coords or (0.5, 0.31))

    # add watermark
    watermark_image = load_image(
        f"config/templates/static/watermark.png").resize(
        (735, 90), Image.Resampling.LANCZOS
    )
    paste_rel(image, watermark_image, (75, 0.055))

    # add user name
    username_text_image = draw_text(f"{user.first_name} {user.last_name}")
    un_coords = paste_rel(image, username_text_image, (0.51, 0.564))

    # add username
    text_image = draw_text(f"@{user.username}", palette["secondary"],
                           fonts["xs"])
    paste_rel(image, text_image,
              (0.51, un_coords[1] + username_text_image.size[1] + 32))

    # add message
    message_image = draw_text(
        text, font_size=fonts["lg"],
        max_width=image.size[0] - image.size[0] * .2
    )
    paste_rel(image, message_image, (0.51, 0.79))

    # add locale
    locale_image = get_locale(
        (user.country_iso or 'IT').lower(),
        user.country or 'Italy',
        palette["primary"],
    )
    paste_rel(image, locale_image, (1.0, 0.0), (65, 65))

    # debug
    # image.save("debug.png")

    if as_bytes:
        image_bytes = io.BytesIO()
        image_bytes.name = 'image.png'
        image.save(image_bytes, 'PNG')
        image_bytes.seek(0)
        return image_bytes
    else:
        return image
