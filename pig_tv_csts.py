import random
from pigtv_constants import *
import pygame
from math import *

import json
with open('parameters.json') as file:               # A json file with all the parameters
    json_data = json.load(file)


pygame.init()





def wait():

    click = 0

    while not click:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                click = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                click = 1

            elif (event.type == KEYDOWN):

                click = 1




## colisions


def collide_circle_to_circle(pos1, rad1, pos2, rad2):

    dist = get_distance(pos1, pos2)

    max_dist_to_touch = (rad1 + rad2)

    if dist < max_dist_to_touch:  # distance between the two circles lesser than their combined radius

        return 1


def collide_line_to_circle(circle_pos, circ_rad, droite):
    """ checking if circle colliding line have solutions

    returns intersection pts or empty array

    circle_equation : (x-a)**2 + (y-b)**2 = r**2

    line_equation : ax + by + c = 0  """

    m, p = droite

    if m == []:  # ligne verticale

        if p == circle_pos[0]-circ_rad:

            return [p, circle_pos[1]]

        elif p == circle_pos[0]+circ_rad:

            return [p, circle_pos[1]]

        elif val_in_array(p, [circle_pos[0]-circ_rad, circle_pos[0]+circ_rad]):

            diff = (circ_rad)**2-((p-circle_pos[0])**2)

            return [[p, sqrt(diff)+circle_pos[0]], [p, -(sqrt(diff)+circle_pos[0])]]

        return []

    ca, cb = circle_pos

    a = 1+m**2

    b = -2*ca + 2*m*p - 2*cb*m

    c = -2*cb*p + cb**2 + ca**2 + p**2 - circ_rad**2

    delta = (b**2) - (4*a*c)

    if delta > 0:

        x1 = (-b-sqrt(delta))/(2*a)

        x2 = (-b+sqrt(delta))/(2*a)

        return [[x1, m*x1+p], [x2, m*x2+p]]

    elif delta == 0:

        x = -b/(2*a)

        return [[x, m*x+p]]

    return []


def collide_segment_to_circle(circ_pos, circ_rad, segment):
    """
    segment is two points

    first checking if circle colliding line have solutions, if yes, checks that point of line is on segment

    circle_equation : (x-a)**2 + (y-b)**2 = r**2

    line_equation : ax + by + c = 0  """

    line = get_droite_from_pt(segment[0], segment[1])  # equation de droite du segment en question

    points = collide_line_to_circle(circ_pos, circ_rad, line)

    if points == []:

        return  # returns false

    for x in range(len(points)-1, -1, -1):

        point = points[x]

        if not collide_point_on_line_to_segment(point, segment):

            points.remove(point)

    return points

def collide_point_to_rect(point, rect):

    return val_in_array(point[0], [rect[0], rect[0]+rect[2]]) and val_in_array(point[1], [rect[1], rect[1]+rect[3]])


def collide_point_on_line_to_segment(point, segment):
    """ returns True if a given point (which is on the segment line) is on that segment """

    return val_in_array(point[0], [segment[0][0], segment[1][0]]) and val_in_array(point[1], [segment[0][1], segment[1][1]])


def segment_in_rect(segment, rect):

    if (collide_point_to_rect(segment[0], rect) and collide_point_to_rect(segment[1], rect)):

        return True

    for colliding_pt in collide_rect_to_line(segment[0], get_droite_from_pt(segment[0], segment[1]), rect):

        if collide_point_on_line_to_segment(colliding_pt, segment):

            return True


def collide_rect_to_demi_droite(rect, start_pos, line):

    inter_points = collide_rect_to_line(start_pos, line, rect)

    for pt in inter_points:

        if pt[0] >= start_pos[0]*line[0]:

            return pt

def collide_rect_to_line(start_pos, line, rect):
    """ returns if line[m, p] and rect[x, y, width, height] are colliding ; """

    A = [rect[0], rect[1]]

    B = [rect[0]+rect[2], rect[1]]

    C = [rect[0], rect[1]+rect[3]]

    D = [rect[0]+rect[2], rect[1]+rect[3]]

    line_1 = [A, B]

    line_2 = [B, D]

    line_3 = [A, C]

    line_4 = [C, D]

    rect_sides = [line_1, line_2, line_3, line_4]

    results = []

    for rect_side in rect_sides:

        inter_point = get_inter_from_droite(get_droite_from_pt(rect_side[0], rect_side[1]), line)

        if inter_point == True:

            #print("droite et cote du rectangle confondus...")

            results.append(rect_side[0])

            results.append(rect_side[1])

        elif inter_point:

            if line[0] == []:

                inter_point = [inter_point, rect_side[0][1]]  # is ordonne du rectangle si droite est une verticale

            else:

                inter_point = [inter_point, line[0]*inter_point+line[1]]

            if val_in_array(inter_point[0], [rect_side[0][0], rect_side[1][0]]) and val_in_array(inter_point[1], [rect_side[0][1], rect_side[1][1]]) :

                results.append(inter_point)

    return results  # .sort(key=lambda x:x*get_sign(liste[0]))[0]


