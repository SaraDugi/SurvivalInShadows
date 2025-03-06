import pygame
from misc.settings import STAMINA_COOLDOWN, SPEED_BOOST_DURATION

class Stamina:
    def __init__(self, initial_stamina=3):
        # Maximum charges available.
        self.max_stamina = initial_stamina  
        # Current available stamina charges.
        self.stamina_counter = initial_stamina
        self.speed_boost_active = False
        self.last_speed_boost = 0

    def use_stamina(self):
        """
        Uses one stamina charge to activate a speed boost.
        A boost is only activated if there is at least one charge left,
        no boost is already active, and the cooldown period has passed.
        """
        current_time = pygame.time.get_ticks()
        if self.stamina_counter > 0 and not self.speed_boost_active:
            if current_time - self.last_speed_boost >= STAMINA_COOLDOWN:
                self.last_speed_boost = current_time
                self.stamina_counter -= 1
                self.speed_boost_active = True
                print(f"Stamina used! Charges left: {self.stamina_counter}")
            else:
                print("Stamina cooldown active. Cannot use stamina yet.")
        else:
            print("Cannot use stamina: either no charges left or boost already active.")

    def restore_stamina(self, amount):
        """
        Restores a given amount of stamina charges.
        The total will not exceed the maximum allowed.
        """
        old_counter = self.stamina_counter
        self.stamina_counter = min(self.max_stamina, self.stamina_counter + amount)
        print(f"Stamina restored from {old_counter} to {self.stamina_counter}")

    def reset_speed_boost(self):
        """
        Checks if the speed boost duration has elapsed.
        If so, deactivates the boost.
        """
        if self.speed_boost_active and pygame.time.get_ticks() - self.last_speed_boost > SPEED_BOOST_DURATION:
            self.speed_boost_active = False

    def draw_stamina_items(self, screen):
        """
        Draws the current stamina charge count on the screen with a color indicator.
        Green when full, orange when medium, and red when low.
        """
        stamina_pos = (10, 80)
        font = pygame.font.Font(None, 36)
        text = "Stamina usage left: "
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, stamina_pos)

        # Choose color based on available stamina.
        if self.stamina_counter == self.max_stamina:
            color = (0, 255, 0)  # Full stamina.
        elif self.stamina_counter >= self.max_stamina // 2:
            color = (255, 165, 0)  # Medium stamina.
        else:
            color = (255, 0, 0)  # Low stamina.

        counter_surface = font.render(str(self.stamina_counter), True, color)
        screen.blit(counter_surface, (stamina_pos[0] + text_surface.get_width() + 5, stamina_pos[1]))