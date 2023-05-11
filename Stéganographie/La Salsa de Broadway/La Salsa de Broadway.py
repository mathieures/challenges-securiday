import tkinter as tk


def get_pixel(image, coords):
    """
    Retourne un tuple de taille 3 contenant les
    valeurs RGB du pixel aux coordonnées données.
    """
    return image.get(*coords)


def set_pixel(image, coords, color):
    """
    Modifie le pixel aux coordonnées données
    pour qu'il corresponde à la couleur donnée.
    """
    r,g,b = color
    x,y = coords
    image.put(f"#{r:02x}{g:02x}{b:02x}", (x, y))


def flatten_pixels(pixels):
    """Retourne la liste des pixels/tuples de canaux aplatie"""
    return [byte for pixel in pixels for byte in pixel]

def decode_byte(flat_channels):
    """
    Décode un octet de la liste de canaux RGB donnée en
    paramètre en lisant le dernier bit de chaque canal
    de la liste de canaux aplatie donnée en paramètre.
    """
    # S'il n'y a pas assez de canaux, c'est la fin et on peut s'arrêter
    if len(flat_channels) < 8:
        return 0

    result = 0
    # bit_index est l'exact opposé de l'indice d'octet et vice-versa
    for bit_index in range(7, -1, -1):
        result += (flat_channels[7 - bit_index] & 1) << bit_index
        # print(f"{bit_index = }, canal : {flat_channels[7 - bit_index]}, "
        #       f"dernier bit : {flat_channels[7 - bit_index] & 1} => {result = }")

    return result


def write_message(image, message, dest_path):
    """Cache le message donné dans l'image"""

    len_message = len(message)
    width, height = image.width(), image.height()
    # S'il y a plus de bits dans le message que de canaux RGB dans l'image
    if len_message * 8 > width * height * 3:
        raise ValueError("Le message est trop long pour cette image ! "
                        f"(Message : {len_message} ; Image : {width * height})")

    message_img = image.copy()

    # peut-être remonter ça et utiliser les valeurs pour l'erreur
    necessary_bytes = len(message)
    necessary_channels = necessary_bytes * 8
    necessary_pixels, rest = divmod(necessary_channels, 3)
    if rest:
        necessary_pixels += 1
    
    # On calcule les coordonnées des pixels dont on aura besoin
    coords = []
    end_y, end_x = divmod(necessary_pixels, width)
    # print(f"{(end_x, end_y) = }")

    # On parcourt toutes les lignes complètes, puis la ligne restante
    for y in range(end_y + 1):
        for x in range(width):
            coords.append((x, y))

    # On récupère les pixels dont on aura besoin (paresseusement)
    pixels = (get_pixel(image, (x, y)) for (x, y) in coords)

    # On aplatit les pixels pour avoir la liste des canaux
    channels = flatten_pixels(pixels)

    bin_message = message.encode()
    channel_index = 0
    # On parcourt les caractères, donc octets, donc canaux
    for byte_index in range(necessary_bytes):
        char = bin_message[byte_index]
        # On vérifie chaque bit de l'octet actuel
        for bit_index in range(7, -1, -1):
            current_bit = (char >> bit_index) & 1
            channel = channels[channel_index]
            channel_bit = channel & 1 # On ne doit changer que le bit de poids faible

            # On ne change le canal que si les deux bits sont différents
            if channel_bit != current_bit:
                # Si channel_bit est à 1 alors on décrémente le canal
                if channel_bit:
                    channels[channel_index] -= 1
                # Sinon il est à 0 alors on incrémente le canal
                else:
                    channels[channel_index] += 1

            channel_index += 1

    # On a maintenant une liste de channels modifiés, on peut donc modifier l'image

    channel_index = 0
    for (x, y) in coords:
        # On prend les 3 prochains canaux que l'on a
        new_pixel = channels[channel_index:channel_index + 3]
        set_pixel(message_img, (x, y), new_pixel)

        channel_index += 3

    # On écrit l'message_img modifiée dans un fichier
    message_img.write(dest_path)


def read_message(image, bit_count=None):
    """Lit le message caché dans l'image"""
    bin_message = bytearray()

    width, height = image.width(), image.height()

    # On récupère tous les pixels (paresseusement)
    pixels = (get_pixel(image, (x, y)) for y in range(height) for x in range(width))

    if bit_count is None:
        bit_count = width * height * 3

    channels = flatten_pixels(pixels)[:bit_count]

    # On prend 8 canaux par 8 canaux, sans prendre en compte ceux
    # qui restent (aucun caractère ne peut être encodé dedans)
    decoded_byte = 0
    for channel_index in range(0, len(channels), 8):
        decoded_byte = decode_byte(channels[channel_index:channel_index + 8])
        bin_message.append(decoded_byte)
        # print(f"décodé : {chr(decoded_byte)}")

    return bin_message


def main():
    """La Salsa de Broadway"""

    # Création de l'image
    print("Création de l'image")

    img_path = "hackerman.png"
    secret_path = "La Salsa de Broadway.png"

    root = tk.Tk()

    img = tk.PhotoImage(master=root, file=img_path)

    flag = f"FLAG<{'merci' * 1000}>FLAG"
    # flag = "FLAG<zeufih8768ifuh>FLAG"
    print("Flag à cacher :", flag, end="\n\n")

    write_message(img, flag, secret_path)


    ## Récupération du flag
    print("Récupération du flag")

    flag_img = tk.PhotoImage(master=root, file=secret_path)
    raw_message = read_message(flag_img)
    # raw_message = read_message(flag_img, bit_count=256)

    # Connaissant la forme du flag, couper au bon endroit est facile
    print("Flag sans aucune information :",
          raw_message,
          end="\n\n")

    flag_delim = b">FLAG"
    print("Flag en connaissant le délimiteur :",
          raw_message[:raw_message.find(flag_delim) + len(flag_delim)].decode(),
          end="\n\n")

    print("Flag en connaissant la taille exacte :", raw_message[:len(flag)].decode())


    # ## Affichage côte à côte
    # print("Affichage côte à côte")

    # label_img = tk.Label(root, image=img)
    # label_img.pack(side=tk.LEFT)

    # label_secret = tk.Label(root, image=flag_img)
    # label_secret.pack(side=tk.RIGHT)
    # root.mainloop()


if __name__ == '__main__':
    main()