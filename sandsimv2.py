import pygame
import numpy
import sys
import random
from numba import njit

@njit
def movement(grid):
    for y in range(height-2,-1,-1):

        for x in range(width):
            current=grid[y,x]
            #sand
            if current==SAND:
                
                    
                if y!=height_limit:
                    val=random.randint(1,2)
                    if val==1:
                        if grid[y+1,x]==EMPTY:
                            grid[y+1,x]=SAND
                            grid[y,x]=EMPTY

                    
                        elif grid[y+1,x+1]==EMPTY:
                            if y!=height_limit and x!=0 and x!=height_limit:  
                                grid[y+1,x+1]=SAND
                                grid[y,x]=EMPTY
                            

                        elif grid[y+1,x-1]==EMPTY:
                            if y!=height_limit and x!=0 and x!=height_limit:  
                                grid[y+1,x-1]=SAND
                                grid[y,x]=EMPTY
                    else:
                        if grid[y+1,x]==EMPTY:
                            grid[y+1,x]=SAND
                            grid[y,x]=EMPTY

                        elif grid[y+1,x-1]==EMPTY:
                                if y!=height_limit and x!=0 and x!=height_limit:  
                                    grid[y+1,x-1]=SAND
                                    grid[y,x]=EMPTY
                                
                        elif grid[y+1,x+1]==EMPTY:
                            if y!=height_limit and x!=0 and x!=height_limit:  
                                grid[y+1,x+1]=SAND
                                grid[y,x]=EMPTY   
                
            #bomb
            elif current==BOMB:
                try:
                    if grid[y+1,x]==WALL:
                        grid[y,x]=EMPTY

                    if grid[y+1,x]==EMPTY:
                        grid[y,x]=EMPTY
                        grid[y+1,x]=BOMB


                    if grid[y+1,x]==SAND:
                        grid[y,x]=EMPTY
                        grid[y+1,x]=EMPTY
                        if grid[y+1,x+1]==SAND: grid[y+1,x+1]=EMPTY
                        if grid[y+1,x-1]==SAND:grid[y+1,x-1]=EMPTY
                        if grid[y+2,x]==SAND:grid[y+2,x]=EMPTY
                        if grid[y+2,x+1]==SAND:grid[y+2,x+1]=EMPTY
                        if grid[y+2,x-1]==SAND:grid[y+2,x-1]=EMPTY

                    
                except:
                    pass

            #wall
            elif current==WALL:
                if grid[y+1,x]==EMPTY:
                    grid[y,x]=EMPTY
                    grid[y+1,x]=WALL

def input_check(size):
    if pygame.mouse.get_pressed()[0]:
        mouse_grid_pos_calculate(SAND,size)

    #Bomb spawn
    keys=pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        mouse_grid_pos_calculate(BOMB,size)
    
    #Wall spawn
    if keys[pygame.K_w]:
        mouse_grid_pos_calculate(WALL,size)

def mouse_grid_pos_calculate(pixel_type,size):
    mx,my=pygame.mouse.get_pos()

    x=mx//pixel_size
    y=my//pixel_size
    
    if x>=0 and x<=width-1 and y>=0 and y<=height-1:
        if size==1:
            if grid[y,x]==EMPTY: grid[y,x]=pixel_type

        elif size==2:
            if grid[y,x]==EMPTY: grid[y,x]=pixel_type
            if grid[y,x-1]==EMPTY: grid[y,x-1]=pixel_type
            if grid[y+1,x]==EMPTY: grid[y+1,x]=pixel_type
            if grid[y+1,x-1]==EMPTY: grid[y+1,x-1]=pixel_type

screen_width=350
screen_height=350
pixel_size=1
fps=300
size=1

EMPTY=0
SAND=1
BOMB=2
WALL=3

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("sand")
clock = pygame.time.Clock()

background=pygame.Surface((screen_width,screen_height))
background.fill('black')

running=True

grid_dimension=int(screen_width/pixel_size)

grid=numpy.zeros((grid_dimension,grid_dimension),dtype=numpy.uint8)
pixels=numpy.zeros((grid_dimension,grid_dimension,3),dtype=numpy.uint8)

height,width = grid.shape

print(grid.shape)
height_limit=height-1


while running:
    pixels.fill(0)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type== pygame.KEYDOWN:
            
            if event.key==pygame.K_e:
                size=2
                

    input_check(size)
    
    movement(grid)

    #Draw
    pixels[grid.T==SAND]=[255,255,0]
    pixels[grid.T==BOMB]=[255,0,0]
    pixels[grid.T==WALL]=[90,90,90]
    
    
    for x in range(width-1):
        if grid[height_limit,x]==BOMB:
            grid[height_limit,x]=EMPTY

    
    surface=pygame.surfarray.make_surface(pixels)
    surface = pygame.transform.scale(surface,(screen_width,screen_height))

    screen.blit(surface,(0,0))
    
    pygame.display.update()
    clock.tick(fps)

  

         