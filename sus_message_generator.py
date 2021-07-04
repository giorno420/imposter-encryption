from PIL import Image, ImageDraw, ImageFont
import random, os

master_im = Image.open("imposter.jpg")
master_string = "when the imposter is sus!"


# the y coordinate for where the text and the face split
y_coord_split = 22

master_x_dict = {
    "w": [[7,29]],
    "h": [[29,43], [83,98]],
    "e": [[43,56], [98,111], [192,205]],
    "n": [[56,69]],
    " ": [[69,75], [111,116], [213,220], [238,244]],
    "t": [[75,83], [183,192]],
    "i": [[116,122], [220,225]],
    "m": [[122,143]],
    "p": [[143,157]],
    "o": [[157,171]],
    "s": [[171,183], [225,238], [244,257], [270,283]],
    "r": [[205,213]],
    "u": [[257,270]],
    "!": [[282,289]],
    "😳": [[289,312]],
}

# [should flip over x axis, should flip over y axis], [x1, x2]
bootleg_x_dict = {
    "a": [[True, False], [146, 155]],
    "q": [[True, False], [143, 155]],
    "b": [[False, True], [143, 157]],
    "d": [[True, True], [143, 157]],
    "c": [[False, False], [157,167]]
}

# list of all avalable charecters
master_char_list = list(master_x_dict.keys()) + list(bootleg_x_dict.keys())


# get input string
input_string = input("Your message here: ").lower()
input_string = input_string.replace(":flushed:", "😳")

# font creation for cheating mode
font_path = (os.getcwd() + "\\fonts\\arial.ttf")
font = ImageFont.truetype(font_path, 13)

# get yes/no and return as true/false
def get_user_input_bool(question_string):
    user_answer = input(question_string)
    while user_answer not in ["y", "n"]:
        user_answer = input(question_string)
    
    user_answer = True if user_answer == "y" else False
    
    return user_answer

# yes or no cypher mode? no text, only jerma barcode
cypher_mode = get_user_input_bool("Would you like to use cypher mode (y/n):")


# yes or no cheating mode? Generate unsupported charecters with a random scan line
cheating_mode = False
for char in input_string:
    if char not in master_char_list:
        cheating_mode = get_user_input_bool("It looks like your using characters not in the default character set, would you like to activate cheating mode? (y/n):")
        break

# cypher warning
change = False
if cheating_mode and cypher_mode:
    print("""\nUsing cypher mode and cheating mode together is not reccomended due to
the fact that the cheating mode uses a random part of the image, hence making it
impossible to figure out the letter used""")
    change_mode = get_user_input_bool("Would you like to disable cypher mode? (y/n)")
    if change_mode:
        cypher_mode = False

final_image = Image.new('RGB', (len(input_string)*12, master_im.height))

# keeps track of the total width of the image, the width of each strip is added at the end of each loop
total_width = 0

for char in input_string:
    if char in master_x_dict.keys():
        x_coords = random.choice(master_x_dict[char])

        letter = master_im.crop((x_coords[0], 0, x_coords[1], y_coord_split))
        face = master_im.crop((x_coords[0], y_coord_split, x_coords[1], master_im.height))
        
    elif char in bootleg_x_dict.keys():   
        x_coords = bootleg_x_dict[char][1]
        
        letter = master_im.crop((x_coords[0], 0, x_coords[1], y_coord_split))
        face = master_im.crop((x_coords[0], y_coord_split, x_coords[1], master_im.height))

        # flip over x?
        if bootleg_x_dict[char][0][0]:
            letter = letter.transpose(Image.FLIP_LEFT_RIGHT)
            face = face.transpose(Image.FLIP_LEFT_RIGHT)

        # flip over y?
        if bootleg_x_dict[char][0][1]:
            letter = letter.transpose(Image.FLIP_TOP_BOTTOM)
            face = face.transpose(Image.FLIP_TOP_BOTTOM)

        # epic edge case
        if char == "a":
            draw = ImageDraw.Draw(letter)
            draw.rectangle([5, 13, 8, 16], fill=(255,255,255,255))
        
    elif cheating_mode:
        random_x = random.randint(0, master_im.width-13)
        scan_line_x_coords = [random_x, random_x+12]
        
        face = master_im.crop((scan_line_x_coords[0], y_coord_split, scan_line_x_coords[1], master_im.height))

        # create new blank letter template
        letter = Image.new('RGB', (face.width, y_coord_split))
        # draw white rectangle background and the letter
        draw = ImageDraw.Draw(letter)
        draw.rectangle([0, 0, letter.width, letter.height], fill=(255,255,255,255))
        draw.text((0, 0), char, font=font, fill=(0,0,0,255))
        # stretch the letter to match the natural stretch of the original image
        letter = letter.resize((int(letter.width*1.75), letter.height))
        letter = letter.crop((0, 0, face.width, letter.height))

    else:
        print(char + ": LETTER NOT SUPPORTED")
        continue

    # combine letter and face then paste it into the final image
    scan_line = Image.new('RGB', (letter.width, letter.height + face.height))
    scan_line.paste(letter, (0, 0))
    scan_line.paste(face, (0, y_coord_split))
    final_image.paste(scan_line, (total_width, 0))

    total_width += scan_line.width
    
if cypher_mode:
    final_image = final_image.crop((0, y_coord_split, final_image.width, final_image.height))

final_image.show()
