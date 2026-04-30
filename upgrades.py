import player
from settings import *
from weapons import *
from player import *
import weapons

CARD_WIDTH = 400
CARD_HEIGHT = 600
CARD_SPACING = 50
ANIMATION_DURATION = 1000

upgrade_icon_map = {
    "Ammo Cache": "icons/PSXAmmoBoxes/PSXAmmoBoxes/#Images/Large_Ammo_Box.png"
}


class Upgrade:
    def __init__(self, x, y, card_type, title, description, icon):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.original_y = y
        self.target_y = y - 50  # Cards pop up
        self.current_y = y
        self.start_time = pygame.time.get_ticks()
        self.card_type = card_type
        self.title = title
        self.description = description
        self.icon = icon
        self.selected = False
        self.hovered = False
        self.animation_progress = 0
        self.scale = 1.0

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        #POP UP ANIMATION
        if elapsed < ANIMATION_DURATION:
            self.animation_progress = elapsed / ANIMATION_DURATION
            # Ease out effect
            ease_out = 1 - (1 - self.animation_progress) ** 3
            self.current_y = self.original_y - (self.original_y - self.target_y) * ease_out
        else:
            self.current_y = self.target_y

        #scale effect on hover
        self.scale = 1.1 if self.hovered else 1.0

    def draw(self, screen, font_large, font_small):
        # Card background with glow effect
        color = (60, 60, 80) if not self.hovered else (80, 100, 120)
        glow_color = (100, 150, 200, 100) if self.hovered else (0, 0, 0, 0)

        # Draw glow
        glow_rect = self.rect.copy()
        glow_rect.inflate_ip(20, 20)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect())
        screen.blit(glow_surf, glow_rect.topleft)

        # Main card surface with rounded corners
        card_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, color, (0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=15)
        pygame.draw.rect(card_surf, (100, 150, 200), (10, 10, CARD_WIDTH-20, CARD_HEIGHT-20), border_radius=12)
    
        # ICON AREA
        icon_rect = pygame.Rect(60, 40, 70, 70)
        pygame.draw.circle(card_surf, (255, 255, 255), icon_rect.center, 35, 3)
        if self.icon:
            icon_size = 60
            icon_scaled = pygame.transform.scale(self.icon, (icon_size, icon_size))
            # Center icon
            icon_pos = icon_scaled.get_rect(center=icon_rect.center)
            # Rounded dark background
            pygame.draw.rect(card_surf, (25, 30, 35), icon_pos.inflate(4, 4), border_radius=12)
            card_surf.blit(icon_scaled, icon_pos)
        else:
            pygame.draw.circle(card_surf, (200, 100, 50), icon_rect.center, 25)
        
        # TITLE
        title_surf = font_large.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(CARD_WIDTH//2, 100))
        card_surf.blit(title_surf, title_rect)
        
        # Description
        desc_surf = font_small.render(self.description, True, (220, 220, 220))
        desc_rect = desc_surf.get_rect(center=(CARD_WIDTH//2, 180))
        card_surf.blit(desc_surf, desc_rect)

        # Type badge
        badge_surf = pygame.Surface((CARD_WIDTH-40, 30), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (50, 100, 150, 200), badge_surf.get_rect(), border_radius=8)
        badge_text = font_small.render(self.card_type, True, (255, 255, 255))
        badge_rect = badge_text.get_rect(center=(CARD_WIDTH//2 - 20, 15))
        badge_surf.blit(badge_text, badge_rect)
        card_surf.blit(badge_surf, (20, CARD_HEIGHT-50))

        # Selection indicator
        if self.selected:
            pygame.draw.rect(card_surf, (255, 200, 100, 150), 
                        (5, 5, CARD_WIDTH-10, CARD_HEIGHT-10), 4, border_radius=12)
        
        # Scale and position
        scaled_surf = pygame.transform.scale(card_surf, 
                                        (int(CARD_WIDTH * self.scale), 
                                            int(CARD_HEIGHT * self.scale)))
        scaled_rect = scaled_surf.get_rect(center=(self.rect.centerx, int(self.current_y)))
        screen.blit(scaled_surf, scaled_rect)

    
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(mouse_pos):
                self.selected = True
                return True
            if self.rect.collidepoint(mouse_pos):
                return True
        return False

    @staticmethod
    def generate_upgrades(screen_width, screen_height, font_small):
        upgrades = [
            ["Weapon", "Shotgun fire rate", "Decrease SG fire rate.", None],
            ["Weapon", "RG Piercing Shot", "Bullets pierce through enemies.", None],
            ["Weapon", "Explosive Shot", "Increase explosion radius for ROCKETS.", None],
            ["Passive", "Increased Health", "Boosts your maximum health.", None],
            ["Passive", "Faster Reload", "Faster weapon swapping.", None],
            ["Passive", "Damage Boost", "Increases all weapon damage.", None],
            ["Health", "Health Pack", "Restores 50 HP.",None],
            ["Health", "Shield Regen", "Decreases time to shield regen.", None],
            ["Ramming", "Reinforced Hull", "Increase RAMMING damage.", None],
            ["Max Ammo", "Ammo Cache", "Increases ammo capacity for all weapons.", load_image_alpha(upgrade_icon_map["Ammo Cache"])]
        ]

        selected_upgrade = random.sample(upgrades, 3)
        total_width = 3 * CARD_WIDTH + 2 * CARD_SPACING
        start_x = (width - total_width) // 2
        y = height // 2 - CARD_HEIGHT // 2

        return [Upgrade(start_x + i * (CARD_WIDTH + CARD_SPACING), y, *data) for i, data in enumerate(selected_upgrade)]
    
    def apply_upgrade(player, weapons, upgrade_title):
        if upgrade_title == "Increased Health":
            player.max_health += 50
            player.health = player.max_health
            
        elif upgrade_title == "Faster Reload":
            # Apply to current weapon and all queued weapons
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapon.rate = int(weapon.rate * 0.9)
                    if weapon.rate < 50:
                            weapon.rate = 50
                            
        elif upgrade_title == "Damage Boost":
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapon.damage = int(weapon.damage * 1.5)
                        
        elif upgrade_title == "Health Pack":
                player.health += 50
                if player.health > player.max_health:
                    player.health = player.max_health
                    
        elif upgrade_title == "Shield Regen":
                player.shield_regeneration += 0.05
                
        elif upgrade_title == "Reinforced Hull":
                player.ram_damage += 3
                
        elif upgrade_title == "Explosive Shot":
            # Only affects Rockets - increases explosion radius
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Rockets":
                    # Increase explosion by recreating (temporary hack)
                    old_damage = weapon.damage
                    Rockets.__init__(weapon)
                    weapon.damage = old_damage * 1.5
                    # Manually set bigger explosion (since init doesn't support it yet)
                    
        elif upgrade_title == "SG fire rate":
            # Only affects Shotgun - increases spread
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Shotgun":
                    weapon.rate += -100
                    if weapon.rate < 200:
                        weapon.rate = 200
                    print(f"Shotgun spread increased to {weapon.spread}")

        elif upgrade_title == "RG Piercing Shot":
            # All weapons get damage boost and pierce
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Rail Gun":
                    if weapon is not None:
                        weapon.bullet_piercing = True
                        weapon.damage = int(weapon.damage * 1.25)

        elif upgrade_title == "Ammo Cache":
            weapons.max_ammo_bonus += 5
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapon.ammo += 5