def collide_segment_to_segment(seg1, seg2):

    line1 = get_droite_from_pt(seg1[0], seg1[1])

    line2 = get_droite_from_pt(seg2[0], seg2[1])

    inter_point = get_inter_from_droite(line1, line2)

    if inter_point == True:  # not the problem

        return seg1[0]

    elif inter_point:

        if line1[0] == []:

            if line2[0] == []:

                return seg1[0]

            else:

                inter_point = [inter_point, line2[0]*inter_point+line2[1]]  # is ordonne du rectangle si droite est une verticale

        else:

            inter_point = [round(inter_point, 5), round(line1[0]*inter_point+line1[1], 5)]

        if (collide_point_on_line_to_segment(inter_point, seg1)) and (collide_point_on_line_to_segment(inter_point, seg2)):

            return inter_point


def collide_segment_to_segments(segment, segments):

    line = get_droite_from_pt(segment[0], segment[1])

    results = []

    for seg in segments:

        inter_point = get_inter_from_droite(get_droite_from_pt(seg[0], seg[1]), line)

        if inter_point == True:

            #print("droite et cote du rectangle confondus...")

            results.append(min(seg[0], seg[1]))

            #results.append(seg[1])

        elif inter_point:

            inter_point = [inter_point, line[0]*inter_point+line[1]]

            if val_in_array(inter_point[0], [seg[0][0], seg[1][0]]) and val_in_array(inter_point[1], [seg[0][1], seg[1][1]]):

                if val_in_array(inter_point[0], [segment[0][0], segment[1][0]]) and val_in_array(inter_point[1], [segment[0][1], segment[1][1]]):

                    results.append(inter_point)

    return results


def collide_circle_to_rect(pos, rad, rect):  # pos[x, y]
    """ rect : [x, y, width, height] ; this function detects if a circle collides a rectangle; returns 1 if collides on xline, 2 if collides on yline, 3 if a mix of the txo (arriving in corner), None else """

    # puts rectangle to normal format

    print_help = 0

    rect = format_rect(rect)

    if pos[0] < rect[0]:  # The x coordinate of the circle is lesser than the left side of the rectangle -> closest x of rect from pos[0] (x centre of circle) is rect[0]
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y to pos[1]

            dist = sqrt((rect[0]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(1, 3)

                return 2#3  # ball arriving in a corner (in that case left low corner) ; when used in some games often should not be interpreted as corner but horizontal part

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = sqrt((rect[0]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(2, 3)

                return 3  # left up corner

        else:  # closest is pos[1] : don't have to substract in y

            dist = abs(rect[0]-pos[0])

            if dist < rad:

                if print_help:

                    print(3, 1)

                return 1  # ball ariving in the retangle from the left -> should switch (*-1) the x coor of the vector

    elif pos[0] > rect[0]+rect[2]:  # x coor of circle is bigger than x coor of rect + its width
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y

            dist = sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(4, 3)

                return 2#3  when used in some games often should not be interpreted as corner but horizontal part

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(5, 3)

                return 3

        else:  # closest is pos[1] : don't have to substract in y

            dist = abs(rect[0]+rect[2]-pos[0])

            if dist < rad:

                if print_help:

                    print(6, 1)

                return 1

    else:  # pos x of circle is in rect

        if pos[1] < rect[1]:  # the ball in under the rect (same x coordinates, y coors of ball < rect's one) -> rect[1] (lowest point of rect (y without the height) is closest in y

            dist = abs(rect[1]-pos[1])

            if dist < rad:

                if print_help:

                    print(7, 2)

                return 2

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = abs(rect[1]+rect[3]-pos[1])

            if dist < rad:

                if print_help:

                    print(8, 2)

                return 2

        else:  # the ball is in rect (left_rect<x_ball<right_rect, down_rect<y_ball<up_rect)

            if min((pos[0]-rect[0])/rect[2], 1-(pos[0]-rect[0])/rect[2]) < min((pos[1]-rect[1])/rect[3], 1-(pos[1]-rect[1])/rect[3]):

                if print_help:

                    print(9, 1)

                return 1

            else:

                if print_help:

                    print(10, 2)

                return 2


def collide_rect_to_rect(rect1, rect2):
    """ Functions that checks wheter to rectangles are colliding ; rect format is [left corner x, y, width, height] """

    rect1 = format_rect(rect1)

    rect2 = format_rect(rect2)

    if ((rect1[0]<=rect2[0]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]+rect2[2]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]+rect2[3]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]+rect2[2]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]+rect2[3]<=rect1[1]+rect1[3])):

        return True


