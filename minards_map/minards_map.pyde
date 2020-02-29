# mapper variables
geoLeft = 22.82
geoRight = 38.74
geoTop = 56.89
geoBot = 52.8

# map resolution
screenWid = 1520
screenLen = 1080

tempX = -1
tempY = -1

plat = -1
plon = -1

# toogle coordinates
x = 1700
y = 270
z = 100

# Colours used
BGCLR = '#FFFFFF'
ATTACK = '#D81E5B'
RETREAT = '#39B54A'
BLUE = '#41C5F9'
BLACK = 0

# variable realted to toggle
cty = True
div_t = [True]* 9
att = ret = True
x_t = [x]*3 + [x+z]*3
y_t = [y, y+z, y+2*z]*2
clr = [ATTACK] * 3 + [RETREAT] * 3

def setup():
    fullScreen()

def draw():
    background(BGCLR)
    global tempX, tempY, plat, plon, div_t, cty, att, ret

    troops_data = loadTable("data/minards-troops-data.csv", "header")
    city_data = loadTable("data/minards-city-data.csv", "header")
    temp_data = loadTable("data/minards-temp-data.csv", "header")

    textSize(45)
    stroke(BLACK)
    strokeWeight(2.0)
    text("CHARLES JOSEPH MINARD'S MAP OF THE NAPOLEAN RUSSIA CAMPAIGN",100,100)

    att = ret = div_t[6] = div_t[7] = div_t[8] = True

    # key press functionality
    if keyPressed:
        if key == 'a' or key == 'A':
            ret = False
        if key == 'r' or key == 'R':
            att = False
        if key == '1':
            div_t[7] = div_t[8] = False
        if key == '2':
            div_t[6] = div_t[8] = False
        if key == '3':
            div_t[6] = div_t[7] = False

    # loop for temprature details
    i = 0
    for row in temp_data.rows():
        lont = row.getFloat("LONT")
        temp = row.getInt("TEMP")
        days = row.getInt("DAYS")
        mon = row.getString("MON")
        day = row.getInt("DAY")

        if str(lont) != 'nan':
            x, y = locToXY(0, lont)
            y = 900 - temp*4
            fill(BLUE)
            circle(x, y, days*3 + 5)
            fill(BLACK)
            textSize(15)
            temptxt = str(temp) + ".0" + u'\N{DEGREE SIGN}' + ", " + str(mon) + " " + str(day) 
            text(temptxt, x, y+40)
            text(str(days) + " days", x, y - 30)
            stroke(0)
            strokeWeight(1)
            if i != 0:
                line(tempX, tempY, x, y)
            tempX = x
            tempY = y
        i = i + 1
    text("*The blue circles represent the total number of days the troops endured that particular temperature", x+500, y+50)

    # loop for legand
    x = 1500
    y = 500
    i = 1
    textSize(30)
    text("LEGAND", x, y-270)
    textSize(15)
    line(x, y-265, x+120, y-265)
    for row in troops_data.rows():
        surv = row.getInt("SURV")
        sw = surv / 30000.0 * 6.0
        if surv / 30000.0 * 6.0 < 2.0 :
            sw = 2.0
        strokeWeight(sw)
        line(x, y, x, y-5*i)
        if i % 4 == 0:
            text(surv, x+50, y-5*i)
        i = i + 1

    # loop for troops details
    i = 0
    for row in troops_data.rows():
        lonp = row.getFloat("LONP")
        latp = row.getFloat("LATP")
        surv = row.getInt("SURV")
        dir = row.getString("DIR")
        div = row.getInt("DIV")

        if str(lonp) != 'nan':
            if plon != -1:
                sw = surv / 30000.0 * 6.0
                if surv / 30000.0 * 6.0 < 2.0 :
                    sw = 2.0 
                strokeWeight(sw)
                x, y = locToXY(latp, lonp)                
                if i != 1 and i != 0 and i != 28 and i != 45:
                        if div_t[0] and div == 1 and dir == 'A' and div_t[6] and att:
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[3] and div == 1 and dir == 'R' and div_t[6] and ret:
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div_t[1] and div == 2 and dir == 'A' and div_t[7] and att:
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[4] and div == 2 and dir == 'R' and div_t[7] and ret:
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div_t[2] and div == 3 and dir == 'A' and div_t[8] and att:
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[5] and div == 3 and dir == 'R' and div_t[8] and ret:
                            stroke(RETREAT)
                            line(plon, plat, x, y)
            plon = x
            plat = y
        i = i + 1

    for row in city_data.rows():
        # city details
        lonc = row.getFloat("LONC")
        latc = row.getFloat("LATC")
        city = row.getString("CITY")

        if cty and str(latc) != 'nan':
            x, y = locToXY(latc, lonc)
            fill(BLACK)
            loc_marker(x, y)
            textSize(15)
            text(city, x-20, y+20)

    checkBoxArea()

    x = 1500
    y = 600
    z = 25
    textSize(30)
    text("Instructions:", x-20, y)
    textSize(15)
    line(x-20, y+5, x+160, y+5)
    for i in range(7):
        if i == 1:
            continue
        fill(BLACK)
        circle(x-10, y+z*(i+1)-5, 5)
    text("Toggle checkboxes to view attack and retreat", x, y+z)
    text("Key Press Actions:", x, y+z*2)
    text("press 'a' to view 'Attack' path only", x, y+z*3)
    text("press 'r' to view 'Retreat' path only", x, y+z*4)
    text("press '1' to view Division 1's path only", x, y+z*5)
    text("press '2' to view Division 2's path only", x, y+z*6)
    text("press '3' to view Division 3's path only", x, y+z*7)

    t = "The illustration depicts Napoleon's army departing the Polish-Russian border. \n" +\
    "A thick band illustrates the size of his army at specific geographic \n" +\
    "points during their advance and retreat. \n" +\
    "It displays six types of data in two dimensions: the number of Napoleon's troops; \n" +\
    "the distance traveled; temperature; latitude and longitude; direction of travel; \n" +\
    "and location relative to specific dates without making mention of Napoleon;"

    text(t, 860, 670)

