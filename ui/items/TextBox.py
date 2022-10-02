from ui.GuiItem import GuiItem

class TextBox(GuiItem):
    def __init__(self, gui, x, y, w, h, center=(None, None), background_colour=None, background_image=None, text="Default Text", text_font="Arial", text_colour=(255, 255, 255), font_size=24, is_sys_font=True) -> None:
        super().__init__(gui, x, y, w, h, center, background_colour, background_image, text, text_font, text_colour, font_size, is_sys_font, False)