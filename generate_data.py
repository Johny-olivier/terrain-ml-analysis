import csv
import random
import numpy as np

# PARAMÈTRES
N = 1_000_000
file_name = "terrain_1M.csv"

communes = [
    "Ivato", "Itaosy", "Alasora", "Talatamaty",
    "Ambohidratrimo", "Analamahitsy", "Ivandry",
    "Ambatobe", "Ambohimangakely", "Ankadikely",
    "Sabotsy Namehana", "Ambohimalaza", "Andoharanofotsy",
    "Ambohijanaka"
]

papier_types = ["titre_borne", "karatany", "fifanolorana"]

# prix de base par commune (réaliste Madagascar)
base_price_commune = {
    "Ivato": 120000,
    "Itaosy": 80000,
    "Alasora": 90000,
    "Talatamaty": 110000,
    "Ambohidratrimo": 95000,
    "Analamahitsy": 150000,
    "Ivandry": 300000,
    "Ambatobe": 280000,
    "Ambohimangakely": 85000,
    "Ankadikely": 70000,
    "Sabotsy Namehana": 75000,
    "Ambohimalaza": 80000,
    "Andoharanofotsy": 100000,
    "Ambohijanaka": 65000
}

# GENERATION
with open(file_name, "w", newline="") as f:

    writer = csv.writer(f)

    # header
    writer.writerow([
        "commune",
        "prix_total",
        "surface",
        "acces_voiture",
        "distance_rn",
        "batissable",
        "distance_jirama",
        "type_papier"
    ])

    for i in range(N):

        commune = random.choice(communes)

        surface = int(np.random.normal(1500, 800))
        surface = max(100, min(surface, 10000))

        acces_voiture = random.choice([0, 1])
        batissable = random.choice([0, 1])

        distance_rn = abs(int(np.random.normal(500, 400)))
        distance_jirama = abs(int(np.random.normal(200, 150)))

        papier = random.choice(papier_types)

    
        # PRIX (LOGIQUE ÉCONOMIQUE)
    

        base = base_price_commune[commune]

        price_per_m2 = base

        # influence variables
        if acces_voiture:
            price_per_m2 *= 1.2

        if batissable:
            price_per_m2 *= 1.3

        price_per_m2 *= max(0.4, 1 - distance_rn / 5000)
        price_per_m2 *= max(0.5, 1 - distance_jirama / 3000)

        if papier == "titre_borne":
            price_per_m2 *= 1.3
        elif papier == "karatany":
            price_per_m2 *= 1.0
        else:
            price_per_m2 *= 0.8

        # bruit réaliste
        price_per_m2 *= random.uniform(0.9, 1.1)

        prix_total = int(price_per_m2 * surface)

        writer.writerow([
            commune,
            prix_total,
            surface,
            acces_voiture,
            distance_rn,
            batissable,
            distance_jirama,
            papier
        ])

        if i % 100000 == 0:
            print(f"{i} lignes générées...")
