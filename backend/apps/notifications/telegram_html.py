"""Convert stored rich HTML to the subset accepted by Telegram sendMessage."""
from html import escape
from html.parser import HTMLParser
from urllib.parse import urljoin

import nh3


FORMATTING = {'b', 'strong', 'i', 'em', 'u', 's', 'strike', 'del', 'code', 'pre'}
BLOCKS = {'p', 'div', 'ul', 'ol', 'li', 'tr', 'blockquote', 'figure', 'figcaption',
          'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


class TelegramHTML(HTMLParser):
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.parts = []
        self.links = []
        self.cell_depth = 0
        self.cell_count = 0

    def newline(self):
        if self.parts and not self.parts[-1].endswith(('\n', '• ')):
            self.parts.append('\n')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in FORMATTING:
            self.parts.append(f'<{tag}>')
        elif tag == 'a':
            href = attrs.get('href')
            self.links.append(bool(href))
            if href:
                href = urljoin(self.base_url, href)
                self.parts.append(f'<a href="{escape(href, quote=True)}">')
        elif tag in {'td', 'th'}:
            if self.cell_count:
                self.parts.append(' | ')
            self.cell_count += 1
            self.cell_depth += 1
        elif tag in BLOCKS:
            if tag != 'p' or not self.cell_depth:
                self.newline()
            if tag == 'tr':
                self.cell_count = 0
            if tag == 'li':
                self.parts.append('• ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'hr':
            self.newline()
            self.parts.append('———\n')
        elif tag == 'img' and attrs.get('src'):
            self.newline()
            url = escape(urljoin(self.base_url, attrs['src']), quote=True)
            label = escape(attrs.get('alt') or 'Изображение')
            self.parts.append(f'<a href="{url}">{label}</a>\n')

    def handle_endtag(self, tag):
        if tag in FORMATTING:
            self.parts.append(f'</{tag}>')
        elif tag == 'a':
            if self.links.pop():
                self.parts.append('</a>')
        elif tag in BLOCKS:
            if tag != 'p' or not self.cell_depth:
                self.newline()
        elif tag in {'td', 'th'}:
            self.cell_depth -= 1

    def handle_data(self, data):
        self.parts.append(escape(data, quote=False))


def telegram_html(value, *, base_url):
    # Clean legacy HTML as well as current editor output before parsing it.
    clean = nh3.clean(value or '', tags=FORMATTING | BLOCKS | {
        'a', 'br', 'hr', 'img', 'table', 'thead', 'tbody', 'tfoot', 'td', 'th'},
                     attributes={'a': {'href'}, 'img': {'src', 'alt'}},
                     url_schemes={'http', 'https', 'mailto', 'tg'}, link_rel=None)
    parser = TelegramHTML(base_url)
    parser.feed(clean)
    parser.close()
    return ''.join(parser.parts).strip()
