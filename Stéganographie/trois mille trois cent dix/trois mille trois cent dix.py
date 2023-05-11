TABLE = {
    "A": "2",
    "B": "22",
    "C": "222",
    "D": "3",
    "E": "33",
    "F": "333",
    "G": "4",
    "H": "44",
    "I": "444",
    "J": "5",
    "K": "55",
    "L": "555",
    "M": "6",
    "N": "66",
    "O": "666",
    "P": "7",
    "Q": "77",
    "R": "777",
    "S": "7777",
    "T": "8",
    "U": "88",
    "V": "888",
    "W": "9",
    "X": "99",
    "Y": "999",
    "Z": "9999"
}


def to_3310(message):
    """Renvoie le message encodé grâce à la table de correspondance."""
    return "-".join(TABLE.get(c.upper(), c) for c in message if c != " ")


def from_3310(message):
    """Renvoie le message décodé grâce à la table de correspondance inversée."""
    reversed_table = dict((val, key) for key, val in TABLE.items())
    return "".join(reversed_table.get(c, c) for c in message.split("-"))


def main():
    flag = "FLAG<NOKIATOUJOURSMIEUXQUAPPLE>FLAG"

    print("Flag à cacher :", flag)

    # Création du secret
    print("Création du secret")

    secret = to_3310(flag)

    print("Dans la console")
    print(secret)

    print("Dans un fichier")
    with open("trois mille trois cent dix.txt", "w", encoding="utf-8") as file:
        file.write(secret)


    # Décodage du secret
    print("Décodage du secret")

    decoded_secret = from_3310(secret)
    print(decoded_secret)


if __name__ == '__main__':
    main()