def collide_pt_on_line_to_half_line(pt, half_line):
    """ halfine is defined as half_line[seg_pt, line_pt) """

    x_diff = get_sign(half_line[0][0]-half_line[1][0])

    y_diff = get_sign(half_line[0][1]-half_line[1][1])

    pt_to_seg_end_x_diff = half_line[0][0]-pt[0]

    pt_to_seg_end_y_diff = half_line[0][1]-pt[1]

    condition_x = (not pt_to_seg_end_x_diff) or (get_sign(pt_to_seg_end_x_diff) == x_diff)  # point is on the segment end (so ok) or in the good direction (sens)

    condition_y = (not pt_to_seg_end_y_diff) or (get_sign(pt_to_seg_end_y_diff) == y_diff)

    return condition_x and condition_y


def collide_point_polygon(pt, polygon):
    """ Functions that returns either a polygon (array of points) collides a pt """

    # defining polygon sides

    sides = []

    for x in range(len(polygon)):

        last_index = (x+2)%(len(polygon)+1)

        if not last_index:  # have to add last and first of the array

            sides.append([polygon[-1], polygon[0]])

        else:

            sides.append(polygon[x:last_index])

    # definig the polygon center (average of points)
    sum_x = 0

    sum_y = 0

    for x in polygon:

        sum_x += x[0]

        sum_y += x[1]

    # will first check if polygon center is in the polygon

    polygon_center = [sum_x//len(polygon), sum_y//len(polygon)]

    #pygame.draw.circle(screen, YELLOW, polygon_center, 25)

    # looks for the longest side

    side_lengths = [get_distance(x[0], x[1]) for x in sides]

    longest_side = sides[side_lengths.index(max(side_lengths))]

    testing_pt = get_milieu_droite(longest_side[0], longest_side[1])

    center_to_test_pt = get_droite_from_pt(polygon_center, testing_pt)  # line between polygon center and middle between two summits

    collisions = 0

    for index in range(len(sides)):

        cur_side = sides[index]

        #pygame.draw.line(screen, RED, cur_side[0], cur_side[1], 3)

        #pygame.draw.line(screen, RED, polygon_center, testing_pt, 3)

        side_line = get_droite_from_pt(cur_side[0], cur_side[1])

        collision_pt = get_inter_from_droite(side_line, center_to_test_pt, full_pt=1)

        collision_pt = [round(collision_pt[0], 2), round(collision_pt[1], 2)]

        if collision_pt and collide_point_on_line_to_segment(collision_pt, cur_side):  # side colliding

            #pygame.draw.circle(screen, YELLOW, (int(collision_pt[0]), int(collision_pt[1])), 20)

            if collide_pt_on_line_to_half_line(collision_pt, [polygon_center, testing_pt]):  # now checking if point collding with half line (sommet-center]

                collisions += 1

        #pygame.display.update()

    center_in = (collisions % 2==1)*1

    #print(collisions, center_in)

    # now checks how much collisions there are between the unknown point and center (that we now if it's in or out) segment and each side of the polygon, to count the number of times it goes in or out

    center_unknown_pt_seg = [polygon_center, pt]

    center_unknown_pt_line = get_droite_from_pt(center_unknown_pt_seg[0], center_unknown_pt_seg[1])

    in_out = 0

    for index in range(len(sides)):

        cur_side = sides[index]

        side_line = get_droite_from_pt(cur_side[0], cur_side[1])

        collision_pt = get_inter_from_droite(side_line, center_unknown_pt_line, full_pt=1)

        if collision_pt:

            collision_pt = [round(collision_pt[0], 2), round(collision_pt[1], 2)]

            if collide_point_on_line_to_segment(collision_pt, cur_side) and collide_point_on_line_to_segment(collision_pt, center_unknown_pt_seg):

                in_out += 1

    return (in_out%2 == 0)


def test_polygon_collision():

    test = 2

    if test == 1:

        screen.fill(BLACK)

        polygon_pt = []

        for x in range(random.randint(3, 4)):

            polygon_pt.append([random.randint(0, screen_width), random.randint(0, screen_height)])

        unknown_pt = DotCenter(random.randint(0, screen_width), random.randint(0, screen_height))

        play = True

        while play:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

            unknown_pt.update(get_vector_to_point([unknown_pt.x, unknown_pt.y], pygame.mouse.get_pos(), 1))

            if collide_point_polygon([unknown_pt.x, unknown_pt.y], polygon_pt):

                color = RED

            else:

                color = GREEN

            screen.fill(BLACK)

            pygame.draw.polygon(screen, GREY, polygon_pt)

            pygame.draw.circle(screen, color, [int(unknown_pt.x), int(unknown_pt.y)], 5)

            pygame.display.update()

    elif test == 2:

        polygon_pt = []

        for x in range(random.randint(30, 40)):

            polygon_pt.append([random.randint(0, screen_width//2), random.randint(0, screen_height)])

        # draws polygon on screen left
        screen.fill(BLACK)

        pygame.draw.polygon(screen, GREY, polygon_pt)

        pygame.display.update()

        # draws all pixel ,on right of screen, red if collidingg polyogn, green else

        a = time.time()

        for y in range(screen_height):

            for x in range(screen_width//2):

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        return

                if collide_point_polygon([x, y], polygon_pt):

                    color = RED

                else:

                    color = GREEN

                screen.set_at((x+screen_width//2, y), color)

            pygame.display.update()

        pygame.display.update()

        print(time.time()-a)

    wait()

def collide_vect_to_line(vect, pos, line):
    """ returns the new vector when an entity with a vector has collided into a line (wall..) """

    #tail of the vect, pos is the intesection vector-line
    pos2 = sum_arrays(pos, vect, 1, -1)

    # creates a rectangle triangle
    first_perp = get_perpendiculaire_from_d(line, pos2)

    # is the intersection between the perpendicular to the line and the line, point that we need is symetric of this pt with pos
    inter_perp_droite = get_inter_from_droite(line, first_perp, full_pt=1)

    move_vect = sum_arrays(pos, inter_perp_droite, 1, -1)

    symetrical_pt = sum_arrays(pos, move_vect)

    # gets the line where the final point is lying
    n_inter_perp_droite = get_perpendiculaire_from_d(line, symetrical_pt)

    perp_to_tale_vect = sum_arrays(pos2, inter_perp_droite, 1, -1)

    final_point = sum_arrays(symetrical_pt, perp_to_tale_vect)

    final_vect = sum_arrays(final_point, pos, 1, -1)

    return final_vect


def collide_circle_to_triangle(pos_c, rad, pt1, pt2, pt3):
    """ Function that detects collisions between a circle and any triangle defined by three points. First computes in which zone the circle is : zone 1 or zone2 (hard to explain without a drawing) """
    pass


def deal_with_collisions(x, y, rad, rectangles=[], circles=[], triangles=[]):
    """ Deals with collisions for a ball(circle) ; returns 2 if collides some horizontal plain(floor, roof ..), or 1 if vertical (as a wall), None for nothing ofc """

    collisions = []

    for rect in rectangles:

        collision = collide_circle_to_rect((x, y), rad, rect)

        if collision:

            collisions.append(collision)

    return collisions


def circle_out_rect(dot, rect):
    """ checks if circle collides with line (therefore single value) ; returns 1 if colliding left, returns 2 if colliding right, returns 3 if colliding up, returns 4 if colliding down (line of the rect) """

    circle_y_array = [dot.y-dot.radius, dot.y+dot.radius]

    circle_x_array = [dot.x-dot.radius, dot.x+dot.radius]

    to_return = []

    if colliding_arrays(circle_x_array, [rect[0], rect[0]]):

        to_return.append(1)

    elif colliding_arrays(circle_x_array, [rect[0]+rect[2], rect[0]+rect[2]]):

        to_return.append(2)

    if colliding_arrays(circle_y_array, [rect[1], rect[1]]):

        to_return.append(3)

    elif colliding_arrays(circle_y_array, [rect[1]+rect[3], rect[1]+rect[3]]):

        to_return.append(4)

    return to_return






## fonts


font_30 = pygame.font.SysFont("monospace", 30, True)

font_20 = pygame.font.SysFont("monospace", 20, True)





def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30, centre=0, font=None, window=None):
    """ Permet d'afficher un texte """

    if centre == 1:

        # taille en fontsize=30 -> 18 px ; on ajuste pour que dans le cas majoritaire ca marche bien

        x -= (len(contenu)/2)*(18)*(taille/30)

    if taille == 30:

        font = font_30

    elif taille == 20:

        font = font_20

    elif (font == None):

        font = pygame.font.SysFont("monospace", taille, True)

    text = font.render(contenu, 1, color)

    if window == None:

        screen.blit(text, (x, y))

    else:

        window.blit(text, (x, y))


## Maths functions

def get_distance_eucli_rn(x, y):
    """ ok : get_distance_eucli_rn([0, 0, 0], [1, 1, 1]) = sqrt(3) """

    return sqrt(sum([(x[i]-y[i])**2 for i in range(len(x))]))


def val_in_array(val, array, is_sorted=0):
    """ tests if a given value is "in" an array """

    if not is_sorted:

        array.sort()

    if array[0] <= val <= array[1]:

        return True


def sum_arrays(array1, array2, facteur1=1, facteur2=1, max_val=0):
    """ sums same size arrays """

    if len(array1) != len(array2):

        print("Arrays of different sizes !")

        return

    n_array = []

    for x in range(len(array1)):

        if type(array1[x]) == list:

            n_array.append(sum_arrays(array1[x], array2[x], facteur1, facteur2, max_val))

        else:

            n_array.append(array1[x]*facteur1 + array2[x]*facteur2)

            if max_val:

                if n_array[-1] > max_val:

                    n_array[-1] = max_val

    return n_array



def get_trigo_sole_angle(angle):
    """ returns the angle modulo[2pi], the only angle, so that two same angles are equal"""

    return angle % (2*pi)


def polar_to_cartesian_coors(angle, radius):

    return [radius*cos(angle), radius*sin(angle)]


def cartesian_to_polar_coors(x, y):

    dist = sqrt(x**2+y**2)

    if x == 0:

        if y > 0:

            angle = pi/2

        else:

            angle = -pi/2

    else:

        angle = atan(y/x)

    return [angle, dist]


def product_sum(liste):

    sum_ = liste[0]

    for x in range(1, len(liste)):

        sum_ *= liste[x]

    return sum_


def get_sign(nbr):

    if nbr < 0:

        return -1

    return 1


def get_sign_zero(nbr):

    if nbr < 0:

        return -1

    elif nbr == 0:

        return 0

    return 1


def factoriel(x):

    if x == 1:

        return 1

    return factoriel(x-1)*x


def get_sign_with_null(nbr):

    if nbr < 0:

        return -1

    elif nbr > 0:

        return 1

    return 0


# angles stuff

def get_pos_on_circle(pi_angle, radius=1, move_list=[0, 0]):
    """ returns the pos of a point on a circle according to some angle(0 to two pi) """

    return [cos(pi_angle)*radius+move_list[0], sin(pi_angle)*radius+move_list[1]]


def get_vect_from_angle(angle, pi_angle=1, rounding=5):

    if not pi_angle:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], angle)

    if rounding:

        return get_vector_to_point([0, 0], [round(cos(angle), rounding), round(sin(angle), rounding)], 1)

    else:

        return get_vector_to_point([0, 0], [cos(angle), sin(angle)], 1)


##


def sym_to_point(pos, center):

    dist_x = center[0]-pos[0]

    n_x = center[0]+dist_x

    dist_y = center[1]-pos[1]

    n_y = center[1]+dist_y

    return [n_x, n_y]


def get_ratio(nbr1, nbr2):

    if nbr2:

        return nbr1/nbr2

    else:

        return nbr1


def get_contraire_in_array(val, array):

    ecart = array[1]-array[0]

    return array[0]+((val-array[0])-ecart)*-1


def test_get_contraire_in_array():

    print(  get_contraire_in_array(0.5, [0, 2]),
            get_contraire_in_array(1.5, [1, 2]),
            get_contraire_in_array(1.5, [0, 2]),
            get_contraire_in_array(0.5, [-1, 2]),
            get_contraire_in_array(-0.5, [-2, 0])
            )


# round


def round_between(nbr, bornes, to_go_bornes=[0, 1], round_to=2):

    return round(((to_go_bornes[1]-to_go_bornes[0])*(nbr-bornes[0]))/(bornes[1]-bornes[0]), round_to)


def round_list(to_round_list, round_to=0):

    for x in range(len(to_round_list)):

        to_round_list[x] = round(to_round_list[x], round_to)

        if round_to == 0:

            to_round_list[x] = int(to_round_list[x])

    return to_round_list


def out_screen(x, y, x_max, y_max, min_x=0, min_y=0):

    return (x<min_x) or (y<min_y) or (x>x_max) or (y>y_max)


# Array functions



def get_list_indexs(liste, element):

    indexs = []

    for x in rl(liste):

        item = liste[x]

        if item == element:

            indexs.append(x)

    return indexs


def get_list_indexs_deep(liste, element, max_depth=-1):

    indexs = []

    for x in rl(liste):

        item = liste[x]

        if item == element:

            indexs.append(x)

        elif type(item) == list and max_depth != 0:

            for res in get_list_indexs_deep(item, element, max_depth-1):

                if type(res) == int:

                   indexs.append([x, res])

                else:

                    indexs.append([x]+res)

    return indexs


def get_practical_format(frmt1, frmt2):

    if len(frmt1) > len(frmt2):

        return list(reversed(get_practical_format(frmt2, frmt1)))

    elif len(frmt1) < len(frmt2):  # array 2 might have a useless dimension

        one_indexs = get_list_indexs(frmt2, 1)

        for one_idx in one_indexs:  # trying all possibilities in exponential manner, but list sizes should be relatively small

            n_frmt2 = frmt2.copy()

            del n_frmt2[one_idx]

            n_frmts = get_practical_format(frmt1, n_frmt2)

            if n_frmts != None:

                return n_frmts

        return None

    else:

        if frmt1 == frmt2:

            return frmt1, frmt2

        else:  # can't be changed into the other format

            return None



def get_flattened_list(liste, reduc_nb=-1):

    if reduc_nb > 0:

        if not (type(liste) == list or type(liste) == tuple):

            return liste

        n_liste = []

        for x in liste:

            if (type(x) == list or type(x) == tuple):

                n_liste.extend(get_flattened_list(x, reduc_nb-1))

            else:

                n_liste.append(x)

        return n_liste

    return liste


def get_reduced_dim_list(liste):

    n_liste = []

    for x in liste:

        if type(x) == list:

            n_liste.extend(x)

        else:

            n_liste.append(x)

    return n_liste


def replace_liste(liste, old_element, new_element):

    for idx in rl(liste):

        x = liste[idx]

        if type(x) == Arr:

            x.replace(old_element, new_element)

        elif type(x) == list:

            replace_liste(x, old_element, new_element)

        elif x == old_element:

            liste[idx] = new_element


def in_deep(liste, element):

    vrai = False

    for x in liste:

        if x == element:

            return True

        elif type(x) == list:

            if in_deep(x, element):

                vrai = True

        elif isinstance(x, Arr):

            if x.in_deep(element):

                vrai = True

    return vrai


def complete_copy_list(liste):

    copie = []

    for x in liste:

        if type(x) == list:

            copie.append(complete_copy_list(x))

        else:

            copie.append(x)

    return copie


class Arr:

    def __init__(self, liste):

        self.liste = liste

        self.len = len(liste)

        self.format = Arr.get_format(self)

    def __len__(self):

        return self.len

    def __eq__(self, arr):

        if isinstance(arr, Arr):

            return self.liste == arr.liste

        elif isinstance(arr, list):

            return self.liste == arr

        else:

            return False

    def __add__(self, arr2):

        if not isinstance(arr2, Arr):

            raise TypeError("Careful ! You're trying to add an Array and sth weird ({})".format(type(arr2)))

        elif len(arr2) != self.len:

            raise ValueError("The lists don't have same length")

        elif self.format != arr2.format:

            # on regarde si on peut interpreter les formats comme etant equivalent

            n_frmts = get_practical_format(self, arr2)

            if new_arrays != None:

                n_self_format, n_arr2_frmt = n_frmts

                if self.format != n_self_format:

                    array1 = Arr.adapted_to_n_format(self)

                else:

                    array1 = self

                if arr2.format != n_arr2_frmt:

                    array2 = Arr.adapted_to_n_format(arr2)

                else:

                    array1 = arr2

                return array1 + array2  # returns the simplist format

            else:

                raise ValueError("Arrays that you're trying to add don't have same format : {} and {}".format(self.format, arr2.format))

        else:

            return Arr([self.liste[x]+arr2.liste[x] for x in range(self.len)])

    def __mul__(self, fact):

        if type(fact) == float or type(fact) == int or (isinstance(fact, Arr) and (fact.format == [1, 1] or fact.format == [1])):  # produit par un scalaire

            if isinstance(fact, Arr) and (fact.format == [1, 1] or fact.format == [1]):

                fact.flatten()

                fact = fact.liste[0]

            if len(self.format) == 1:

                return Arr([self.liste[x]*fact for x in range(self.len)])

            else:  # apllies the multiplication by fact recursively to sub arrays

                return Arr([(Arr(self.liste[x])*fact).liste for x in range(self.len)])

        elif isinstance(fact, Arr):

            if (self.format == [1, 1] or self.format == [1]):

                arr = Arr.flattened(self)

                facteur = arr.liste[0]

                return facteur*fact

            if self.format == fact.format and (self.len == 1):  # multiplication terme a terme (produit de Hadamard)

                if len(self.format) == 1:

                    return Arr([self.liste[x]*fact.liste[x] for x in range(self.format[0])])

                else:

                    return Arr([(Arr(self.liste[x])*Arr(fact.liste[x])).liste for x in range(self.format[0])])  # needs to transform the inner lists in arrays to treat recursively

            else:  # dot product (produit de matrices)

                if len(self.format) == 2:  # matrice carree

                    other_format = fact.format

                    other_list = fact.liste

                    if len(other_format) == 1:

                        other_format.append(1)

                    if other_format[1] == 1:

                        other_list = [[x] for x in other_list]

                    if other_format[0] != self.format[1]:

                        raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))

                    res_liste = [[sum([self.liste[l][k]*other_list[k][c] for k in range(self.format[1])]) for c in range(other_format[1])] for l in range(self.format[0])]

                    return Arr(res_liste)

                elif len(fact.format) == 2:  # facteur : matrice carree

                    other_format = fact.format

                    if len(self.format) == 1:  # un vecteur ligne (x1, ..., xn) est aussi une matrice (n, 1)

                        self.liste = [self.liste]

                        self.format.insert(0, 1)

                    this_list = self.liste

                    #if self.format[0] == 1:

                     #   this_list = [this_list]

                    if other_format[0] != self.format[1]:

                        raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))

                    res_liste = [[sum([this_list[l][k]*fact.liste[k][c] for k in range(self.format[1])]) for c in range(other_format[1])] for l in range(self.format[0])]

                    return Arr(res_liste)

                #elif self.format[

                else:

                    raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))
        else:

            raise TypeError("Unexpected type in Array multiplication (type {})".format(type(fact)))

    def __rmul__(self, fact):

        return Arr.__mul__(self, fact)

