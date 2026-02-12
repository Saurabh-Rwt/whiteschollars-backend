from html import escape
from html.parser import HTMLParser


ALLOWED_TAGS = {
    'p',
    'br',
    'strong',
    'em',
    'ul',
    'ol',
    'li',
    'a',
}

ALLOWED_ATTRS = {
    'a': {'href', 'target', 'rel'},
}

SELF_CLOSING = {'br'}


class _Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS:
            return

        if tag in SELF_CLOSING:
            self._parts.append(f"<{tag}>")
            return

        attrs_dict = {key: value for key, value in attrs if value is not None}
        safe_attrs = []

        if tag in ALLOWED_ATTRS:
            for key in ALLOWED_ATTRS[tag]:
                if key not in attrs_dict:
                    continue
                value = attrs_dict.get(key, '')
                if key == 'href':
                    if value.lower().startswith('javascript:'):
                        continue
                if key == 'target':
                    value = '_blank'
                if key == 'rel':
                    value = 'noopener noreferrer'
                safe_attrs.append(f'{key}="{escape(value, quote=True)}"')

        if tag == 'a' and not any(attr.startswith('rel=') for attr in safe_attrs):
            safe_attrs.append('rel="noopener noreferrer"')

        attrs_out = f" {' '.join(safe_attrs)}" if safe_attrs else ''
        self._parts.append(f"<{tag}{attrs_out}>")

    def handle_endtag(self, tag):
        if tag in ALLOWED_TAGS and tag not in SELF_CLOSING:
            self._parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data:
            self._parts.append(escape(data))

    def handle_entityref(self, name):
        self._parts.append(f"&{name};")

    def handle_charref(self, name):
        self._parts.append(f"&#{name};")

    def get_html(self):
        return ''.join(self._parts)


def sanitize_html(value):
    if not value:
        return ''
    parser = _Sanitizer()
    parser.feed(value)
    return parser.get_html()
