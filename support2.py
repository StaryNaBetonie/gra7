def get_rect(image, kwargs):
    rect = image.get_rect()
    for key, value in kwargs.items():
        if key == 'center': rect.center = value
        elif key == 'topleft': rect.topleft = value
    return rect