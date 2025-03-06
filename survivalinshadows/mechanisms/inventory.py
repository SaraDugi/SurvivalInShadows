import pygame
from misc.settings import WHITE, BLACK, RED

class Inventory:
    def __init__(self):
        """
        Initializes an inventory for the player.
        """
        self.items = []  # ✅ List to store inventory items
        self.capacity = 5  # ✅ Max number of items
        self.is_open = False  # ✅ Track if inventory is open
        self.selected_index = 0  # ✅ Highlighted item in inventory

    def add_item(self, item):
        """
        Adds an item to the inventory if there's space.
        """
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added {item} to inventory.")
        else:
            print("Inventory is full!")

    def remove_item(self):
        """
        Removes the currently selected item from the inventory.
        """
        if self.items and 0 <= self.selected_index < len(self.items):
            removed_item = self.items.pop(self.selected_index)
            print(f"Removed {removed_item} from inventory.")
            self.selected_index = max(0, self.selected_index - 1)  # ✅ Adjust selection

    def toggle_inventory(self):
        """
        Opens/closes the inventory.
        """
        self.is_open = not self.is_open

    def handle_event(self, event):
        """
        Handles keyboard navigation in inventory.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items) if self.items else 0
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items) if self.items else 0
            elif event.key == pygame.K_RETURN:
                self.remove_item()  # ✅ Remove item when pressing ENTER
            elif event.key == pygame.K_i:
                self.toggle_inventory()  # ✅ Close inventory

    def render_inventory_screen(self, screen, font):
        """
        Displays the inventory screen.
        """
        if self.is_open:
            screen.fill(BLACK)  # ✅ Dark background for inventory

            title_text = font.render("Inventory", True, WHITE)
            screen.blit(title_text, (50, 50))

            for i, item in enumerate(self.items):
                color = RED if i == self.selected_index else WHITE
                item_text = font.render(f"- {item}", True, color)
                screen.blit(item_text, (50, 100 + i * 40))  # ✅ Position items

            close_text = font.render("Press I to Close | ENTER to Remove Item", True, WHITE)
            screen.blit(close_text, (50, 400))

            pygame.display.flip()