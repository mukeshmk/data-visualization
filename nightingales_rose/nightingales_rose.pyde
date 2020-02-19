rotate = 0
clicked = 0

def setup():
    size(1800, 900)
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
            arc(500, 500, disr*(clicked*100 + 100), disr*(clicked*100 + 100),  deg + float(i)*radians(30), deg + float(i+1)*radians(30))
        else:
            j = i - 12
            # scale down the value
            disr = disr/100
            arc(1300, 500, disr*(clicked*100 + 100), disr*(clicked*100 + 100),  deg + float(j)*radians(30), deg + float(j+1)*radians(30))
        
def mouseWheel(event):
    global rotate 
    rotate += event.getCount()
    # keep value in range
    rotate = rotate % 12
    
def mouseClicked(): 
    global clicked
    if clicked == 0:
        clicked = 1
    else:
        clicked = 0
