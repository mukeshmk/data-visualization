R = 1000

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



def setup():
    fullScreen()
    #size(screenWid, screenLen)
    background(0, 0, 0)

def draw():
    global tempX, tempY, plat, plon
    table = loadTable("minard-data.csv", "header")

    i = 0
    for row in table.rows():
        fill(255)
        # city details
        lonc = row.getFloat("LONC")
        latc = row.getFloat("LATC")
        city = row.getString("CITY")
        # temprature details
        lont = row.getFloat("LONT")
        temp = row.getInt("TEMP")
        days = row.getInt("DAYS")
        mon = row.getString("MON")
        day = row.getInt("DAY")
        # path details
        lonp = row.getFloat("LONP")
        latp = row.getFloat("LATP")
        surv = row.getInt("SURV")
        dir = row.getString("DIR")
        div = row.getInt("DIV")

        if str(latc) != 'nan': 
            x, y = locToXY(latc, lonc)
            text(city, x, y)

        if str(lont) != 'nan':
            fill(130)
            x, y = locToXY(0, lont)
            y = 900 - temp*4
            fill(255)
            text(str(temp), x, y+20)
            if tempX != -1:
                stroke(255)
                if i != 0:
                    strokeWeight(1)
                    line(tempX, tempY, x, y)
            tempX = x
            tempY = y

        if str(lonp) != 'nan':
            if plon != -1:
                strokeWeight(surv/10000 * 1.5)
                x, y = locToXY(latp, lonp)
                if i != 1 and i != 0:
                    line(plon, plat, x, y)

            plon = x
            plat = y

        i = i + 1

def locToXY(lat, lon):
    y = screenLen - screenLen * (lat - geoBot) / (geoTop - geoBot)
    x = screenWid * (lon - geoLeft) / (geoRight - geoLeft)
    return x, y
    
        
