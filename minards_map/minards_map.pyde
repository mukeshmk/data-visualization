geoLeft = 22.82
geoRight = 38.74
geoTop = 56.89
geoBot = 52.8

screenWid = 1520
screenLen = 1080

tempX = -1
tempY = -1

plat = -1
plon = -1

# Colours used
BGCLR = '#FFFFFF'
ATTACK = '#D81E5B'
RETREAT = '#39B54A'
BLUE = '#41C5F9'
BLACK = 0

cty = div1A = div1R = div2A = div2R = div3A = div3R = True

def setup():
    fullScreen()
    #size(screenWid, screenLen)

def draw():
    background(BGCLR)
    global tempX, tempY, plat, plon, div1A, div1R, div2A, div2R, div3A, div3R, cty
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
            temptxt = str(temp) + ".0" + u'\N{DEGREE SIGN}' + ", " + str(mon) + " " + str(day) 
            text(temptxt, x, y+40)
            
            stroke(0)
            strokeWeight(1)
            if i != 0:
                line(tempX, tempY, x, y)
            tempX = x
            tempY = y
        else:
            tempX = tempY -1
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

                #div1 = checkBox(1600, 600, div1)
                #div2 = checkBox(1600, 700, div2)
                #div3 = checkBox(1600, 800, div3)
                
                if cty and i != 1 and i != 0 and i != 28 and i != 45:
                        if div1A and div == 1 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div1R and div == 1 and dir == 'R':
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div2A and div == 2 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div2R and div == 2 and dir == 'R':
                            stroke(RETREAT)
                            line(plon, plat, x, y)
                        if div3A and div == 3 and dir == 'A':
                            stroke(ATTACK)
                            line(plon, plat, x, y)
                        if div3R and div == 3 and dir == 'R':
                            stroke(RETREAT)
                            line(plon, plat, x, y)

            plon = x
            plat = y
        else:
            plon = plat = -1
        i = i + 1
    
    for row in city_data.rows():
        # city details
        lonc = row.getFloat("LONC")
        latc = row.getFloat("LATC")
        city = row.getString("CITY")
        
        if str(latc) != 'nan':
            x, y = locToXY(latc, lonc)
            fill(BLACK)
            loc_marker(x, y)
            text(city, x, y+20)

    drawCheckBox()

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

def drawCheckBox():
    x = 1600
    y = 600
    s = 25
    z = 100
    
    if not cty:
        noFill()
    else:
        fill(BLACK)
    square(x, y-z, s)
    
    if not div1A:
        noFill()
    else:
        fill(BLACK)
    square(x, y, s)
    
    if not div2A:
        noFill()
    else:
        fill(BLACK)
    square(x, y+z, s)
    
    if not div3A:
        noFill()
    else:
        fill(BLACK)
    square(x, y+2*z, s)
    
    if not div1R:
        noFill()
    else:
        fill(BLACK)
    square(x+z, y, s)
    
    if not div2R:
        noFill()
    else:
        fill(BLACK)
    square(x+z, y+z, s)
    
    if not div3R:
        noFill()
    else:
        fill(BLACK)
    square(x+z, y+2*z, s)

def mouseClicked():
    global div1A, div2A, div3A, div1R, div2R, div3R, cty
    x = 1600
    y = 600
    z = 100

    div1A = mouseClick(x, y, div1A)
    div2A = mouseClick(x, y+z, div2A)
    div3A = mouseClick(x, y+2*z, div3A)
    div1R = mouseClick(x+z, y, div1R)
    div2R = mouseClick(x+z, y+z, div2R)
    div3R = mouseClick(x+z, y+2*z, div3R)
    cty = mouseClick(x, y-z, cty)

def mouseClick(x, y, val):
    s = 25
    if mouseX > x and mouseX < x+s and mouseY > y and mouseY < y+s:
        val = not val
    return val 
    
        
