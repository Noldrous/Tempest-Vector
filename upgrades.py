import player
from settings import *
from weapons import *
from player import *
import weapons

CARD_WIDTH = int(width // 3.5)
CARD_HEIGHT = int(height // 1.25)
CARD_SPACING = 35
ANIMATION_DURATION = 1500

upgrade_icon_map = {
    "Ricochet Rounds": "icons/ricochet.png",
    "Pellet Scatter": "icons/shotgun-rounds.png",
    "Piercing Shot": "icons/piercing_shot.png",
    "Explosive Shot": "icons/explosion.png",
    "Increased Health": "icons/health_increase.png",
    "Faster Rate of Fire": "icons/fire_rate.png",
    "Damage Boost": "icons/damage_upgrade.png",
    "Shield Regen": "icons/armor-upgrade.png",
    "Reinforced Hull": "icons/ram-profile.png",
    "Ammo Cache": "icons/ammo-box.png",
    "Fortified Shield": "icons/bordered-shield.png",
    "Thruster Optimization": "icons/thruster-upgrade.png",
}

class Upgrade:
    def __init__(self, x, y, card_type, title, description, icon):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.original_y = y + height
        self.target_y = y   # Cards pop up
        self.start_time = pygame.time.get_ticks()
        self.card_type = card_type
        self.title = title
        self.description = description
        self.icon = icon
        self.selected = False
        self.hovered = False
        self.animation_progress = 0
        self.scale = 1.0
        self.animating_out = False
        self.animation_direction = 0  # -1 = up, 1 = down
        self.animation_speed = 45
        self.alpha = 255

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        # ENTRY ANIMATION
        if not self.animating_out:
            if elapsed < ANIMATION_DURATION:
                t = elapsed / ANIMATION_DURATION
                ease_out = 1 - (1 - t) ** 3

                new_y = self.original_y - (self.original_y - self.target_y) * ease_out
                self.rect.y = int(new_y)
            else:
                self.rect.y = self.target_y

            self.scale = 1.1 if self.hovered else 1.0

        # EXIT ANIMATION
        else:
            self.rect.y += self.animation_speed * self.animation_direction

            # Selected card grows slightly
            if self.selected:
                self.scale = min(self.scale + 0.02, 1.2)

            self.alpha = max(0, self.alpha - 8)

    def draw(self, screen, font_large, font_small):
        # Card background with glow effect
        color = (18, 24, 32) if not self.hovered else (0, 200, 255)
        glow_color = (0, 200, 255, 120) if self.hovered else (0, 0, 0, 0)

        # Draw glow
        glow_rect = self.rect.copy()
        glow_rect.inflate_ip(20, 20)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect())
        screen.blit(glow_surf, glow_rect.topleft)

        # Main card surface with rounded corners
        card_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, color, (0, 0, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(card_surf, (28, 40, 58), (10, 10, CARD_WIDTH-20, CARD_HEIGHT-20))

        # Grid pattern
        inner_rect = pygame.Rect(10, 10, CARD_WIDTH - 20, CARD_HEIGHT - 20)
        pygame.draw.rect(card_surf, (28, 40, 58), inner_rect)
        grid_size = 20
        grid_color = (40, 55, 75)
        
        # Draw vertical grid lines
        for x in range(inner_rect.left + grid_size, inner_rect.right, grid_size):
            pygame.draw.line(card_surf, grid_color, (x, inner_rect.top), (x, inner_rect.bottom - 1), 1)
            
        # Draw horizontal grid lines
        for y in range(inner_rect.top + grid_size, inner_rect.bottom, grid_size):
            pygame.draw.line(card_surf, grid_color, (inner_rect.left, y), (inner_rect.right - 1, y), 1)

        # ICON AREA
        icon_size = int(CARD_WIDTH * 0.5)
        icon_scaled = pygame.transform.scale(self.icon, (icon_size, icon_size))
        icon_center = (CARD_WIDTH // 2, 150)
        icon_rect = icon_scaled.get_rect(center=icon_center)
        bg_rect = icon_rect.inflate(30, 30)
        pygame.draw.rect(card_surf, (25, 30, 35), bg_rect)

        if self.hovered:
            pygame.draw.rect(card_surf, (100, 150, 200), bg_rect, 3)

        card_surf.blit(icon_scaled, icon_rect)
        
        # TITLE
        title_surf = font_large.render(self.title, False, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(CARD_WIDTH//2, 300))
        card_surf.blit(title_surf, title_rect)
        
        # Description
        desc_surf = font_small.render(self.description, False, (220, 220, 220))
        desc_rect = desc_surf.get_rect(center=(CARD_WIDTH//2, 320))
        card_surf.blit(desc_surf, desc_rect)

        # Type badge
        badge_surf = pygame.Surface((CARD_WIDTH-40, 30), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (50, 100, 150, 200), badge_surf.get_rect())
        badge_text = font_small.render(self.card_type, True, (255, 255, 255))
        badge_rect = badge_text.get_rect(center=(CARD_WIDTH//2 - 20, 15))
        badge_surf.blit(badge_text, badge_rect)
        card_surf.blit(badge_surf, (20, CARD_HEIGHT-50))

        # Selection indicator
        if self.selected:
            pygame.draw.rect(card_surf, (255, 200, 100, 150), (5, 5, CARD_WIDTH-10, CARD_HEIGHT-10), 4)
        
        # Scale and position
        scaled_surf = pygame.transform.scale(card_surf, (int(CARD_WIDTH * self.scale), int(CARD_HEIGHT * self.scale)))
        scaled_rect = scaled_surf.get_rect(center=self.rect.center)
        screen.blit(scaled_surf, scaled_rect)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(mouse_pos):
                self.selected = True
                return True
        return False

    @staticmethod
    def generate_upgrades():
        upgrades = [
            ["Weapon", "Ricochet Rounds", "Improve machinegun bullet bounce.", load_image_alpha(upgrade_icon_map["Ricochet Rounds"])],
            ["Weapon", "Pellet Scatter", "Increase number of shotgun pellets.", load_image_alpha(upgrade_icon_map["Pellet Scatter"])],
            ["Weapon", "Piercing Shot", "Enhance railgun pierce capability.", load_image_alpha(upgrade_icon_map["Piercing Shot"])],
            ["Weapon", "Explosive Shot", "Wider blast radius for rockets.", load_image_alpha(upgrade_icon_map["Explosive Shot"])],
            ["Utility", "Ammo Cache", "Ammo reserves expanded.", load_image_alpha(upgrade_icon_map["Ammo Cache"])],
            ["Offense", "Damage Amplifier", "Weapon output amplified.", load_image_alpha(upgrade_icon_map["Damage Boost"])],
            ["Offense", "Burst Overclock", "Faster fire rate and turn speed.", load_image_alpha(upgrade_icon_map["Faster Rate of Fire"])],
            ["Offense", "Reinforced Hull", "Increased RAMMING damage.", load_image_alpha(upgrade_icon_map["Reinforced Hull"])],
            ["Defense", "Vitality Boost", "Core integrity boosted.", load_image_alpha(upgrade_icon_map["Increased Health"])],
            ["Defense", "Shield Matrix", "Shield capacity and regen boosted.", load_image_alpha(upgrade_icon_map["Fortified Shield"])],
            ["Mobility", "Thruster Optimization", "Enhanced thrust output.", load_image_alpha(upgrade_icon_map["Thruster Optimization"])],
        ]

        selected_upgrade = random.sample(upgrades, 3)
        total_width = 3 * CARD_WIDTH + 2 * CARD_SPACING
        start_x = (width - total_width) // 2
        y = height // 2 - CARD_HEIGHT // 2

        return [Upgrade(start_x + i * (CARD_WIDTH + CARD_SPACING), y, *data) for i, data in enumerate(selected_upgrade)]
    
    def apply_upgrade(player, weapons, upgrade_title):
        if upgrade_title == "Vitality Boost":
            player.max_health *= 1.4
            player.health = player.max_health

        elif upgrade_title == "Shield Matrix":
            player.max_shield *= 1.20
            player.shield_regeneration += 0.025
            player.shield_regen_delay -= 10
            player.shield = player.max_shield

        elif upgrade_title == "Thruster Optimization":
            player.max_speed += 2
            player.thrust_power += 0.15

        elif upgrade_title == "Burst Overclock":
            player.turn_speed += 0.03
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapon.rate = int(weapon.rate * 0.85)
                    if weapon.rate < 50:
                            weapon.rate = 50

        elif upgrade_title == "Damage Amplifier":
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapon.damage = int(weapon.damage * 1.3)
                
        elif upgrade_title == "Reinforced Hull":
                player.ram_damage *= 1.6
                player.max_shield += 25
                player.shield_regen_delay -= 5
                player.shield = player.max_shield

        elif upgrade_title == "Ricochet Rounds":
            # Only affects Machine Gun - add bullet bounce
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Machine Gun":
                    if weapon is not None:
                        weapon.bullet_bounce = True
                        weapon.bounce_count += 2
                        weapon.damage = int(weapon.damage * 1.15)
                        weapon.ammo += 10

        elif upgrade_title == "Pellet Scatter":
            # Only affects Shotgun - increases spread and pellet count
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Shotgun":
                    if weapon is not None:
                        weapon.bullet_count += 3
                        weapon.spread += 2
                        weapon.ammo += 2

        elif upgrade_title == "Piercing Shot":
            # Only affects Railguns - increase pierce level
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Rail Gun":
                    if weapon is not None:
                        weapon.bullet_piercing = True
                        weapon.pierce_level += 2
                        weapon.ammo += 2

        elif upgrade_title == "Explosive Shot":
            # Only affects Rockets - increases explosion radius
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon.name == "Rockets":
                    if weapon is not None:
                        weapon.damage = int(weapon.damage * 1.2)
                        weapon.explosion_radius = int(weapon.explosion_radius * 1.25)
                        weapon.ammo += 1

        elif upgrade_title == "Ammo Cache":
            all_weapons = weapons.queue + [weapons.main]
            for weapon in all_weapons:
                if weapon is not None:
                    weapons.original_ammo[weapon.name] = math.ceil(weapons.original_ammo[weapon.name] * 1.25)
                    weapon.ammo = weapons.original_ammo[weapon.name]