##    def __divmod__(self, fact):
##
##        return Arr.__mul__(self, 1/fact)

    def __sub__(self, arr2):

        return Arr.__add__(self, (arr2*(-1)))

    def __repr__(self):

        if len(self.format) == 2:

            string = "Arr ( \n["

            c = 0

            for x in self.liste:

                c += 1

                if c == 1:

                    string += "[ " + str(x) + " ]\n"

                else:

                    string += " [ " + str(x) + " ]\n"

            return string + " ) "

        else:

            return "Arr ( "+str(self.liste)+ " ) \n"

    def is_nul(self):

        for x in self.liste:

            if x != 0:

                return False

        return True

    def __getitem__(self, key):

        return self.liste[key]

    def __setitem__(self, key, value):

        self.liste[key] = value

        self.format = Arr.get_format(self)

        self.len = self.len(liste)

    def transposed(self):

        if len(self.format) == 2:

            n_liste = [[self.liste[i][j] for i in range(self.format[0])] for j in range(self.format[1])]

            return Arr(n_liste)

        elif len(self.format) == 1:

            n_liste = [[self.liste[i]] for i in range(len(self.liste))]

            return Arr(n_liste)

        else:

            print("On transpose seulement des matrices")

    def transpose(self):

        transp_arr = Arr.transposed(self)

        self.liste = transp_arr.liste

        self.format = transp_arr.format

    def copy(self):

        return Arr(self.liste.copy())

    def get_format(self):
        """ format is a list : it's len is the Array's depth, ie le nb de listes imbriquees, and each number of the list is the size of the dimension associated """

        def get_format_liste(liste):

            contains_list = 0

            contains_non_list = 0

            for x in liste:

                if type(x) == list:

                    contains_list = 1

                else:

                    contains_non_list = 1

            if contains_list == 0:

                return [len(liste)]

            elif contains_list == 1 and contains_non_list == 1:

                return [len(liste), "_"]  # invalid format

            else:

                liste_formats = []

                for ss_liste in liste:

                    liste_formats.append(get_format_liste(ss_liste))

                for format_ in liste_formats:

                    if format_ != liste_formats[0]:

                        return [len(liste), "_"]  # invalid format

                return [len(liste), liste_formats[0][0]]

        return get_format_liste(self.liste)

    def adapted_to_n_format(self):

        return n_arr

    def get_nul(format_):

        def get_nul_liste(format_):

            if len(format_) == 1:

                return [0 for x in range(format_[0])]

            else:

                return [get_nul_liste(format_[1:]) for x in range(format_[0])]

        return Arr(get_nul_liste(format_))

    def get_mat_rot2D(angle):

        return Arr([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])

    def get_polar(self):
        """ for a 2D vector (x, y) returns radius and angle """

        if self.liste[0] == 0:

            if self.liste[1] >= 0:

                angle = pi/2

            else:

                angle = -pi/2

        else:

            ratio = self.liste[1] / self.liste[0]

            angle = arctan(ratio)

        return Arr.norme_eucli(self), angle

    def norme_eucli(self):

        return get_distance_eucli_rn(self.liste, [0 for x in range(self.len)])

    def get_distance(arr1, arr2):

        if len(arr1.format) == 1:

            return get_distance_eucli_rn(arr1.liste, arr2.liste)

        elif len(arr1.format) == 2:

            return sum([get_distance_eucli_rn(arr1.liste[x], arr2.liste[x]) for x in rl(arr1.liste)])
        else:

            print("bad format, not done yet")

    def normalize(self, norme=1):

        if not Arr.is_nul(self):

            norme_actuelle = Arr.norme_eucli(self)

            facteur = norme/norme_actuelle

            self.liste = Arr.__mul__(self, facteur).liste

    def normalized(self, norme=1):

        arr = Arr.copy(self)

        arr.normalize(norme)

        return arr

    def get_random(norme=1, dim=2):

        liste = [random.random()-0.5 for x in range(dim)]

        arr = Arr(liste)

        arr.normalize(norme)

        return arr

    def apply_fun(self, function):

        self.liste = [function(x) for x in self.liste]

    def with_fun_applied(self, function):

        return [function(x) for x in self.liste]

    def p_s(arr1, arr2):
        """ produit scalaire euclidien de deux vecteurs de R^n """

        if len(arr1) == len(arr2):

            return sum([arr1[x]*arr2[x] for x in range(len(arr1))])

        else:

            raise Exception

    def get_orth(self):
        """ retourne la droite orthogonale de norme 1 pour un vecteur 2D , (x' y') tq [(x y) scal (x' y') = 0]"""

        if self.format == [2]:

            x, y = self.liste

            if x == 0:

                return Arr([1, 0])

            else:

                y_prim = x**2/(x**2+y**2)

                x_prim = -y_prim*y/x

                return Arr([x_prim, y_prim])

        else:

            raise ValueError("Expected 2D vector, got format : {}".format(self.format))

    def draw(self):

        size = 100

        pygame.draw.line(screen, BLACK, [size, size], [size+self.liste[0]*10, size+self.liste[1]*10])

    def get_indexs(self, element):

        return get_list_indexs(self.liste, element)

    def get_indexs_deep(self, element, max_depth=-1):
        """ get all multidimensional indexes of an element in a multidimensional list ; if max_depth is not -1, the list elements that are more than max_depth dimensional are ignored """

        return get_list_indexs_deep(self.liste, element, max_depth)

    def in_deep(self, element):

        return in_deep(liste, element)

    def flatten(self):

        self.liste = get_flattened_list(self.liste)

    def flattened(self):

        arr = Arr.copy(self)

        arr.flatten()

        return arr

    def replace(self, old_element, new_element):

        replace_liste(self.liste, old_element, new_element)

    def complete_copy(self):

        return Arr(complete_copy_list(self.liste))




