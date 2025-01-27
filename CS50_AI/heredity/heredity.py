import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {
        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    probabilities = {
        person: {
            "gene": {2: 0, 1: 0, 0: 0},
            "trait": {True: 0, False: 0}
        }
        for person in people
    }

    names = set(people)
    for have_trait in powerset(names):
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)

    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    probability = 1

    for person in people:
        gene_count = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )
        has_trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        if mother is None and father is None:
            probability *= PROBS["gene"][gene_count]
        else:
            probabilities_from_parents = {}

            for parent in [mother, father]:
                parent_genes = (
                    2 if parent in two_genes else
                    1 if parent in one_gene else
                    0
                )
                if parent_genes == 2:
                    probabilities_from_parents[parent] = 1 - PROBS["mutation"]
                elif parent_genes == 1:
                    probabilities_from_parents[parent] = 0.5
                else:
                    probabilities_from_parents[parent] = PROBS["mutation"]

            if gene_count == 2:
                probability *= probabilities_from_parents[mother] * probabilities_from_parents[father]
            elif gene_count == 1:
                probability *= (
                    probabilities_from_parents[mother] * (1 - probabilities_from_parents[father]) +
                    (1 - probabilities_from_parents[mother]) * probabilities_from_parents[father]
                )
            else:
                probability *= (1 - probabilities_from_parents[mother]) * (1 - probabilities_from_parents[father])

        probability *= PROBS["trait"][gene_count][has_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        gene_count = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    for person in probabilities:
        for key in ["gene", "trait"]:
            total = sum(probabilities[person][key].values())
            for value in probabilities[person][key]:
                probabilities[person][key][value] /= total


if __name__ == "__main__":
    main()
