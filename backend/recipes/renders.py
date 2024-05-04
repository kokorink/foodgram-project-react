import io

from rest_framework import renderers


class TXTShoppingCartDataRenderer(renderers.BaseRenderer):

    media_type = "text/plain"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list):
            text_buffer = io.StringIO()

            verdicts = {}
            for ingredient in data:
                name = (f'{ingredient["name"]} '
                        f'({ingredient["measurement_unit"]})')
                amount = ingredient['amount']
                if name in verdicts:
                    verdicts[name] += amount
                else:
                    verdicts[name] = amount

            text_buffer.write(
                ''.join(f'• {name} — {amount}\n'
                        for name, amount in verdicts.items())
            )

            return text_buffer.getvalue()