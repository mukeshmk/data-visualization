R = 1000

geoLeft = 22.82
geoRight = 38.74
geoTop = 56.89
geoBot = 52.8

screenLen = 1080
screenWid = 1920

def setup():
    fullScreen()
    #size(screenWid, screenLen)
    background(0, 0, 0)

def draw():
    table = loadTable("minard-data.csv", "header")
    i = 0
    for row in table.rows():
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
            x, y = locToXY(lonc, latc)
            text(city, x, y)
            i = i + 1
        
def locToXY(lat, lon):
    x = screenWid*(lat-geoLeft)/(geoRight-geoLeft)
    y = screenLen - screenLen*(lon-geoBot)/(geoTop-geoBot)
    return x, y
    
        
