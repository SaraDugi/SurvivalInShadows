import pygame

class Inventory:
    def __init__(self):
        self.items = {}
        self.is_open = False

    def add_item(self, item):
        key = type(item).__name__
        if key in self.items:
            self.items[key]['count'] += 1
        else:
            self.items[key] = {"image": item.image, "count": 1}
        print(f"Added {key} to inventory. Count: {self.items[key]['count']}")

    def toggle_inventory(self):
        self.is_open = not self.is_open

    def close_inventory(self):
        self.is_open = False

    def render_inventory_screen(self, screen, font):
        if not self.is_open:
            return

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        title_text = font.render("Inventory", True, (255, 255, 255))
        screen.blit(title_text, (50, 20))

        x, y = 50, 60
        for key, data in self.items.items():
            image = data["image"]
            screen.blit(image, (x, y))
            count_text = font.render(str(data["count"]), True, (255, 255, 255))
            screen.blit(count_text, (x, y + image.get_height() + 5))
            x += image.get_width() + 20

        close_text = font.render("Press ESC to close inventory", True, (255, 255, 255))
        screen.blit(close_text, (50, screen.get_height() - 40))