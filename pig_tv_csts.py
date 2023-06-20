import random
from pigtv_constants import *
import pygame





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
