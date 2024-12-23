import plotly.graph_objects as go


def load_css(css_file: str):
    """Reads and injects a CSS file """
    with open(css_file, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"


# ---  Variables ----

stocks_lists = {"US":["^GSPC", "^DJI", "^IXIC", "^RUT"],
                "Canada":["^GSPTSE", "TX60.TS", "^TXSC", "^SPCDNX"],
                "Mexico":["^MXX", "^INMEX", "^FIBRAS", "^IPC-L"],
                "Currencies":["EURUSD=X", "USDJPY=X", "GBPUSD=X","USDCAD=X"]}