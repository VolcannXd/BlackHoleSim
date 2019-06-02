import math
import PIL.Image

print('[LOG] Opening programm...')

Width = 640
Height = 480
Scale = 1

change = input('Change default IMG settings (' + str(Width) + 'x' + str(Height) + ') ? (y/ n) : ')

if change == 'y' :
    Width = int(input('IMG Width : '))
    Height = int(input('IMG Height : '))
    Scale = int(input('IMG Scale : '))

outFile = str(input("Out file name : "))
filepath = str(input('SkySphere file name (if different) : '))
if filepath == '' : filepath = 'img_background_01.jpg';

background = PIL.Image.open(filepath)
background_im = background.convert('RGB')


print('[LOG] Loading Background Image')
background_im.show()
iWidth = background.size[0]
iHeight = background.size[1]

print('[LOG] iWidth = ' + str(iWidth) + " | iHeight = " + str(iHeight))

# ENV VARIABLES SETUP
hfov = float(input("HFOV (DFLT : 1.2) : "))
radius = float(input("RADIUS (DFLT : 0.1) : "))
dt = float(input("dt (DFLT : 0.1) : "))
MaxDistance = float(input("MAX PHOTON DISTANCE (DFLT : 3) : "))

Pixels = [0] * (Width * Height)
arraySize = Width * Height

n = 0
radDistL = 0
iPhoton = 0
jPhoton = 0
print("[LOG] Starting Simulation....")
for i in range (0, Width) :
    for j in range (0, Height) :
        alpha =  math.sqrt(math.pow(i - Width / 2, 2) + math.pow(Height / 2 - j, 2)) * hfov / Width # math.sqrt(math.pow(i - Width / 2, 2) + math.pow(Height / 2 + j, 2)) * hfov / Width
        beta = math.atan2(Height / 2 - j, i - Width / 2)
        x = 1; y = 0; t = 0 # START PHOTON 4D MAPPING
        vx = - math.cos(alpha); vy = math.sin(alpha)

        while (math.sqrt(x*x + y*y) < MaxDistance and math.sqrt(x*x + y*y) > radius) :
            t = t + dt

            x = x + dt * vx; y = y + dt * vy
            radDistL = math.sqrt(x*x + y*y)

            dphi = (x * vy - y * vx) / radDistL / radDistL
            ax = (-3 / 2) * radius * (dphi * dphi) * x / radDistL
            ay = (-3 / 2) * radius * (dphi * dphi) * y / radDistL
            vx = vx + dt * ax; vy = vy + dt * ay

        if radDistL >= MaxDistance :
            pAlpha = math.atan2(y, 1 - x)
            iPhoton = iWidth / 2 + pAlpha * math.cos(beta) * iWidth / math.pi / 2
            jPhoton = iHeight / 2 - pAlpha * math.sin(beta) * iHeight / math.pi

            iPhoton = round(iPhoton)
            jPhoton = round(jPhoton)

            # Clamping pixels to prevent 'out of bounds'
            while iPhoton < 0 : iPhoton = iPhoton + iWidth;
            while iPhoton >= iWidth : iPhoton = iPhoton - iWidth;
            while jPhoton < 0 : jPhoton = jPhoton + iHeight;
            while jPhoton >= iHeight : jPhoton = jPhoton - iHeight;

            color = background_im.getpixel((iPhoton, jPhoton))

            prct = (n / arraySize) * 100
            print("[SIMULATION STATE] " + str(round(prct, 3)) +"%")
            Pixels[n] = color
        else :
            Pixels[n] = (0, 0, 0) # Display Black pixels if --> Rs

        n = n + 1

image = PIL.Image.new('RGB', (Width, Height))
pix = image.load()

# Assign every pixels of the calculation to the output image
n = 0
for x in range(Width) :
    for y in range(Height) :
        pix[x, y] = Pixels[n]; n = n + 1

image.save(outFile + '.png', "PNG")
output = PIL.Image.open(outFile + '.png')
output.show()
print("[LOG] Calculations has been ended succesfuly :) !")
