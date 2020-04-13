# Colours used
BGCLR = '#FFFFFF'
BLACK = 0
WHITE = 255

CLR_LIST = ['#C0392B', '#E74C3C', '#9B59B6', '#8E44AD', '#2980B9', '#3498DB', '#1ABC9C',
            '#16A085', '#27AE60', '#2ECC71', '#F1C40F', '#F39C12', '#E67E22', '#D35400',
            '#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D', '#34495E', '#2C3E50', '#FF0000',
            '#800000', '#FFFF00', '#808000', '#00FF00', '#008000', '#00FFFF', '#008080',
            '#0000FF', '#000080', '#FF00FF', '#800080', '#DAF7A6',
            ## repeated
            '#FFFFFF', '#E67E22', '#D35400', '#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D', '#34495E', '#2C3E50']

# global variables
movie = False
tv = False

# chart variables
pie = True
bar = False
comp = False
comp_list = set()

def setup():
    fullScreen()

def genre_check_box(x, y, genre_dict):
    global comp_list
    i = 0
    j = 0
    s = 25
    for _key, _val in genre_dict.items():
        fill(CLR_LIST[i])
        x1 = x+(200*j)
        y1 = y+(25*(i+1)) - (275*j)
        square(x1, y1, 25)
        if mousePressed:
            if mouseX > x1 and mouseX < x1+s and mouseY > y1 and mouseY < y1+s:
                if (_key, CLR_LIST[i]) in comp_list:
                    comp_list.remove((_key, CLR_LIST[i]))
                else:
                    comp_list.add((_key, CLR_LIST[i]))

        fill(BLACK)
        text(_key, x+(200*j)+30, y+(25*(i+1)) - (275*j)+25)
        fill(WHITE)
        i+=1
        j = int(i/11)

def pie_chart_legand(x, y, legand_dict):
    i = 0
    j = 0
    for _key, _val in legand_dict.items():
        fill(CLR_LIST[i])
        square(x+(200*j), y+(25*(i+1)) - (275*j), 25)
        fill(BLACK)
        text(_key, x+(200*j)+30, y+(25*(i+1)) - (275*j)+25)
        #text(_val, x+(200*j)+30, y+(25*(i+1)) - (275*j)+25)
        fill(WHITE)
        i+=1
        j = int(i/11)

def pie_chart(data_dict, x, y, s1, s2, bias=200, clr_lst=None):
    deg = radians(0)
    i = 0
    inc = len(data_dict.keys())
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        if _val > bias:
            arc(x, y, int(_val*s1), int(_val*s1), deg + i*(radians(360)/(inc)), deg + (i+1)*(radians(360)/(inc)), PIE)
        else:
            arc(x, y, int(_val*s2), int(_val*s2), deg + i*(radians(360)/(inc)), deg + (i+1)*(radians(360)/(inc)), PIE)
        i+=1

def pie_chart_percent(data_dict, x, y, s1, clr_lst=None):
    deg = radians(0)
    i = 0
    inc = len(data_dict.keys())
    if clr_lst is None:
        clr_lst = CLR_LIST
    
    tot_val = 0
    for _key, _val in data_dict.items():
        tot_val += _val
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        arc(x, y, s1, s1, deg, deg + (_val/tot_val)*radians(360), PIE)
        deg += (_val/tot_val)*radians(360)
        i+=1

def hover_over_legand(x1, y1, x2, y2, legand):
    if mouseX > x1 and mouseX < x2 and mouseY > y1 and mouseY < y2:
        fill(BLACK)
        text(legand[0], 1010, 970)
        text(legand[1], 1000, 1000)
        fill(WHITE)
        
