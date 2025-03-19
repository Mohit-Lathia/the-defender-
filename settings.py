import pygame

class Settings:
    def __init__(self, screen, available_fonts, initial_font_size=24, initial_font="arial"):
        self.screen = screen
        self.available_fonts = available_fonts
        self.current_font_index = available_fonts.index(initial_font) if initial_font in available_fonts else 0
        self.font_size = initial_font_size
        self.font_color = "red"

        # Define text-based button properties
        self.button_color_active = "blue"
        self.button_color_inactive = "yellow"

        # Define text-based button properties
        self.button_font = pygame.font.SysFont("arial", 24, bold=True)
        self.buttons = {
            "Back": (332, 450),
            "Font +": (500, 200),
            "Font -": (500, 250),
            "Next Font": (500, 300),
            "Prev Font": (200, 300)
        }

    def draw_text(self, text, font, text_col, x, y):
        text_surface = font.render(text, True, text_col)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, pos, font):
        # Create a text-based button
        button_rect = pygame.Rect(pos[0], pos[1], 140, 40)
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Button color on hover
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_color_active, button_rect)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, self.button_color_inactive, button_rect)
        self.draw_text(text, font, "black", pos[0] + 10, pos[1] + 5)
        return False  


    def draw(self):
        self.screen.fill("green")
        pygame.draw.rect(self.screen, "black", (150, 100, 500, 400), border_radius=30)

        # Current font for rendering
        current_font = pygame.font.SysFont(self.available_fonts[self.current_font_index], self.font_size, bold=True)

        # Display current settings
        self.draw_text("TEXT SETTINGS", current_font, self.font_color, 250, 120)
        self.draw_text(f"Font: {self.available_fonts[self.current_font_index]}", current_font, self.font_color, 200, 200)
        self.draw_text(f"Size: {self.font_size}", current_font, self.font_color, 200, 250)
        self.draw_text("Preview Text", current_font, self.font_color, 250, 350)

        # Draw text-based buttons
        if self.draw_button("Back", self.buttons["Back"], current_font):
            return "main"

        if self.draw_button("Font +", self.buttons["Font +"], current_font):
            self.font_size = min(self.font_size + 2, 72)

        if self.draw_button("Font -", self.buttons["Font -"], current_font):
            self.font_size = max(self.font_size - 2, 12)

        if self.draw_button("Next Font", self.buttons["Next Font"], current_font):
            self.current_font_index = (self.current_font_index + 1) % len(self.available_fonts)

        if self.draw_button("Prev Font", self.buttons["Prev Font"], current_font):
            self.current_font_index = (self.current_font_index - 1) % len(self.available_fonts)

        return "text_settings"

    def get_current_font(self):
        return self.available_fonts[self.current_font_index]

    def get_current_font_size(self):
        return self.font_size
