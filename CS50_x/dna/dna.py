import csv
import sys

def longest_match(sequence, subsequence):
    """Returnează numărul maxim de repetări consecutive ale unui STR într-o secvență."""
    longest_run = 0
    subseq_length = len(subsequence)
    seq_length = len(sequence)

    for i in range(seq_length):
        count = 0
        while sequence[i + count * subseq_length : i + (count + 1) * subseq_length] == subsequence:
            count += 1
        longest_run = max(longest_run, count)

    return longest_run

def main():
    # Verifică dacă sunt furnizate 2 argumente de linie de comandă
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # Citește fișierul CSV
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    # Citește fișierul de secvență ADN
    with open(sys.argv[2], "r") as file:
        dna_sequence = file.read()

    # Extrage lista STR-urilor din fișierul CSV
    str_list = list(database[0].keys())[1:]

    # Calculează numărul maxim de repetări consecutive pentru fiecare STR în secvența ADN
    dna_str_counts = {}
    for STR in str_list:
        dna_str_counts[STR] = longest_match(dna_sequence, STR)

    # Caută o potrivire în baza de date
    for person in database:
        match = True
        for STR in str_list:
            if int(person[STR]) != dna_str_counts[STR]:
                match = False
                break
        if match:
            print(person["name"])
            return

    # Dacă nu există potrivire
    print("No match")

# Apelează funcția principală
if __name__ == "__main__":
    main()
