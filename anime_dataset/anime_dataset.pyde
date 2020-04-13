# Colours used
BGCLR = '#FFFFFF'
BLACK = 0
WHITE = 255

# global variables
movie = False
tv = False

def setup():
    fullScreen()

def pie_chart(data_dict, x, y, clr1, clr2, s1, s2, bias):
    deg = radians(0)
    i = 0
    inc = len(data_dict.keys())
    for _key, _val in data_dict.items():
        if _val > bias:
            fill(clr1)
            arc(x, y, _val*s1, _val*s1, deg + i*(radians(360)/inc), deg + (i+1)*(radians(360)/inc), PIE)
        else:
            fill(clr2)
            arc(x, y, _val*s2, _val*s2, deg + i*(radians(360)/inc), deg + (i+1)*(radians(360)/inc), PIE)
        i+=1
        
def bar_graph(data_dict, x, y, w, max_val):
    fill(WHITE)
    i = 0
    l = len(data_dict.keys())
    for _key, _val in data_dict.items():
        if _val > max_val:
            rect(x+(w/l)*i, y, w/l, -max_val+50)
            rect(x+(w/l)*i, y-max_val+40, w/l, -50)
        else:
            rect(x+(w/l)*i, y, w/l, -_val)
        i+=1

def draw_check_box(val, x, y, clr):
    s = 25
    stroke(BLACK)
    strokeWeight(2)
    if not val:
        noFill()
    else:
        fill(clr)
    square(x, y, s)

def check_box(x, y, val):
    s = 25
    if mousePressed:
        if mouseX > x-s and mouseX < x+s and mouseY > y-s and mouseY < y+s:
            val = not val
    draw_check_box(val, x, y, BLACK)
    return val

def back_button(val):
    textSize(25)
    fill(BLACK)
    text('<- Back', 1750+32, 50+22)
    return check_box(1750, 50, val)

def selection_screen():
    global movie, tv
    movie = check_box(600, 400, movie)
    tv = check_box(600, 500, tv)

    textSize(25)
    fill(BLACK)
    text('Anime Movie', 600+32, 400+22)
    text('Anime TV Shows', 600+32, 500+22)
    

def movie_screen():
    global movie
    movie_data = loadTable("data/movie_type_anime.csv", "header")
    
    genre_dict = {}
    for row in movie_data.rows():

        name = row.getString('name')
        genre_list = row.getString('genre').split(', ')
        #eps = row.getInt('episodes')
        #type = row.getString('type')
        rating = row.getFloat('rating')
        mem = row.getInt('members')
        
        for genre in genre_list:
            if genre not in genre_dict:
                genre_dict[genre] = 0
            genre_dict[genre] += 1

    others = 0
    k =0
    for genre, count in genre_dict.items():
        if count <= 30:
            others += count
            k +=1
            del genre_dict[genre]
    
    genre_dict['Others'] = others
    
    pie_chart(genre_dict, 400, 400, '#008080', '#00ffff', 1, 4, 200)

    movie = back_button(movie)


def tv_screen():
    global tv
    tv_data = loadTable("data/tv_type_anime.csv", "header")
    
    genre_dict = {}
    for row in tv_data.rows():

        name = row.getString('name')
        genre_list = row.getString('genre').split(', ')
        eps = row.getInt('episodes')
        #type = row.getString('type')
        rating = row.getFloat('rating')
        mem = row.getInt('members')
        
        for genre in genre_list:
            if genre not in genre_dict:
                genre_dict[genre] = 0
            genre_dict[genre] += 1

    others = 0
    k =0
    for genre, count in genre_dict.items():
        if count <= 50:
            others += count
            k +=1
            del genre_dict[genre]
    
    genre_dict['Others'] = others
    
    #pie_chart(genre_dict, 400, 400, '#008080', '#00ff00', 0.5, 2, 250)
    
    bar_graph(genre_dict, 200, 1000, 500, 600)
    
    tv = back_button(tv)

def draw():
    background(BGCLR)
    
    if not(movie or tv):
        selection_screen()

    if movie:
        movie_screen()
    if tv:
        tv_screen()
