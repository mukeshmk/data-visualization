rotate = 0
zoom = 0
x1 = 500
y1 = 500
x2 = 1300
y2 = 500

def setup():
    size(1920, 1080)
    background(0, 0, 0)

def draw():
    i = 0
    deg = float(rotate)*radians(30)
    background(0, 0, 0)
    table = loadTable("nightingale-rose.csv", "header")
    for row in table.rows():
        i = i + 1
        mny = row.getString("Month")
        sz = row.getInt("Average size of army")
        dis = row.getInt("Zymotic diseases")
        inj = row.getInt("Wounds & injuries")
        oth = row.getInt("All other causes")
        disr = row.getFloat("Zymotic diseases rate")
        injr = row.getFloat("Wounds & injuries rate")
        othr = row.getFloat("All other causes rate")

        if i < 12:
            # scale down the value
            disr = disr/200
            injr = injr/200
            othr = othr/200

            # diseases
            fill(180, 190, 190)
            arc(x1, y1, disr*(zoom*100 + 100), disr*(zoom*100 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30))
            # injuries
            fill(100, 80, 80)
            arc(x1, y1, injr*(zoom*100 + 100), injr*(zoom*100 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30))
            # other causes
            fill(230, 180, 170)
            arc(x1, y1, othr*(zoom*100 + 100), othr*(zoom*100 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30))
        else:
            # scale down the value
            disr = disr/100
            injr = injr/100
            othr = othr/100

            # diseases
            fill(180, 190, 190)
            arc(x2, y2, disr*(zoom*100 + 100), disr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
            # injuries
            fill(100, 80, 80)
            arc(x2, y2, injr*(zoom*100 + 100), injr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
            # other causes
            fill(230, 180, 170)
            arc(x2, y2, othr*(zoom*100 + 100), othr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
        
def mouseWheel(event):
    global rotate 
    rotate += event.getCount()
    # keep value in range
    rotate = rotate % 12
    
def mouseClicked(): 
    global zoom
    if zoom == 0:
        zoom = 1
    else:
        zoom = 0
