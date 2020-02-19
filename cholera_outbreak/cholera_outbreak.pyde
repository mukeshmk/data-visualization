def setup():
    size(1000, 911)
    img = loadImage("mapclean.jpg")
    background(0)
    image(img, 0, 0)

def draw():
    table = loadTable("snow_pixelcoords.csv", "header")
    for row in table.rows():
        count = row.getInt("count")
        x_screen = row.getFloat("x_screen")
        y_screen = row.getFloat("y_screen")
        if count == -999:
            fill(0, 0, 256)
            rect(x_screen, y_screen, 10, 10)
        else:
            fill(256, 0, 0)
            circle(x_screen, y_screen, count*2)
