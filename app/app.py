from tf.advanced.app import App

class TfApp(App):
    def __init__(app, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fmt_layoutRich(app, n, **kwargs):
        api = app.api
        F = api.F
        material = F.g_cons.v(n)
        after = F.trailer.v(n) or ""
        
        #return f"{material}"
        return f"{material}{after}"