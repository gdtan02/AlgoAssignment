from PIL import Image, ImageDraw
from collections import deque as queue

# Read the FloorPlan.txt file
def create_floor_plan():
    file = open("FloorPlan.txt", "r")

    # Declare the array to store the floor plan layout 
    global ground_floor
    global first_floor
    temp_floor = ''   # For floor tracking purpose
    global ground_images
    global first_images

    # Read the file and convert it into numerical value
    for line in file.readlines():
        if (line[0] == 'G'):
            temp_floor = 'G'
            continue
        elif (line[0] == 'F'):
            temp_floor = 'F'
            continue
        
        row = []
        
        for c in line:
            if (c.isspace() and c != "\n"):
                row.append(1)    # Walkable path
            elif (c != "\n"):
                row.append(0)    # Boundaries
                
        if temp_floor == 'G':
            ground_floor.append(row)
        else:
            first_floor.append(row)
            
    file.close()

    # Display the floor layout in numerical value
    print("Ground Floor: ")
    for r in ground_floor:
        print(r)
        
    print("\nFirst Floor:")
    for r in first_floor:
        print(r)

        

def isValid(visited, floor, row, col):
    global floor_rows
    global floor_cols
    
    # Check boundaries
    if (row < 0 or row >= floor_rows or col < 0 or col >= floor_cols):
        return False
    
    # Check walkable path
    if (floor[row][col] == 0):
        return False
    
    # Check visited cell
    if (visited[row][col]):
        return False
    
    return True

def DFS(current_floor, start, end):
    global floor_rows
    global floor_cols
    global ground_floor
    global first_floor
    global d_row
    global d_col
    
    if(current_floor == 'G'):
        floor = ground_floor
    else:
        floor = first_floor
        
    visited = [[not floor[i][j] for j in range(floor_cols)] for i in range(floor_rows)]
    movement = [[0 for j in range(floor_cols)] for i in range(floor_rows)]
    step = 1
    
    stack = []
    stack.append([start[0], start[1]])
    
    while(len(stack) > 0):
        current_cell = stack[len(stack)-1]
        stack.remove(stack[len(stack)-1])
        
        current_row = current_cell[0]
        current_col = current_cell[1]
        
        if(not isValid(visited, floor, current_row, current_col)):
            continue
        
        visited[current_row][current_col] = True
        movement[current_row][current_col] = step
        path.append([current_row, current_col])
        draw_matrix(current_floor, movement, start, end)
        step += 1
        
        for i in range(4):
            adjx = current_row + d_row[i]
            adjy = current_col + d_col[i]
            stack.append([adjx, adjy])

def BFS(current_floor, start, end):
    global floor_rows
    global floor_cols
    global ground_floor
    global first_floor
    global d_row
    global d_col
    
    if(current_floor == 'G'):
        floor = ground_floor
    else:
        floor = first_floor
    
    visited = [[not floor[i][j] for j in range(floor_cols)] for i in range(floor_rows)]
    movement = [[0 for j in range(floor_cols)] for i in range(floor_rows)]
    step = 1
    
    q = queue()
    q.append((start[0], start[1]))
    visited[start[0]][start[1]] = True
    movement[start[0]][start[1]] = step
    draw_matrix(current_floor, movement, start, end)

    
    while(len(q) > 0):
        current_cell = q.popleft()
        row = current_cell[0]
        col = current_cell[1]

        
        for i in range(4):
            adjx = row + d_row[i]
            adjy = col + d_col[i]
            if (isValid(visited, floor, adjx, adjy)):
                q.append((adjx, adjy))
                step += 1
                visited[adjx][adjy] = True
                movement[adjx][adjy] = step
                draw_matrix(current_floor, movement, start, end)
                

def draw_matrix(current_floor, movement, start, end):
    global floor_rows
    global floor_cols
    global ground_floor
    global first_floor
    
    if(current_floor == 'G'):
        floor = ground_floor
    else:
        floor = first_floor

    layout = Image.new('RGB', (zoom * floor_cols , zoom * floor_rows), (255, 255, 255))
    draw = ImageDraw.Draw(layout)
    
    for i in range(floor_rows):
        for j in range(floor_cols):
            color = (255, 255, 255)
            r = 0
            if floor[i][j] == 0:
                color = (0, 0, 0)
            if (start[0] == i and start[1] == j):   # Starting point
                color = (0, 255, 0)
                r = borders
            if (end[0] == i and end[1] == j):   # Ending point
                color = (0, 0, 255)
                r = borders
            draw.rectangle((j * zoom+r, i * zoom+r, j*zoom+zoom-r-1, i * zoom+zoom-r-1), fill = color)
            
            if(movement[i][j] > 0):
                r = borders
                draw.ellipse((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=(255,0,0))
            
            
            
    # for u in range(len(path)-1):
    #     y = path[u][1] * zoom + int(zoom/2)
    #     x = path[u][0] * zoom + int(zoom/2)
    #     y1 = path[u+1][1] * zoom + int(zoom/2)
    #     x1 = path[u+1][0] * zoom + int(zoom/2)
    #     draw.line((x,y,x1,y1), fill=(255,0,0), width=5)
        
    draw.rectangle((0,0,zoom*floor_cols, zoom*floor_rows), outline = (0, 255, 0), width=2)
    if(current_floor == 'G'):
        ground_images.append(layout)
    else:
        first_images.append(layout)


ground_floor = []
first_floor = []
ground_images = []
first_images = []

readFile()

zoom = 20
borders = 6
floor_rows = len(ground_floor)
floor_cols = len(ground_floor[0])
d_row = [-1, 0, 1, 0]
d_col = [0, 1, 0, -1]


# Starting point and ending point
ground_start = [11,15]
ground_end = [1,1]
first_start = [1,1]
first_end = [13, 19]
path = []

BFS('G', ground_start, ground_end)
BFS('F', first_start, first_end)

# draw_matrix(ground_floor, start, end, path)
ground_images[0].save('ground_bfs.gif', save_all=True, append_images=ground_images[1:], optimize=False, duration=1, loop=0) 
first_images[0].save('first_bfs.gif', save_all=True, append_images=first_images[1:], optimize=False, duration=1, loop=0)

ground_images=[]
first_images=[]

DFS('G', ground_start, ground_end)
DFS('F', first_start, first_end)

ground_images[0].save('ground_dfs.gif', save_all=True, append_images=ground_images[1:], optimize=False, duration=1, loop=0) 
first_images[0].save('first_dfs.gif', save_all=True, append_images=first_images[1:], optimize=False, duration=1, loop=0)
