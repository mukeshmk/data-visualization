spin = 0
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
    deg = float(spin)*radians(30)
    background(0, 0, 0)
    table = loadTable("nightingale-rose.csv", "header")
    for row in table.rows():
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

            # to write the text
            stroke(255)

            # to calc rotational degree
            t = deg + float(i)*radians(30) + radians(15)

            # to calc point on the circle
            # X = Cx + (r * cos(angle))
            # Y = Cy + (r * sin(angle))
            x = (x1 + (270 + zoom*250)*cos(t)) # replace 270 with disr*60 works but looks weird
            y = (y1 + (270 + zoom*250)*sin(t))

            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            # write text after translation
            text(mny, 0, 0)
            popMatrix()

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

            # to write the text
            stroke(255)

            # to calc rotational degree
            t = deg + float(i-12)*radians(30) + radians(15)

            # to calc point on the circle
            # X = Cx + (r * cos(angle))
            # Y = Cy + (r * sin(angle))
            x = (x2 + (140 + zoom*110)*cos(t)) # replace 140 with disr*60 works but looks weird
            y = (y2 + (140 + zoom*110)*sin(t))

            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            # write text after translation
            text(mny, 0, 0)
            popMatrix()

            # diseases
            fill(180, 190, 190)
            arc(x2, y2, disr*(zoom*100 + 100), disr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
            # injuries
            fill(100, 80, 80)
            arc(x2, y2, injr*(zoom*100 + 100), injr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
            # other causes
            fill(230, 180, 170)
            arc(x2, y2, othr*(zoom*100 + 100), othr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30))
        i = i + 1
        
def mouseWheel(event):
    global spin
    spin += event.getCount()
    # keep value in range
    spin = spin % 12
    
def mouseClicked(): 
    global zoom
    if zoom == 0:
        zoom = 1
    else:
        zoom = 0
