import pygame

scrolling = False
list = [("Level" + str(i + 1)) for i in range(30)]
pygame.init()



text_size = 20
def GenerateMenu(level_list, surface):
    width, height = surface.get_size()
    print(width, height)
    font = pygame.font.Font("freesansbold.ttf", text_size)
    menu_rect = pygame.Rect(width / 4, height / 4, width / 2, height / 2)
    scrollerbar_rect = pygame.Rect(menu_rect.right + 50, menu_rect.y, 20, menu_rect.height)
    scroller_rect = pygame.Rect(scrollerbar_rect.x, scrollerbar_rect.y, scrollerbar_rect.width,
                                scrollerbar_rect.height * 3 / len(level_list))
    text_surface = pygame.Surface((menu_rect.size[0], len(level_list) * text_size * 4))

    text_surfaces = [pygame.Surface((menu_rect.size[0], text_size * 4)) for i in range(len(level_list))]
    text_rects = [text_surfaces[i].get_rect() for i in range(len(level_list))]

    for i in range(len(level_list)):
        text_rects[i].center = (menu_rect.center[0], i * text_size * 4)
        text_surfaces[i].blit(font.render("Level" + str(i), True, (255, 255, 255), (0, 0, 0)),
                              (text_surfaces[i].get_width()/2, text_surfaces[i].get_height()/2))

    for i in range(len(level_list)):
        text_surface.blit(font.render("Level" + str(i), True, (255, 255, 255), (0, 0, 0)),
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
    percentage = (scroller_rect.top - scrollerbar_rect.top) / (scrollerbar_rect.height - scroller_rect.height)
    for i in range(len(text_surfaces)):
        text_rects[i].center = (surface.get_width() / 2, menu_rect.top +text_rects[i].height/2+ i * 4 * text_size - (text_rects[i].height * len(text_rects) - menu_rect.height) * percentage)

    DisplayMenu(menu_data, surface)


screen = pygame.display.set_mode((600, 800))
menu_data = GenerateMenu(list, screen)
menu_rect, scrollerbar_rect, scroller_rect, text_surfaces, text_rects, font = menu_data
loop = True

selected_level = [False, None]
while loop:
    selected_level[0] = False
    screen.fill((200, 180, 90))
    mouse_scroll = (0, 0)
    events = pygame.event.get()
    for i in range(len(events)):
        event = events[i]
        if event.type == pygame.MOUSEWHEEL:
            mouse_scroll = (event.x, event.y)
    for event in events:
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_scroll==(0, 0):
            if scrollerbar_rect.collidepoint(event.pos):
                scrolling = True
            for i in range(len(text_rects)):
                if selected_level[0] == False:
                    if text_rects[i].collidepoint(event.pos):
                        selected_level[0] = True
                        selected_level[1] = text_rects[i]
        elif event.type == pygame.MOUSEBUTTONUP:
            scrolling = False

    scroller_rect.center = (scroller_rect.center[0], scroller_rect.center[1] - mouse_scroll[1]*4)
    if scrolling:
        scroller_rect.center = (scroller_rect.center[0], pygame.mouse.get_pos()[1])
    if (scroller_rect.top < scrollerbar_rect.top):
        scroller_rect.center = (scroller_rect.center[0], scrollerbar_rect.top + (scroller_rect.height / 2))
    if (scroller_rect.bottom > scrollerbar_rect.bottom):
        scroller_rect.center = (scroller_rect.center[0], scrollerbar_rect.bottom - (scroller_rect.height / 2))

    else:
        if scroller_rect.top < scrollerbar_rect.top:
            scroller_rect.top = scrollerbar_rect.top
        elif scroller_rect.bottom > scrollerbar_rect.bottom:
            scroller_rect.bottom = scrollerbar_rect.bottom

    UpdateMenu(menu_data, screen)

    if selected_level[1] != None:
        pygame.draw.rect(screen, (0, 255, 0), selected_level[1], 3)

    pygame.display.update()
