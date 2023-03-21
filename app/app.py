import types
from tf.advanced.app import App


def fmt_layoutRich(app, n, **kwargs):
    return app._formatRich(n)


class TfApp(App):
    def __init__(app, *args, **kwargs):
        app.fmt_layout = types.MethodType(fmt_layoutRich, app)
        super().__init__(*args, **kwargs)

    def fmt_layoutRich(app, n, **kwargs):
        api = app.api
        F = api.F
        material = F.sign.v(n)

        return f"{material}"