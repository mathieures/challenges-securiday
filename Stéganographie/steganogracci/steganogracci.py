def get_file_bytes(filename: str) -> bytes:
    """Retourne le contenu du fichier dans un objet bytes."""
    with open(filename, "rb") as file:
        return file.read()


def fibonacci(number: int):
    """Retourne le n-ème terme de la suite de fibonacci"""
    if number < 2:
        return number
    return fibonacci(number - 1) + fibonacci(number - 2)


def hide_image(src: str, dst:str, secret: str):
    """
    Cache l'image 'secret' dans l'image 'dst'
    en la concaténant à la fin de l'image 'src'.
    """
    content_src = get_file_bytes(src)
    content_secret = get_file_bytes(secret)
    result = content_src + content_secret
    with open(dst, "wb") as file:
        file.write(result)


def extract_duplicate(src: str, dst: str):
    """
    Extrait l'image cachée concaténée à la fin d'une autre.
    Il faut que les deux images fassent la même taille.
    """
    content_src = get_file_bytes(src)
    original_length = len(content_src) // 2
    with open(dst, "wb") as file:
        file.write(content_src[original_length:])


def write_message(src: str, dst: str, message: str, start: int):
    """
    Duplique l'image dont le nom de fichier
    est passé en paramètre puis cache le
    message donné dans cette seconde image.
    Le paramètre 'start' est présent car les
    premiers nombres de la suite de fibonacci
    sont 0, 1 et 1, ce qui écrase un caractère.
    """
    if not message:
        raise ValueError("Le message est vide")
    mutable_content = list(get_file_bytes(src))

    sequence = [fibonacci(i) for i in range(start, len(message) + start)]
    if sequence[-1] > len(mutable_content):
        raise RuntimeError("Le message est trop long pour cette image !")

    for i, letter in enumerate(message):
        mutable_content[sequence[i]] = ord(letter)

    with open(dst, "wb") as file:
        file.write(bytes(mutable_content))


def read_message(filename: str, out=None):
    """
    Lit un message caché dans une image en affichant
    les octets correspondants aux nombres de
    la suite de fibonacci. Parcourt le fichier entier
    car on ne connaît pas la longueur du message.
    """
    content = get_file_bytes(filename)

    # On sauvegarde le dernier nombre de fibonacci calculé
    current_fib = 0
    i = 1

    message = []
    while current_fib < len(content):
        message.append(chr(content[current_fib]))
        current_fib = fibonacci(i)
        i += 1

    # Si 'out' est précisé alors on écrit dans le fichier
    if out:
        with open(out, "w", encoding="utf-8") as file:
            print("".join(message), file=file)
    else:
        print("".join(message))


def main():
    """Crée l'image du défi puis résout ce dernier."""

    flag = "FLAG<ufetdihsigu>FLAG"
    original_image = "steganogracci.jpg"
    final_image = "flag_steganogracci.jpg"

    hidden_image = original_image
    message_image = original_image
    # hidden_image = f"hidden_{original_image}"
    # message_image = f"message_{original_image}"

    ## Tests
    # print(get_file_bytes(original_image))
    # print([fibonacci(i) for i in range(10)])
    # write_message(original_image, message_image, flag, start=3)
    # read_message(message_image)
    # hide_image(original_image, final_image, hidden_image)
    # extracted_image = f"extracted_{original_image}"
    # extract_duplicate(hidden_image, extracted_image)

    # Création de l'image contenant le flag
    print("Création de l'image contenant le flag")

    # Écriture du message dans l'image originale
    write_message(src=original_image, dst=hidden_image, message=flag, start=3)

    # Dissimulation de l'image avec le message à la fin de l'image originale
    hide_image(src=original_image, dst=final_image, secret=hidden_image)

    # Extraction du flag
    print("Extraction du flag")

    extract_duplicate(src=final_image, dst=message_image)

    print("Dans la console")
    read_message(message_image)

    # print("Dans un fichier")
    # read_message(message_image, out="flag.txt")
    # with open("flag.txt", "r", encoding="utf-8") as file:
    #     print(file.read())


if __name__ == '__main__':
    main()