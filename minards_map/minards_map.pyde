geoLeft = 22.82
geoRight = 38.74
geoTop = 56.89
geoBot = 52.8

screenLen = 1080
screenWid = 1920

tempX = -1
tempY = -1

plat = -1
plon = -1

# Colours used
BGCLR = '#FFFFFF'
ATTACK = '#D81E5B'
RETREAT = '#39B54A'
BLACK = 0

def setup():
    fullScreen()
    #size(screenWid, screenLen)

def draw():
    background(BGCLR)
    global tempX, tempY, plat, plon
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
            fill(BLACK)
            text(str(temp), x, y+20)
            if tempX != -1 and  i != 0:
                stroke(0)
                strokeWeight(1)
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
                strokeWeight(surv/10000 * 1.5)
                x, y = locToXY(latp, lonp)
                if i != 1 and i != 0:
                    if(dir == "A"):
                        stroke(ATTACK)
                    else:
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
            text(city, x+10, y)

def locToXY(lat, lon):
    y = screenLen - screenLen * (lat - geoBot) / (geoTop - geoBot)
    x = screenWid * (lon - geoLeft) / (geoRight - geoLeft)
    return x, y

def loc_marker(x, y):
    square(x-5, y-5, 10)
    
        
