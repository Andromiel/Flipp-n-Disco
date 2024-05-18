
import pygame

scrolling = False
list = [("Level" + str(i + 1)) for i in range(10)]
pygame.init()
text_size = 20
def GenerateMenu(level_list, surface):
    width, height = surface.get_size()
    print(width, height)
    font = pygame.font.Font("freesansbold.ttf", 20)
    menu_rect = pygame.Rect(width / 4, height / 4, width / 2, height / 2)
    scrollerbar_rect = pygame.Rect(menu_rect.right + 50, menu_rect.y, 20, menu_rect.height)

    scroller_rect = pygame.Rect(scrollerbar_rect.x, scrollerbar_rect.y, scrollerbar_rect.width,
                                scrollerbar_rect.height * (menu_rect.height / (len(level_list) * 4 * text_size)))

    if scroller_rect.height > scrollerbar_rect.height:
        scroller_rect.height = scrollerbar_rect.height

    text_surface = pygame.Surface((menu_rect.size[0], len(level_list) * text_size * 4))

    text_surfaces = [pygame.Surface((menu_rect.size[0], text_size * 4)) for i in range(len(level_list))]
    text_rects = [text_surfaces[i].get_rect() for i in range(len(level_list))]

    for i in range(len(level_list)):
        text_rects[i].center = (menu_rect.center[0], i * text_size * 4)
        text_surfaces[i].blit(font.render(level_list[i], True, (255, 255, 255), (0, 0, 0)),
                              (text_surfaces[i].get_width()/2, text_surfaces[i].get_height()/2))

    for i in range(len(level_list)):
        text_surface.blit(font.render(level_list[i], True, (255, 255, 255), (0, 0, 0)),
                          (text_surface.get_size()[0] / 2 / 3, i * text_size * 4))
    text_rect = text_surface.get_rect()
    text_rect.center = (width / 2, height / 2)
    return [menu_rect, scrollerbar_rect, scroller_rect, text_surfaces, text_rects, font]


def DisplayMenu(menu_data, surface):
    menu_rect, scrollerbar_rect, scroller_rect, text_surfaces, text_rects, font = menu_data
    pygame.draw.rect(surface, (100, 100, 100), menu_rect)
    for i in range(len(text_surfaces)):
        surface.blit(text_surfaces[i], text_rects[i])
    #surface.blit(text_surface, text_rect)
    pygame.draw.rect(surface, (50, 80, 80), scrollerbar_rect)
    pygame.draw.rect(surface, (120, 120, 120), scroller_rect)

def UpdateMenu(menu_data, surface):
    menu_rect, scrollerbar_rect, scroller_rect, text_surfaces, text_rects, font = menu_data
    if scrollerbar_rect.height - scroller_rect.height == 0:
        percentage = 0
    else:
        percentage = (scroller_rect.top - scrollerbar_rect.top) / (scrollerbar_rect.height - scroller_rect.height)
    for i in range(len(text_surfaces)):
        text_rects[i].center = (surface.get_width() / 2, menu_rect.top +text_rects[i].height/2+ i * 4 * text_size - (text_rects[i].height * len(text_rects) - menu_rect.height) * percentage)

    DisplayMenu(menu_data, surface)