def bar_graph(data_dict, x, y, w, max_val, s, legand):
    fill(WHITE)
    i = 0
    l = len(data_dict.keys())
    for _key, _val in data_dict.items():
        fill(CLR_LIST[i])
        if _val > max_val:
            rect(x+(w/l)*i, y, w/l, -max_val+50)
            rect(x+(w/l)*i, y-max_val+40, w/l, -50)
            points[_key] = [x+(w/l)*i-w/l, y-_val*s, x+(w/l)*i, y]
        else:
            rect(x+(w/l)*i, y, w/l, -_val*s)
            hover_over_legand(x+(w/l)*i, y-_val*s, x+(w/l)*i+w/l, y, [_key, legand[_key][1]])
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
    global movie, pie, bar
    movie_data = loadTable("data/movie_type_anime.csv", "header")
    
    genre_dict = {}
    for row in movie_data.rows():

        name = row.getString('name')
        genre_list = row.getString('genre').split(', ')
        eps = row.getInt('episodes')
        #type = row.getString('type')
        rating = row.getFloat('rating')
        mem = row.getInt('members')
        
        for genre in genre_list:
            if genre not in genre_dict:
                genre_dict[genre] = [0, 0.0]
            genre_dict[genre] = [genre_dict[genre][0]+1, genre_dict[genre][1]+rating]

    others = 0
    o_rating = 0.0
    k =0
    for genre, val in genre_dict.items():
        if val[0] <= 20:
            others += val[0]
            o_rating += val[1]
            k +=1
            del genre_dict[genre]
    
    genre_dict['Others'] = [others, o_rating]

    graph_dict = {}
    for genre, val in genre_dict.items():
        graph_dict[genre] = genre_dict[genre][1]/genre_dict[genre][0]
        genre_dict[genre] = [genre_dict[genre][0], genre_dict[genre][1]/genre_dict[genre][0]]
    
    pie = check_box(100, 100, pie)
    fill(BLACK)
    text('Pie Chart', 130, 125)
    text('Bar Graph', 280, 125)
    fill(WHITE)
    bar = check_box(250, 100, bar)
    if pie:
        pie_chart(graph_dict, 400, 400, 50, 50)
        pie_chart_legand(800, 100, graph_dict)
    if bar:
        fill(BLACK)
        text('Genre: ', 910, 970)
        text('Rating: ', 905, 1000)
        fill(WHITE)
        bar_graph(graph_dict, 200, 1000, 700, 1000, 50, genre_dict)

    movie = back_button(movie)


def tv_screen():
    global tv, pie, bar, comp
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
                genre_dict[genre] = [0, 0.0]
            genre_dict[genre] = [genre_dict[genre][0]+1, genre_dict[genre][1]+rating]

    others = 0
    o_rating = 0.0
    k =0
    for genre, val in genre_dict.items():
        if val[0] <= 50:
            others += val[0]
            o_rating += val[1]
            k +=1
            del genre_dict[genre]
    
    genre_dict['Others'] = [others, o_rating]

    graph_dict = {}
    for genre, val in genre_dict.items():
        graph_dict[genre] = genre_dict[genre][1]/genre_dict[genre][0] - 5
        genre_dict[genre] = [genre_dict[genre][0], genre_dict[genre][1]/genre_dict[genre][0]]
    
    pie = check_box(100, 100, pie)
    bar = check_box(250, 100, bar)
    if pie:
        pie_chart(graph_dict, 400, 350, 100, 200)
        pie_chart_legand(800, 100, graph_dict)
    if bar:
        fill(BLACK)
        text('Genre: ', 910, 970)
        text('Rating: ', 905, 1000)
        fill(WHITE)
        bar_graph(graph_dict, 200, 1000, 700, 1000, 200, genre_dict)
    comp = check_box(410, 100, comp)
    if comp:
        pie = False
        bar = False
        genre_check_box(800, 100, graph_dict)
        comp_dict = {}
        clr_lst = []
        for item in comp_list:
            comp_dict[item[0]] = graph_dict[item[0]]
            clr_lst.append(item[1])
        pie_chart(comp_dict, 400, 450, 100, 100, 200, clr_lst)
        pie_chart_percent(comp_dict, 800, 800, 200, clr_lst)

    fill(BLACK)
    text('Pie Chart', 130, 125)
    text('Bar Graph', 280, 125)
    text('Compare Genre', 440, 125)
    fill(WHITE)
    tv = back_button(tv)

def draw():
    background(BGCLR)
    
    if not(movie or tv):
        selection_screen()

    if movie:
        movie_screen()
    if tv:
        tv_screen()
