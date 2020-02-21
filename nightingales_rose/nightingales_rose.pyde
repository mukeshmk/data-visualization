spin = 0
zoom = 0
x1 = 1300
y1 = 500
x2 = 350
y2 = 350

def setup():
    size(1920, 1080)
    background(0, 0, 0)

def draw():
    vd = vi = vo = True
    i = 0
    deg = float(spin)*radians(30)
    strokeWeight(2.0)
    background(0, 0, 0)
    table = loadTable("nightingale-rose.csv", "header")

    if keyPressed:
        if key == 'd' or key == 'D':
            vi = vo = False
        if key == 'i' or key == 'I':
            vd = vo = False
        if key == 'o' or key == 'O':
            vd = vi = False

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
            # finding the radius and scaling down the value
            disr = sqrt((disr/100)*12/PI)/1.3
            injr = sqrt((injr/100)*12/PI)/1.3
            othr = sqrt((othr/100)*12/PI)/1.3

            # to write the text
            stroke(255)

            # to calc rotational degree
            t = deg + float(i)*radians(30) + radians(15)

            # to calc point on the circle
            # X = Cx + (r * cos(angle))
            # Y = Cy + (r * sin(angle))

            if disr*50 < 50:
                x = (x1 + (disr*51 + zoom*disr*51 + 100)*cos(t))
                y = (y1 + (disr*51 + zoom*disr*51 + 100)*sin(t))
            else:
                x = (x1 + (disr*51 + zoom*disr*51)*cos(t))
                y = (y1 + (disr*51 + zoom*disr*51)*sin(t))


            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            fill(255, 255, 255)
            # write text after translation
            text(mny, 0, 0)
            popMatrix()

            # diseases
            fill(180, 190, 190)
            if vd:
                arc(x1, y1, disr*(zoom*100 + 100), disr*(zoom*90 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30), PIE)
            # injuries
            fill(230, 180, 170)
            if vi:
                arc(x1, y1, injr*(zoom*100 + 100), injr*(zoom*90 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30), PIE)
            # other causes
            fill(100, 80, 80)
            if vo:
                arc(x1, y1, othr*(zoom*100 + 100), othr*(zoom*90 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30), PIE)
        else:
            # finding the radius and scaling down the value
            disr = sqrt((disr/100)*12/PI)/1.2
            injr = sqrt((injr/100)*12/PI)/1.2
            othr = sqrt((othr/100)*12/PI)/1.2

            # to write the text
            stroke(255)

            # to calc rotational degree
            t = deg + float(i-12)*radians(30) + radians(15)

            # to calc point on the circle
            # X = Cx + (r * cos(angle))
            # Y = Cy + (r * sin(angle))
            x = (x2 + (150 + zoom*110)*cos(t))
            y = (y2 + (150 + zoom*110)*sin(t))

            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            fill(255, 255, 255)
            # write text after translation
            text(mny, 0, 0)
            popMatrix()

            # diseases
            fill(180, 190, 190)
            if vd:
                arc(x2, y2, disr*(zoom*100 + 100), disr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30), PIE)
            # injuries
            fill(230, 180, 170)
            if vi:
                arc(x2, y2, injr*(zoom*100 + 100), injr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30), PIE)
            # other causes
            fill(100, 80, 80)
            if vo:
                arc(x2, y2, othr*(zoom*100 + 100), othr*(zoom*100 + 100),  deg + float(i-12)*radians(30), deg + float(i-11)*radians(30), PIE)
        i = i + 1
        
        textAlign(LEFT, LEFT)
        fill(255)
        textSize(30.0)
        text("Nightingale's Rose", 200, 700)
        textSize(20.0)
        text("Scroll with the mouse wheel to rotate ",200, 735)
        text("Click for zoom-in and out", 200, 760)
        text("Hold 'd' to see mortality rate due to Zymotic diseases", 200, 785)
        text("Hold 'i' to see mortality rate due to Wounds & injuries", 200, 810)
        text("Hold 'o' to see mortality rate due to All other causes", 200, 835)
        textSize(12.0)

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
