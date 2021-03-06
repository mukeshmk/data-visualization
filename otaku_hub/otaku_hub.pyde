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
bubble = False
box_plt = False
nx = False
show_mem = False
bar_zoom = False
comp_list = set()
nw_plt = None

img = None

def setup():
    global img
    img = loadImage("kakashi.png")
    fullScreen()

def draw_network_node(x, y, r, a, c, v):
    x1 = x + (r * cos(a))
    y1 = y + (r * sin(a))
    fill(c)
    circle(x1, y1, v[0])
    x2 = x1 + (v[0]/2 * cos(radians(270))) - v[0]/2
    y2 = y1 + (v[0]/2 * sin(radians(270)))
    x3 = x1 + (v[0]/2 * cos(radians(90))) + v[0]/2
    y3 = y1 + (v[0]/2 * sin(radians(90)))
    fill(BLACK)
    text(v[1], x2-50, y3+25)
    hover_over_legand(x2, y2, x3, y3, [v[1], v[2]])
    fill(WHITE)
    return x1 - (v[0]/2 * cos(a)), y1  - (v[0]/2 * sin(a))

def network_graph(network_data, x, y, r, type, mem_info=False):
    if nw_plt is None:
        return
    i = 0
    l = 5
    if mem_info:
        l = 7
    min_rat = network_data[nw_plt[0]]['min_rating']
    max_rat = network_data[nw_plt[0]]['max_rating']
    min_eps = network_data[nw_plt[0]]['min_eps']
    max_eps = network_data[nw_plt[0]]['max_eps']
    count = network_data[nw_plt[0]]['count']
    min_mem = network_data[nw_plt[0]]['min_mem']
    max_mem = network_data[nw_plt[0]]['max_mem']

    if type == 'tv':
        xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [min_eps*5, 'Min Episodes', min_eps])
        line(x, y, xn, yn)
        i+=1
        m = max_eps
        if max_eps < min_eps*5:
            m = max_eps*5
        if max_eps > r:
            m = r
        xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [m, 'Max Episodes', max_eps])
        line(x, y, xn, yn)
        i+=1
    if type == 'movie' or mem_info:
        m = min_mem/10
        if min_mem < 100:
            m = min_mem
        xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [m, 'Min Members', min_mem])
        line(x, y, xn, yn)
        i+=1
        m = max_mem/1000
        if m < min_eps:
            m = m*2
        if m > r:
            m = r
        xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [m, 'Max Members', max_mem])
        line(x, y, xn, yn)
        i+=1
    c = count
    if count > r:
        c = r
    xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [min_rat*10, 'Min Rating', min_rat])
    line(x, y, xn, yn)
    i+=1
    xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [max_rat*10, 'Max Rating', max_rat])
    line(x, y, xn, yn)
    i+=1
    xn, yn = draw_network_node(x, y, r, radians(360/l*i), nw_plt[1], [c, 'Count', count])
    line(x, y, xn, yn)
    i+=1
    draw_network_node(x, y, 0, 0, nw_plt[1], [60, nw_plt[0], ''])