def locToXY(lat, lon):
    y = screenLen - screenLen * (lat - geoBot) / (geoTop - geoBot)
    x = screenWid * (lon - geoLeft) / (geoRight - geoLeft)
    return x, y

def loc_marker(x, y):
    fill(BLACK)
    stroke(BLACK)
    strokeWeight(1.0)
    square(x-5, y-5, 10)

def checkBox(x, y, val):
    s = 25
    if mousePressed:
        if mouseX > x-s and mouseX < x+s and mouseY > y-s and mouseY < y+s:
            val = not val
    stroke(BGCLR)
    square(x, y, s)
    return val

def drawBox(val, x, y, clr):
    s = 25
    stroke(BLACK)
    strokeWeight(2)
    if not val:
        noFill()
    else:
        fill(clr)
    square(x, y, s)

def checkBoxArea():
    toggletext = []
    toggletext.append("Attack")
    toggletext.append("Attack")
    toggletext.append("Attack")
    toggletext.append("Retreat")
    toggletext.append("Retreat")
    toggletext.append("Retreat")

    noFill()
    strokeWeight(2.0)
    rect(x_t[0]-z*2 - 40, y_t[0]-z, 400, 630)

    drawBox(cty, x_t[0], y_t[0]-z/1.5, BLACK)
    for i in range(6):
        drawBox(div_t[i], x_t[i], y_t[i], clr[i])
        textSize(20)
        stroke(BLACK)
        fill(BLACK)
        text(toggletext[i], x_t[i]-20, y_t[i]-5)
    text("Show Cities", x_t[0]+40, y_t[0]-z/1.5+20)
    text("Div 1:", x_t[0]-70, y_t[0]+20)
    text("Div 2:", x_t[0]-70, y_t[4]+20)
    text("Div 3:", x_t[0]-70, y_t[2]+20)


def mouseClicked():
    global div_t, cty
    div_t[0] = mouseClick(x_t[0], y_t[0], div_t[0])
    div_t[1] = mouseClick(x_t[1], y_t[1], div_t[1])
    div_t[2] = mouseClick(x_t[2], y_t[2], div_t[2])
    div_t[3] = mouseClick(x_t[3], y_t[3], div_t[3])
    div_t[4] = mouseClick(x_t[4], y_t[4], div_t[4])
    div_t[5] = mouseClick(x_t[5], y_t[5], div_t[5])
    cty = mouseClick(x_t[0], y_t[0]-z/1.5, cty)

def mouseClick(x, y, val):
    s = 25
    if mouseX > x and mouseX < x+s and mouseY > y and mouseY < y+s:
        val = not val
    return val