def get_random_point_in_screen():

    return [random.randint(0, screen_width), random.randint(0, screen_height)]




def set_color(col):

    rand = 0

    if rand:

        return get_random_color()

    return list(col)

screen_center = [screen_width//2, screen_height//2]


WHITE = set_color((255, 255, 255))

BLACK = set_color((0, 0, 0))

RED = set_color((255, 0, 0))

LIGHT_RED = set_color((200, 0, 80))

DARK_RED = set_color((150, 0, 0))

YELLOW = set_color((255, 255, 0))

BEIGE = set_color((210, 210, 150))

GREEN = set_color((20, 255, 25))

DARK_GREEN = set_color((20, 60, 25))

BROWN = set_color((60, 30, 20))

BROWN2 = set_color([79, 51, 26])

DARK_BROWN = set_color((20, 0, 10))

GREY = set_color((150, 150, 150))

LIGHT_GREY = set_color((200, 200, 200))

DARK_GREY = set_color((60, 60, 60))

BLUE = set_color((0, 0, 150))

LIGHT_BLUE = set_color((0, 0, 255))

REAL_LIGHT_BLUE = set_color((200, 200, 255))

DARK_BLUE = set_color([0, 0, 60])

PURPLE = set_color([200, 10, 190])

ORANGE = set_color([255, 160, 0])

DARK_ORANGE = set_color([160, 40, 40])

PINK = set_color([255, 80, 80])

PINK2 = set_color([255, 20, 147])

##greys = []
##
##for x in range(25):
##
##    greys.append([x*10 for x in range(3)])


colors = [WHITE ,BLACK,RED ,LIGHT_RED ,DARK_RED ,YELLOW ,GREEN,DARK_GREEN,BROWN,BROWN2,DARK_BROWN,BLUE,LIGHT_BLUE ,REAL_LIGHT_BLUE ,DARK_BLUE ,PURPLE ,ORANGE, DARK_ORANGE, PINK, PINK2]
