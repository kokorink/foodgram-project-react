"""Рендеринг данных."""

import io

from rest_framework import renderers

AMOUNT_INDEX = 0
MEASUREMENT_UNIT_INDEX = 1


class ShoppingCartToTXTExport(renderers.BaseRenderer):
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
                    shopping_cart[name][AMOUNT_INDEX] += amount
                else:
                    shopping_cart[name] = [amount, measurement_unit]

            txt.write(
                ''.join(f'— {name}: {amount_unit[AMOUNT_INDEX]} ({amount_unit[MEASUREMENT_UNIT_INDEX]})\n'
                        for name, amount_unit in shopping_cart.items())
            )

            return txt.getvalue()
