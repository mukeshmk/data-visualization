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
x = 1600
y = 600
z = 100

# Colours used
BGCLR = '#FFFFFF'
ATTACK = '#D81E5B'
RETREAT = '#39B54A'
BLUE = '#41C5F9'
BLACK = 0

# variable realted to toggle
cty = True
div_t = [True]* 6
x_t = [x]*3 + [x+z]*3
y_t = [y, y+z, y+2*z]*2
clr = [ATTACK] * 3 + [RETREAT] * 3

def setup():
    fullScreen()

def draw():
    background(BGCLR)
    global tempX, tempY, plat, plon, div_t, cty
    troops_data = loadTable("data/minards-troops-data.csv", "header")
    city_data = loadTable("data/minards-city-data.csv", "header")
    temp_data = loadTable("data/minards-temp-data.csv", "header")

    i = 0
    for row in temp_data.rows():
        # temprature details
        lont = row.getFloat("LONT")
        temp = row.getInt("TEMP")
        days = row.getInt("DAYS")
        mon = row.getString("MON")
        day = row.getInt("DAY")

        if str(lont) != 'nan':
            x, y = locToXY(0, lont)
            y = 900 - temp*4
            fill(BLUE)
            circle(x, y, days*3)
            fill(BLACK)
            textSize(15)
            temptxt = str(temp) + ".0" + u'\N{DEGREE SIGN}' + ", " + str(mon) + " " + str(day) 
            text(temptxt, x, y+40)
            stroke(0)
            strokeWeight(1)
            if i != 0:
                line(tempX, tempY, x, y)
            tempX = x
            tempY = y
        i = i + 1

    i = 0
    for row in troops_data.rows():
        # troops details
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
                        if div_t[0] and div == 1 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[3] and div == 1 and dir == 'R':
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div_t[1] and div == 2 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[4] and div == 2 and dir == 'R':
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div_t[2] and div == 3 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div_t[5] and div == 3 and dir == 'R':
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
            text(city, x, y+20)

    checkBoxArea()

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
    
        
