import pygame
import sys
from bazar_logic import (
    ITEMS,
    discounted_price,
    can_buy,
    remaining_budget,
    calculate_savings,
    has_affordable_option,
)

pygame.init()
WIDTH, HEIGHT = 720, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bazar Boss: Budget Shopping")

FONT_LG = pygame.font.SysFont("arial", 28, bold=True)
FONT_MD = pygame.font.SysFont("arial", 20)
FONT_SM = pygame.font.SysFont("arial", 16)

BG_COLOR = (245, 247, 250)
CARD_COLOR = (255, 255, 255)
TEXT_DARK = (30, 41, 59)
ACCENT_BLUE = (37, 99, 235)
ACCENT_GREEN = (22, 163, 74)
ACCENT_RED = (220, 38, 38)
GRAY_BTN = (203, 213, 225)


def draw_button(rect, text, color, text_color=(255, 255, 255)):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = FONT_MD.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


def main():
    clock = pygame.time.Clock()
    budget = 505.0
    coupon_available = True
    use_coupon = False
    total_paid = 0.0
    item_idx = 0
    status_msg = "Select Shop A or Shop B to buy the current item."
    status_color = TEXT_DARK
    game_state = "PLAYING"  # PLAYING, WON, LOST

    reference_total = sum(max(i["A"], i["B"]) for i in ITEMS)

    btn_a = pygame.Rect(110, 260, 220, 65)
    btn_b = pygame.Rect(390, 260, 220, 65)
    btn_coupon = pygame.Rect(210, 350, 300, 45)
    btn_restart = pygame.Rect(260, 390, 200, 50)

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if game_state == "PLAYING":
                    if coupon_available and btn_coupon.collidepoint(pos):
                        use_coupon = not use_coupon

                    chosen_shop = None
                    if btn_a.collidepoint(pos):
                        chosen_shop = "A"
                    elif btn_b.collidepoint(pos):
                        chosen_shop = "B"

                    if chosen_shop:
                        item = ITEMS[item_idx]
                        cost = discounted_price(item[chosen_shop], use_coupon)
                        if can_buy(budget, cost):
                            budget = remaining_budget(budget, cost)
                            total_paid = round(total_paid + cost, 2)
                            if use_coupon:
                                coupon_available = False
                                use_coupon = False
                            status_msg = f"Bought {item['name']} (Shop {chosen_shop}) for {cost:.2f} BDT!"
                            status_color = ACCENT_GREEN
                            item_idx += 1

                            if item_idx >= len(ITEMS):
                                game_state = "WON"
                            elif not has_affordable_option(ITEMS[item_idx], budget, coupon_available):
                                game_state = "LOST"
                        else:
                            status_msg = f"Rejected! {cost:.2f} BDT exceeds remaining {budget:.2f} BDT."
                            status_color = ACCENT_RED

                elif btn_restart.collidepoint(pos):
                    budget = 505.0
                    coupon_available = True
                    use_coupon = False
                    total_paid = 0.0
                    item_idx = 0
                    status_msg = "Select Shop A or Shop B to buy the current item."
                    status_color = TEXT_DARK
                    game_state = "PLAYING"

        # Header Bar
        title = FONT_LG.render("BAZAR BOSS: BUDGET SHOPPING", True, TEXT_DARK)
        screen.blit(title, (30, 20))

        hud = FONT_MD.render(
            f"Budget: {budget:.2f} BDT   |   Paid: {total_paid:.2f} BDT   |   Item: {min(item_idx + 1, 5)}/5",
            True,
            ACCENT_BLUE,
        )
        screen.blit(hud, (30, 62))

        if game_state == "PLAYING":
            item = ITEMS[item_idx]
            card = pygame.Rect(60, 110, 600, 120)
            pygame.draw.rect(screen, CARD_COLOR, card, border_radius=12)

            item_lbl = FONT_LG.render(f"Current Item: {item['name']}", True, TEXT_DARK)
            screen.blit(item_lbl, (85, 130))

            price_a = discounted_price(item["A"], use_coupon)
            price_b = discounted_price(item["B"], use_coupon)
            sub_lbl = FONT_MD.render(
                f"Shop A: {price_a:.2f} BDT     vs     Shop B: {price_b:.2f} BDT",
                True,
                TEXT_DARK,
            )
            screen.blit(sub_lbl, (85, 178))

            draw_button(btn_a, f"Buy Shop A ({price_a:.2f})", ACCENT_BLUE)
            draw_button(btn_b, f"Buy Shop B ({price_b:.2f})", ACCENT_BLUE)

            if coupon_available:
                c_color = ACCENT_GREEN if use_coupon else GRAY_BTN
                c_text_col = (255, 255, 255) if use_coupon else TEXT_DARK
                c_label = "10% Coupon: ON" if use_coupon else "Apply 10% Coupon (1 Left)"
                draw_button(btn_coupon, c_label, c_color, c_text_col)
            else:
                draw_button(btn_coupon, "Coupon Already Used", GRAY_BTN, (100, 116, 139))

            msg_surf = FONT_SM.render(status_msg, True, status_color)
            screen.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, 435)))

        elif game_state == "WON":
            savings = calculate_savings(reference_total, total_paid)
            win_lbl = FONT_LG.render("SHOPPING COMPLETE!", True, ACCENT_GREEN)
            screen.blit(win_lbl, win_lbl.get_rect(center=(WIDTH // 2, 160)))

            stats = [
                f"Total Paid: {total_paid:.2f} BDT",
                f"Budget Remaining: {budget:.2f} BDT",
                f"Total Savings: {savings:.2f} BDT (vs {reference_total:.2f} BDT max)",
            ]
            for idx, line in enumerate(stats):
                s_surf = FONT_MD.render(line, True, TEXT_DARK)
                screen.blit(s_surf, s_surf.get_rect(center=(WIDTH // 2, 220 + idx * 40)))

            draw_button(btn_restart, "Play Again", ACCENT_BLUE)

        elif game_state == "LOST":
            lose_lbl = FONT_LG.render("OUT OF BUDGET!", True, ACCENT_RED)
            screen.blit(lose_lbl, lose_lbl.get_rect(center=(WIDTH // 2, 180)))

            reason = FONT_MD.render(
                f"Cannot afford {ITEMS[item_idx]['name']} with {budget:.2f} BDT left.",
                True,
                TEXT_DARK,
            )
            screen.blit(reason, reason.get_rect(center=(WIDTH // 2, 240)))
            draw_button(btn_restart, "Try Again", ACCENT_RED)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()