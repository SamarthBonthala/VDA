def draw_via(x, y):

    sarah.penup()
    sarah.goto(x + 0.05, y + 0.05)
    #sarah.pencolor("black")
    sarah.pendown()
    sarah.begin_fill()
    sarah.forward(0.3)
    sarah.left(90)
    sarah.forward(0.3)
    sarah.left(90)
    sarah.forward(0.3)
    sarah.left(90)
    sarah.forward(0.3)
    sarah.left(90)
    sarah.forward(0.3)
    sarah.fillcolor("black")
    sarah.end_fill()
    sarah.penup()

def draw_route(route_path, source, target, route_type, layer):

    # Initial route in layer1
    # print("Source: ", source)
    # print "Source xcoord: ", (source[0]+0.)
    # print "Source ycoord: ", (source[1] + 0.25)
    if layer == 1:
    	sarah.pencolor("red")
    elif layer == 2:
    	sarah.pencolor("blue")

    if route_type == 0:
        sarah.goto(source[0], source[1] + 0.25)
        #sarah.pencolor("red")
        sarah.pendown()
        sarah.forward(0.75)
        sarah.penup()

        route_path.reverse()  # So that source is first and destination at the end
        for node in range(2, len(route_path)):
            delta_x = route_path[node][0]-route_path[node-1][0]
            delta_y = route_path[node][1]-route_path[node-1][1]

            if delta_x == 0 and delta_y == 0.5: # Path moved up
                sarah.goto(route_path[node-1][0] + 0.25, route_path[node-1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.left(90)
                sarah.forward(0.5)
                sarah.penup()
                sarah.right(90)
            if delta_x == 0 and delta_y == -0.5:  # Path moved down
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.right(90)
                sarah.forward(0.5)
                sarah.penup()
                sarah.left(90)
            if delta_x == 0.5 and delta_y == 0:  # Path moved right
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.forward(0.5)
                sarah.penup()
            if delta_x == -0.5 and delta_y == 0:  # Path moved left
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.left(180)
                sarah.forward(0.5)
                sarah.penup()
                sarah.right(180)
            if delta_x == 0 and delta_y == 0:  # Path moved left
                draw_via(route_path[node - 1][0], route_path[node - 1][1])

        sarah.goto(target[0] + 0.25, target[1] + 0.25)
        sarah.pencolor("red")
        sarah.pendown()
        sarah.forward(0.25)
        sarah.penup()
    else:
        route_path.reverse()  # So that source is first and destination at the end
        for node in range(1, len(route_path)):
            delta_x = route_path[node][0] - route_path[node - 1][0]
            delta_y = route_path[node][1] - route_path[node - 1][1]

            if delta_x == 0 and delta_y == 0.5:  # Path moved up
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.left(90)
                sarah.forward(0.5)
                sarah.penup()
                sarah.right(90)
            if delta_x == 0 and delta_y == -0.5:  # Path moved down
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.right(90)
                sarah.forward(0.5)
                sarah.penup()
                sarah.left(90)
            if delta_x == 0.5 and delta_y == 0:  # Path moved right
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                #sarah.pencolor("red")
                sarah.pendown()
                sarah.forward(0.5)
                sarah.penup()
            if delta_x == -0.5 and delta_y == 0:  # Path moved left
                sarah.goto(route_path[node - 1][0] + 0.25, route_path[node - 1][1] + 0.25)
                sarah.pencolor("red")
                sarah.pendown()
                sarah.left(180)
                sarah.forward(0.5)
                sarah.penup()
                sarah.right(180)

        sarah.goto(target[0], target[1] + 0.25)
        sarah.pencolor("red")
        sarah.pendown()
        sarah.forward(0.25)
        sarah.penup()

#paths = [1,2,3,5,3,6,7,12,8,0,9,10,11,12,17,14,15,18]
paths = [[1,1],[2,2],[2,2],[3,3],[4,4],[5,5],[5,5],[6,6]]

def splitting_path(paths):
    i = 0
    temp = []
    split_paths = []

    for i in range(len(paths)-1):
        print (i)
        if paths[i+1] != paths[i]:
            temp.append(paths[i])
        else:
            split_paths.append(temp)
            temp = []

    if temp != []:
        temp.append(paths[len(paths)-1])
        split_paths.append(temp)
        temp =[]

    if paths[len(paths)-1] == paths[len(paths)-2]:
        temp = split_paths[-1] 
        temp.append(paths[len(paths)-1])

    return split_paths
x = splitting_path(paths)
print (x)
print (len(x))