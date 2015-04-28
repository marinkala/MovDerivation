from PIL import Image

new_im=Image.new('RGB',(400,300*52))
count=0

for f in os.listdir(folder):
    im=Image.open(folder+f)
    im.thumbnail((400,400))
    new_im.paste(im,(0,300*count))
    count+=1
   
new_im.save('Trajectories.jpg')