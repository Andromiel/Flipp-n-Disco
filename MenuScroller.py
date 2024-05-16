import pygame


scrolling = False
list = [("Level"+str(i+1)) for i in range(30)]
pygame.init()
def GenerateMenu(level_list, surface):
    text_size = 20
    width, height = surface.get_size()
    print(width, height)
    font = pygame.font.Font("freesansbold.ttf", text_size)
    menu_rect = pygame.Rect(width//4, height//4, width//2, height//2)
    scrollerbar_rect = pygame.Rect(menu_rect.right+50, menu_rect.y, 20, menu_rect.height)
    scroller_rect = pygame.Rect(scrollerbar_rect.x, scrollerbar_rect.y, scrollerbar_rect.width, scrollerbar_rect.height*3/len(level_list))
    text_rects = [pygame.Rect(menu_rect.width-35, menu_rect.top+menu_rect.height//4*(i+1), 70, 20) for i in range(len(level_list))]
    return [menu_rect, scrollerbar_rect, scroller_rect, text_rects, font]
def DisplayMenu(menu_data, surface):
    pygame.draw.rect(surface, (100, 100, 100), menu_data[0])
    pygame.draw.rect(surface, (50, 80, 80), menu_data[1])
    pygame.draw.rect(surface, (120, 120, 120), menu_data[2])
    for i in range(len(menu_data[3])):
        pygame.draw.rect(surface, (255, 0, 0), menu_data[3][i])
        surface.blit(menu_data[4].render("Level  " + str(i + 1), False, (255,255,255), (0,0,0)), menu_data[3][i])
def UpdateMenu(menu_data, surface):
    for i in range(len(menu_data[3])):
        menu_data[3][i].y = menu_data[0].top+menu_data[0].height//4*(i+1)-menu_data[2].y*(menu_data[2].height//menu_data[1].height)
        print(menu_data[1].height//menu_data[2].height)
    DisplayMenu(menu_data, surface)

screen = pygame.display.set_mode((600,800))
menu_data = GenerateMenu(list, screen)
loop = True

while loop:
    screen.fill((200,180,90))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_data[2].collidepoint(event.pos):
                scrolling = True
                offset = menu_data[2].y - pygame.mouse.get_pos()[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            scrolling = False

    if scrolling:
        if (menu_data[2].top >= menu_data[1].top) and (menu_data[2].bottom <= menu_data[1].bottom):
            menu_data[2].y = pygame.mouse.get_pos()[1] + offset
    else:
        if menu_data[2].top < menu_data[1].top:
            menu_data[2].top = menu_data[1].top
        elif menu_data[2].bottom > menu_data[1].bottom:
            menu_data[2].bottom = menu_data[1].bottom

    UpdateMenu(menu_data, screen)
    pygame.display.update()