def median(sortedLst):
    # assumes a sorted list
    lstLen = len(sortedLst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[0: index+1], sortedLst[index: lstLen], sortedLst[index]
    else:
        return sortedLst[0: index], sortedLst[index+1: lstLen], (sortedLst[index] + sortedLst[index + 1])/2.0

def draw_blox_plot(x, y, w, s, o, val_lst):
    if 0 in val_lst:
        val_lst =  [e for e in val_lst if e != 0]
    sl = sorted(val_lst)
    if len(val_lst) < 3:
        return 100, 0
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
    return _min, _max

def box_plot(data_dict, x, y, w, s=100, o=200, clr_lst=None):
    i = 0
    l = len(data_dict.keys())
    _min = 100
    _max = 0
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        x1 = x+(w/l)*i
        _mi, _ma = draw_blox_plot(x1, y, w/l, s, o, _val)
        if _mi < _min:
            _min = _mi
        if _ma > _max:
            _max = _ma
        i+=1
    fill(BLACK)
    line(x-10, y-40, x+1470, y-40)
    line(x-10, y-40, x-10, y-800)
    line(x-20, y - _min*s+o, x, y - _min*s+o)
    line(x-20, y - _max*s+o, x, y - _max*s+o)
    text(_min, x-120, y - _min*s+o)
    text(_max, x-120, y - _max*s+o)
    fill(WHITE)

def bubble_chart(data_dict, x, y, w, clr_lst=None):
    i = 0
    l = len(data_dict.keys())
    _min = 1000
    _max = 0
    if clr_lst is None:
        clr_lst = CLR_LIST
    for _key, _val in data_dict.items():
        fill(clr_lst[i])
        x1 = x+(w/l)*i
        y1 = y - _val[0]/3
        r = _val[1]*10
        circle(x1, y1, r)
        if _val[0] < _min:
            _min = _val[0]
        if _val[0] > _max:
            _max = _val[0]
        i+=1
    fill(BLACK)
    text(_min, x-120, y - _min/3)
    text(_max, x-120, y - _max/3)
    line(x-60, y+30, x+1450, y+30)
    line(x-60, y+30, x-60, y-700)
    line(x-50, y - _min/3, x-70, y - _min/3)
    line(x-50, y - _max/3, x-70, y - _max/3)
    fill(WHITE)

def legand_check_box(x, y, genre_dict, enable = False, add_val = 5):
    global comp_list, nw_plt
    i = 0
    j = 0
    s = 25
    fill(BLACK)
    text('Value: ', x, y)
    fill(WHITE)
    for _key, _val in genre_dict.items():
        fill(CLR_LIST[i])
        x1 = x+(200*j)
        y1 = y+(25*(i+1)) - (275*j)
        square(x1, y1, 25)
        if mousePressed and enable:
            if mouseX > x1 and mouseX < x1+s and mouseY > y1 and mouseY < y1+s:
                nw_plt = (_key, CLR_LIST[i])
                if (_key, CLR_LIST[i]) in comp_list:
                    comp_list.remove((_key, CLR_LIST[i]))
                else:
                    comp_list.add((_key, CLR_LIST[i]))
        fill(BLACK)
        if mouseX > x1 and mouseX < x1+s and mouseY > y1 and mouseY < y1+s:
            text(str(_val + add_val), x+80, y)
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
    fill(WHITE)
    if inc > 0:
        circle(x, y, 100)

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
    background('#605354')
    image(img, 0-20, 0)

    fill('#b53a4e')
    textSize(150)
    text('OtakuHub', 1150, 200)
    fill('#669966')
    textSize(100)
    text('Anime Stats for an Otaku', 650, 350)
    fill('#f5dbc4')
    textSize(50)
    text('Get Stats about: ', 1100, 650)

    movie = check_box(1500, 620, movie)
    tv = check_box(1650, 620, tv)
    textSize(30)
    text('Movies', 1500+32, 620+22)
    text('TV Shows', 1650+32, 620+22)

    fill('#ced0dc')
    text('Anime Dataset Visualisation: A Project for CS7DS4 - DATA VISUALISATION', 800, 1000)
    text('By: Mukesh Arambakam - 19301497', 1300, 1050)

def screen(type):
    global movie, tv, pie, bar, comp, bubble, box_plt, nx, show_mem, bar_zoom
    tx = 1300
    ty = 500
    ts = 30
    data = []
    if type == 'tv':
        data = loadTable("data/tv_type_anime.csv", "header")
    elif type == 'movie':
        data = loadTable("data/movie_type_anime.csv", "header")
    else:
        return
    
    genre_dict = {}
    genre_rating_dict = {}
    network_data = {}
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
                network_data[genre] = {}
            genre_dict[genre] = [genre_dict[genre][0]+1, genre_dict[genre][1]+rating]
            genre_rating_dict[genre].append(rating)
            # setup types of network data
            if 'min_rating' not in network_data[genre]:
                network_data[genre]['min_rating'] = rating
            if 'max_rating' not in network_data[genre]:
                network_data[genre]['max_rating'] = rating
            if 'min_eps' not in network_data[genre]:
                network_data[genre]['min_eps'] = eps
            if 'max_eps' not in network_data[genre]:
                network_data[genre]['max_eps'] = eps
            if 'count' not in network_data[genre]:
                network_data[genre]['count'] = 0
            if 'min_mem' not in network_data[genre]:
                network_data[genre]['min_mem'] = mem
            if 'max_mem' not in network_data[genre]:
                network_data[genre]['max_mem'] = mem
            # set network data
            if network_data[genre]['min_rating'] > rating and rating != 0:
                network_data[genre]['min_rating'] = rating
            if network_data[genre]['max_rating'] < rating:
                network_data[genre]['max_rating'] = rating
            if network_data[genre]['min_eps'] > eps and eps != 0:
                network_data[genre]['min_eps'] = eps
            if network_data[genre]['max_eps'] < eps:
                network_data[genre]['max_eps'] = eps
            if network_data[genre]['min_mem'] > mem and mem != 0:
                network_data[genre]['min_mem'] = mem
            if network_data[genre]['max_mem'] < mem:
                network_data[genre]['max_mem'] = mem
            network_data[genre]['count'] +=1

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
    bubble = check_box(410, 100, bubble)
    box_plt = check_box(605, 100, box_plt)
    nx = check_box(100, 150, nx)
    comp = check_box(750, 100, comp)

    fill(BLACK)
    text('Pie Chart', 130, 125)
    text('Bar Graph', 280, 125)
    text('Bubble Chart', 440, 125)
    text('Box Plot', 635, 125)
    text('Compare Genre', 780, 125)
    text('Network Graph', 130, 175)
    fill(WHITE)

    if pie:
        bar = False
        bubble = False
        box_plt = False
        comp = False
        nx = False
        bar_zoom = check_box(920, 900, bar_zoom)
        z = 1
        if bar_zoom:
            z = 1.5
        else:
            z = 1
        if type == 'tv':
            pie_chart(graph_dict, 500, 600, 150, 200*z)
            legand_check_box(1300, 100, graph_dict)
        elif type == 'movie':
            pie_chart(graph_dict, 500, 600, 75, 60*z)
            legand_check_box(1100, 100, graph_dict, add_val = 0)
        fill(BLACK)
        text('Click to toggle Scale', 920+40, 900+25)
        textSize(50)
        text('Hover over the LEGEND boxes\nabove to see the avg rating', tx-120, ty - ts)
        textSize(ts-5)
        text('The Pie Chart Represents various genres of', tx, ty + ts*5)
        txt = ''
        if type == 'tv':
            txt = 'TV Shows'
        elif type == 'movie':
            txt = 'Movies'
        text('Anime ' + txt + ', where each coloured segment', tx, ty + ts*6)
        text('represents a particular genre and the radius of', tx, ty + ts*7)
        text('each segment represents the average rating of', tx, ty + ts*8)
        text('that genre.', tx, ty + ts*9)
        text('This is a derived data which doesn\'t exists as', tx, ty + ts*11)
        text('part of the dataset and is calculated from the data.', tx, ty + ts*12)
        text('Anime Genre VS Genre avg. Rating', 300, 1000)
    if bar:
        pie = False
        bubble = False
        box_plt = False
        comp = False
        nx = False
        bar_zoom = check_box(920, 900, bar_zoom)
        z = 1
        if bar_zoom:
            z = 1.5
        else:
            z = 1
        fill(BLACK)
        text('Click to toggle Scale', 920+40, 900+25)
        text('Genre: ', 910, 970)
        text('Rating: ', 905, 1000)
        fill(WHITE)
        if type == 'tv':
            bar_graph(graph_dict, 200, 1050, 700, 1000, 200*z, genre_dict)
        elif type == 'movie':
            bar_graph(graph_dict, 200, 1000, 700, 1000, 60*z, genre_dict)
        fill(BLACK)
        textSize(50)
        text('Hover over the GRAPH\'s bars\nto see the avg rating and genre', tx-150, ty - ts)
        textSize(ts-5)
        text('The Bar Graph Represents various genres of', tx, ty + ts*5)
        txt = ''
        if type == 'tv':
            txt = 'TV Shows'
        elif type == 'movie':
            txt = 'Movies'
        text('Anime ' + txt + ', where each coloured bar', tx, ty + ts*6)
        text('represents a particular genre and the height of', tx, ty + ts*7)
        text('each bar represents the average rating of', tx, ty + ts*8)
        text('that genre.', tx, ty + ts*9)
        text('This is a derived data which doesn\'t exists as', tx, ty + ts*11)
        text('part of the dataset and is calculated from the data.', tx, ty + ts*12)
        text('Anime Genre VS Genre avg. Rating', 300, 300)
    if bubble:
        pie = False
        bar = False
        box_plt = False
        comp = False
        nx = False
        bubble_chart(genre_dict, 200, 1000, 1400)
        if type == 'tv':
            legand_check_box(1300, 100, graph_dict)
        else:
            legand_check_box(1100, 100, graph_dict, add_val = 0)
        fill(BLACK)
        text('Genre', 750, 1060)
        if type == 'tv':
            text('Anime\nCount', 40, 550)
        elif type == 'movie':
            text('Anime\nMovie\nCount', 40, 530)
        textSize(50)
        text('Hover over the LEGEND boxes\nabove to see the avg rating', tx-120, ty - ts)
        textSize(25)
        text('Count of Anime in each Genre VS Genre\n(radius of circle represents avg. rating)', 300, 250)
        fill(WHITE)
    if box_plt:
        pie = False
        bar = False
        bubble = False
        comp = False
        nx = False
        if type == 'tv':
            box_plot(genre_rating_dict, 130, 1100, 1400)
            legand_check_box(1300, 60, graph_dict)
        elif type == 'movie':
            box_plot(genre_rating_dict, 130, 1100, 1400, 80, 100)
            legand_check_box(1330, 60, graph_dict, add_val = 0)
        fill(BLACK)
        text('Genre', 1550, 1000)
        text('Rating', 40, 320)
        text('Hover over the LEGEND boxes\nabove to see the avg rating', tx+ts*8, ty - ts*2)
        text('Anime Genre VS Genre avg. Rating', 300, 300)
        fill(WHITE)
    if nx:
        pie = False
        bar = False
        bubble = False
        box_plt = False
        comp = False
        if type == 'tv':
            show_mem = check_box(1300, 450, show_mem)
            fill(BLACK)
            text('Show Member Nodes', 1330, 475)
            fill(WHITE)
            network_graph(network_data, 600, 600, 300, type, show_mem)
            legand_check_box(1300, 100, graph_dict, True)
        else:
            network_graph(network_data, 600, 600, 300, type)
            legand_check_box(1100, 100, graph_dict, True, add_val = 0)
        fill(BLACK)
        textSize(50)
        text('Hover over the LEGEND boxes\nabove to see the avg rating', tx-120, ty - ts + 100)
        textSize(ts)
        text('Click on Genre in the LEGEND boxes to', tx, ty + ts*7)
        text('see the Network Graph for that genre.', tx, ty + ts*8)
        text('Hover the Graph\'s nodes to see', tx, ty + ts*10)
        text('the details of the node', tx, ty + ts*11)
    if comp:
        pie = False
        bar = False
        bubble = False
        box_plt = False
        nx = False
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
        fill(BLACK)
        textSize(50)
        text('Hover over the LEGEND boxes\nabove to see the avg rating', tx-120, ty - ts)
        textSize(ts)
        text('Click on Genres in the LEGEND boxes to', tx, ty + ts*4)
        text('start comparing genres via graphs.', tx, ty + ts*5)
        textSize(25)
        text('Anime Genre VS Genre avg. Rating', 300, 250)

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
