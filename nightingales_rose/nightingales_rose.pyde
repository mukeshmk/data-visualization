spin = 0
zoom = 0
x1 = 1300
y1 = 550
x2 = 350
y2 = 350

textx = 200
texty = 800

def setup():
    fullScreen()
    #size(1920, 1080)
    background(0, 0, 0)

# https://coolors.co/748291-c0c0c0-eff5f7-ffffff-1b6cd6
def draw():
    vd = vi = vo = True
    i = 0
    deg = float(spin)*radians(30)
    strokeWeight(2.0)
    background('#748291')
    table = loadTable("data/nightingale-rose.csv", "header")

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
                x = (x1 + (90)*cos(t))
                y = (y1 + (90)*sin(t))
            else:
                x = (x1 + (disr*51 + zoom*disr*51)*cos(t))
                y = (y1 + (disr*51 + zoom*disr*51)*sin(t))


            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            fill(255, 255, 255)
            textSize(20.0)
            # write text after translation
            text(mny.split(" ")[0], 0, 0)
            popMatrix()

            stroke(0)
            # diseases
            fill('#1B6CD6')
            if vd:
                arc(x1, y1, disr*(zoom*100 + 100), disr*(zoom*90 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30), PIE)
            # injuries
            fill('#c0c0c0')
            if vi:
                arc(x1, y1, injr*(zoom*100 + 100), injr*(zoom*90 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30), PIE)
            # other causes
            fill('#eff5f7')
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
            t = deg + float(i-6)*radians(30) + radians(15)

            # to calc point on the circle
            # X = Cx + (r * cos(angle))
            # Y = Cy + (r * sin(angle))
            x = (x2 + (150 + zoom*110)*cos(t))
            y = (y2 + (150 + zoom*110)*sin(t))
            
            if disr*50 < 50:
                x = (x2 + (80 + zoom*20)*cos(t))
                y = (y2 + (80 + zoom*20)*sin(t))
            elif injr > disr:
                x = (x2 + (injr*51 + zoom*injr*51 + 10)*cos(t))
                y = (y2 + (injr*51 + zoom*injr*51 + 10)*sin(t))
            else:
                x = (x2 + (disr*51 + zoom*disr*51 + 10)*cos(t))
                y = (y2 + (disr*51 + zoom*disr*51 + 10)*sin(t))

            pushMatrix()
            translate(x, y)
            rotate(t-PI/2)
            # align it to the centre after rotation
            textAlign(CENTER, CENTER)
            fill(255, 255, 255)
            # write text after translation
            textSize(20.0)
            text(mny.split(" ")[0], 0, 0)
            popMatrix()

            stroke(0)
            # diseases
            fill('#1B6CD6')
            if vd:
                arc(x2, y2, disr*(zoom*100 + 100), disr*(zoom*100 + 100),  deg + float(i-6)*radians(30), deg + float(i-5)*radians(30), PIE)
            # injuries
            fill('#c0c0c0')
            if vi:
                arc(x2, y2, injr*(zoom*100 + 100), injr*(zoom*100 + 100),  deg + float(i-6)*radians(30), deg + float(i-5)*radians(30), PIE)
            # other causes
            fill('#eff5f7')
            if vo:
                arc(x2, y2, othr*(zoom*100 + 100), othr*(zoom*100 + 100),  deg + float(i-6)*radians(30), deg + float(i-5)*radians(30), PIE)
        i = i + 1
        
        textAlign(LEFT, LEFT)
        textSize(50.0)
        fill('#453BF9')
        text("NIGHTINGALE'S ROSE", textx+450, texty-700)
        line(textx+450, texty-700+10, textx+960, texty-700+10)
        textSize(40.0)
        fill('#748291')
        rect(textx-20, texty-50, 550, 220)
        fill('#453BF9')
        text("INSTRUCTIONS:", textx, texty)
        line(textx, texty+5, textx+300, texty+5)
        textSize(20.0)
        fill(255)
        text("Scroll with the mouse wheel to rotate ",textx, texty+30)
        text("Click for zoom-in and out", textx, texty+60)
        text("Hold 'd' to see mortality rate due to Zymotic diseases", textx, texty+90)
        text("Hold 'i' to see mortality rate due to Wounds & injuries", textx, texty+120)
        text("Hold 'o' to see mortality rate due to All other causes", textx, texty+150)
        fill(0)
        circle(textx-10, texty+25, 7)
        circle(textx-10, texty+55, 7)
        circle(textx-10, texty+85, 7)
        circle(textx-10, texty+115, 7)
        circle(textx-10, texty+145, 7)
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
