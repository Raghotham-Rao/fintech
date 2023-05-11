def span(content, **kwargs):
    style_options = ""
    if kwargs is not None:
        style_options = "; ".join([f'{k}: {v}' for k, v in kwargs.items()])

    return f'<span style="{style_options}">{content}</span>'