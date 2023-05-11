from base64 import b64encode, b64decode


def main():
    src = "ch3.pcap"
    dest = "Authentification basique.pcap"

    user = "usertest"
    flag = "i<3_hack"

    with open(src, "rb") as file:
        content = file.read()

    # Remplacement des données
    print("Remplacement des données")

    content = content.replace(b"twitter",
                              b"example")
    content = content.replace(b"dXNlcnRlc3Q6cGFzc3dvcmQ=",
                              b64encode(bytes(f"{user}:{flag}", encoding="utf-8")))

    # Création du fichier pcap
    print("Création du fichier pcap")

    with open(dest, "wb") as file:
        file.write(content)

    # Extraction du flag
    print("Extraction du flag")
    with open(dest, "rb") as file:
        content = file.read()

    # print("Contenu non modifié :")
    # print(content)

    start = content.index(b"Basic") + 6 # On enlève l'espace également

    # print("Recherche dans la sous-chaîne :")
    # print(content[start:])

    # La chaine en base64 est suivie d'un retour chariot
    end = content[start:].index(b"\r") + start

    print("Trouvé :")
    code = content[start:end]
    print(code)

    decode = b64decode(code)
    print(f"Flag : {decode.split(b':')[1].decode()}")


if __name__ == '__main__':
    main()