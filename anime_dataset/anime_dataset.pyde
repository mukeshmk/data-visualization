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
scatter = False
box_plt = False
comp_list = set()

def setup():
    fullScreen()

def median(sortedLst):
    # assumes a sorted list
    lstLen = len(sortedLst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[0: index+1], sortedLst[index: lstLen], sortedLst[index]
    else:
        return sortedLst[0: index], sortedLst[index+1: lstLen], (sortedLst[index] + sortedLst[index + 1])/2.0

def draw_blox_plot(x, y, w, val_lst, i):
    s = 100
    o = 200
    if 0 in val_lst:
        val_lst =  [e for e in val_lst if e != 0]
    sl = sorted(val_lst)
    if len(val_lst) < 3:
        return
    sl1, sl2, q2 = median(sl)
    _, _, q1 = median(sl1)
    _, _, q3 = median(sl2)
    iqr = q3 - q1
    _min = min(sl)
    _max = max(sl)
    rect(x, y + o - q1*s, w-10, -iqr*s)
    line(x + int((w-10)/2), y - _min*s+o, x + int((w-10)/2), y - q1*s+o)
    line(x + int((w-10)/2), y - q3*s+o, x + int((w-10)/2), y - _max*s+o)
    line(x, y - _min*s+o, x + w-10, y - _min*s+o)
    line(x, y - _max*s+o, x + w-10, y - _max*s+o)
    line(x, y - q2*s+o, x + w-10, y - q2*s+o)

def box_plot(data_dict, x, y, w, clr_lst=None):
    i = 0
    l = len(data_dict.keys())
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        x1 = x+(w/l)*i
        draw_blox_plot(x1, y, w/l, _val, i)
        i+=1

def scatter_plot(data_dict, x, y, w, clr_lst=None):
    i = 0
    l = len(data_dict.keys())
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        x1 = x+(w/l)*i
        y1 = y - _val[0]/3
        r = _val[1]*10
        circle(x1, y1, r)
        i+=1

def legand_check_box(x, y, genre_dict, enable = False, add_val = 5):
    global comp_list
    i = 0
    j = 0
    s = 25
    for _key, _val in genre_dict.items():
        fill(CLR_LIST[i])
        x1 = x+(200*j)
        y1 = y+(25*(i+1)) - (275*j)
        square(x1, y1, 25)
        if mousePressed and enable:
            if mouseX > x1 and mouseX < x1+s and mouseY > y1 and mouseY < y1+s:
                if (_key, CLR_LIST[i]) in comp_list:
                    comp_list.remove((_key, CLR_LIST[i]))
                else:
                    comp_list.add((_key, CLR_LIST[i]))
        fill(BLACK)
        if mouseX > x1 and mouseX < x1+s and mouseY > y1 and mouseY < y1+s:
            text('Value: ' + str(_val + add_val), x, y)
        text(_key, x+(200*j)+30, y+(25*(i+1)) - (275*j)+25)
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
        
def bar_graph(data_dict, x, y, w, max_val, s, legand, clr_lst=None):
    fill(WHITE)
    i = 0
    l = len(data_dict.keys())
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
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

def screen(type):
    global movie, tv, pie, bar, comp, scatter, box_plt
    data = []
    if type == 'tv':
        data = loadTable("data/tv_type_anime.csv", "header")
    elif type == 'movie':
        data = loadTable("data/movie_type_anime.csv", "header")
    else:
        return
    
    genre_dict = {}
    genre_rating_dict = {}
    for row in data.rows():

        name = row.getString('name')
        genre_list = row.getString('genre').split(', ')
        eps = row.getInt('episodes')
        #type = row.getString('type')
        rating = row.getFloat('rating')
        mem = row.getInt('members')
        
        for genre in genre_list:
            if genre not in genre_dict:
                genre_dict[genre] = [0, 0.0]
                genre_rating_dict[genre] = []
            genre_dict[genre] = [genre_dict[genre][0]+1, genre_dict[genre][1]+rating]
            genre_rating_dict[genre].append(rating)

    others = 0
    o_rating = 0.0
    k = 0
    s = 0
    if type == 'tv':
        s = 50
    elif type == 'movie':
        s = 20
    for genre, val in genre_dict.items():
        if val[0] <= s:
            others += val[0]
            o_rating += val[1]
            k +=1
            del genre_dict[genre]
    
    genre_dict['Others'] = [others, o_rating]
    c = 0
    if type == 'tv':
        c = 5
    elif type == 'movie':
        c = 0

    graph_dict = {}
    for genre, val in genre_dict.items():
        graph_dict[genre] = genre_dict[genre][1]/genre_dict[genre][0] - c
        genre_dict[genre] = [genre_dict[genre][0], genre_dict[genre][1]/genre_dict[genre][0]]
    
    pie = check_box(100, 100, pie)
    bar = check_box(250, 100, bar)
    scatter = check_box(410, 100, scatter)
    box_plt = check_box(590, 100, box_plt)
    comp = check_box(750, 100, comp)

    fill(BLACK)
    text('Pie Chart', 130, 125)
    text('Bar Graph', 280, 125)
    text('Scatter Plot', 440, 125)
    text('Box Plot', 620, 125)
    text('Compare Genre', 780, 125)
    fill(WHITE)

    if pie:
        bar = False
        scatter = False
        box_plt = False
        comp = False
        if type == 'tv':
            pie_chart(graph_dict, 500, 600, 100, 200)
            legand_check_box(1300, 100, graph_dict)
        elif type == 'movie':
            pie_chart(graph_dict, 400, 400, 50, 50)
            legand_check_box(1100, 100, graph_dict, add_val = 0)
    if bar:
        pie = False
        scatter = False
        box_plt = False
        comp = False
        fill(BLACK)
        text('Genre: ', 910, 970)
        text('Rating: ', 905, 1000)
        fill(WHITE)
        if type == 'tv':
            bar_graph(graph_dict, 200, 1050, 700, 1000, 200, genre_dict)
        elif type == 'movie':
            bar_graph(graph_dict, 200, 1000, 700, 1000, 50, genre_dict)
    if scatter:
        pie = False
        bar = False
        box_plt = False
        comp = False
        scatter_plot(genre_dict, 200, 1000, 1400)
        if type == 'tv':
            legand_check_box(1300, 100, graph_dict)
        else:
            legand_check_box(1100, 100, graph_dict, add_val = 0)
        fill(BLACK)
        line(140, 1030, 1650, 1030)
        line(140, 1030, 140, 200)
        text('Genre', 750, 1060)
        if type == 'tv':
            text('Anime\nCount', 40, 550)
        elif type == 'movie':
            text('Anime\nMovie\nCount', 40, 530)
        fill(WHITE)
    if box_plt:
        pie = False
        bar = False
        scatter = False
        comp = False
        box_plot(genre_rating_dict, 80, 1100, 1400)
        if type == 'tv':
            legand_check_box(1300, 60, graph_dict)
        elif type == 'movie':
            legand_check_box(1330, 60, graph_dict, add_val = 0)
        fill(BLACK)
        line(70, 1060, 1550, 1060)
        line(70, 1060, 70, 300)
        text('Genre', 1450, 1000)
        text('Rating', 100, 320)
        fill(WHITE)
    if comp:
        pie = False
        bar = False
        scatter = False
        box_plt = False
        comp_dict = {}
        clr_lst = []
        for item in comp_list:
            comp_dict[item[0]] = graph_dict[item[0]]
            clr_lst.append(item[1])
        if type == 'tv':
            legand_check_box(1300, 100, graph_dict, True)
            pie_chart(comp_dict, 400, 400, 100, 100, 200, clr_lst)
            bar_graph(comp_dict, 200, 1050, 700, 1000, 200, genre_dict, clr_lst)
        elif type == 'movie':
            legand_check_box(1100, 100, graph_dict, True, 0)
            pie_chart(comp_dict, 400, 400, 80, 50, 200, clr_lst)
            bar_graph(comp_dict, 200, 1050, 700, 1000, 50, genre_dict, clr_lst)
        pie_chart_percent(comp_dict, 1200, 800, 200, clr_lst)
        if len(comp_dict.keys()) > 0:
            fill(BLACK)
            text('Genre: ', 910, 970)
            text('Rating: ', 905, 1000)
            fill(WHITE)

    if type == 'tv':
        tv = back_button(tv)
    elif type == 'movie':
        movie = back_button(movie)

def draw():
    background(BGCLR)
    
    if not(movie or tv):
        selection_screen()

    if movie:
        screen('movie')
    if tv:
        screen('tv')
