def load_css(css_file: str):
    """Reads and injects a CSS file """
    with open(css_file, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"