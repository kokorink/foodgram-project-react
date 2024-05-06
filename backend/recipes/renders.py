"""Рендеринг данных."""

import io

from rest_framework import renderers


class TXTShoppingCartExport(renderers.BaseRenderer):
    """Рендеринг списка покупок в текстовый формат."""

    media_type = "text/plain"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list):
            txt = io.StringIO()

            shopping_cart = {}
            for ingredient in data:
                name = ingredient["name"]
                measurement_unit = ingredient["measurement_unit"]
                amount = ingredient["amount"]
                if name in shopping_cart:
                    shopping_cart[name][0] += amount
                else:
                    shopping_cart[name] = [amount, measurement_unit]

            txt.write(
                ''.join(f'— {name}: {amount_unit[0]} ({amount_unit[1]})\n'
                        for name, amount_unit in shopping_cart.items())
            )

            return txt.getvalue()
