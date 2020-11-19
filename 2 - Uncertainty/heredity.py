import csv
import itertools
import sys

from functools import reduce

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

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
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
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # sorting people from higher to lower generation
    persons = sort_people(people)

    # list to store calculated probabilities
    values = []

    for person in persons:
        # number of genes in this person father (for calculation purposes)
        if people[person]["father"] == None:
            father_genes = None
        elif people[person]["father"] in one_gene:
            father_genes = 1
        elif people[person]["father"] in two_genes:
            father_genes = 2
        else:
            father_genes = 0
        
        # number of genes in this person mother (for calculation purposes)
        if people[person]["mother"] == None:
            mother_genes = None
        elif people[person]["mother"] in one_gene:
            mother_genes = 1
        elif people[person]["mother"] in two_genes:
            mother_genes = 2
        else:
            mother_genes = 0
        
        # calculate no genes
        if person not in one_gene and person not in two_genes:
            #probabilities[person]["gene"][0] = calculate_no_genes(person, father_genes, mother_genes)
            values.append(calculate_no_genes(person, father_genes, mother_genes))
            if person in have_trait:
                # calculate trait given no genes
                #probabilities[person]["trait"][True] = PROBS["trait"][0][True]
                values.append(PROBS["trait"][0][True])
            else:
                # calculate no trait given no genes
                #probabilities[person]["trait"][False] = PROBS["trait"][0][False]
                values.append(PROBS["trait"][0][False])

        #calculate one gene
        elif person in one_gene:
            #probabilities[person]["gene"][1] = calculate_one_gene(person, father_genes, mother_genes)
            values.append(calculate_one_gene(person, father_genes, mother_genes))
            if person in have_trait:
                # calculate trait given one gene
                #probabilities[person]["trait"][True] = PROBS["trait"][1][True]
                values.append(PROBS["trait"][1][True])
            else:
                # calculate no trait given one gene
                #probabilities[person]["trait"][False] = PROBS["trait"][1][False]
                values.append(PROBS["trait"][1][False])

        #calculate two genes
        elif person in two_genes:
            #probabilities[person]["gene"][2] = calculate_two_genes(person, father_genes, mother_genes)
            values.append(calculate_two_genes(person, father_genes, mother_genes))
            if person in have_trait:
                # calculate trait given two genes
                #probabilities[person]["trait"][True] = PROBS["trait"][2][True]
                values.append(PROBS["trait"][2][True])
            else:
                # calculate no trait given two genes
                #probabilities[person]["trait"][False] = PROBS["trait"][2][False]
                values.append(PROBS["trait"][2][False])
    
    # multiply all probabilities and return value
    return reduce(multiply, values)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene0 = probabilities[person]["gene"][0] / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        gene1 = probabilities[person]["gene"][1] / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        gene2 = probabilities[person]["gene"][2] / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        probabilities[person]["gene"][0] = gene0
        probabilities[person]["gene"][1] = gene1
        probabilities[person]["gene"][2] = gene2
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
        probabilities[person]["trait"][False] = 1 - probabilities[person]["trait"][True]


def sort_people(people):
    """
    Return a list of people sorted by generation
    """
    sorted_people = []

    while len(sorted_people) < len(people):
        if not sorted_people:
            for person in people:
                if people[person]["father"] == None:
                    sorted_people.append(person)
        else:
            for person in people:
                if people not in sorted_people:
                    if people[person]["father"] in sorted_people and people[person]["mother"] in sorted_people:
                        sorted_people.append(person)

    return sorted_people


def calculate_no_genes(person, father_genes, mother_genes):
    """
    Calculate the probabilities of person having no genes,
    given parents genes
    """
    if father_genes == None:
        # if no parents, return unconditional probability
        return PROBS["gene"][0]
    else:
        # parents have no genes
        if father_genes == 0 and mother_genes == 0:
            return 1 - PROBS["mutation"] * 1 - PROBS["mutation"]
        # one parent have no genes, the other have 1 gene
        elif (father_genes == 0 and mother_genes == 1) or (father_genes == 1 and mother_genes == 0):
            return 1 - PROBS["mutation"] * 1 / 2 - PROBS["mutation"]
        # one parent have no genes, the other have 2 genes
        elif (father_genes == 0 and mother_genes == 2) or (father_genes == 2 and mother_genes == 0):
            return 1 - PROBS["mutation"] * PROBS["mutation"]
        # both parents have 1 gene
        elif father_genes == 1 and mother_genes == 1:
            return 1 / 2 - PROBS["mutation"] * 1 / 2 * PROBS["mutation"]
        # one parent have 1 gene, the other have 2 genes
        elif (father_genes == 1 and mother_genes == 2) or (father_genes == 2 and mother_genes == 1):
            return 1 / 2 - PROBS["mutation"] * PROBS["mutation"]
        # both parents have 2 genes
        else:
            return PROBS["mutation"] * PROBS["mutation"]


def calculate_one_gene(person, father_genes, mother_genes):
    """
    Calculate the probabilities of person having one gene,
    given parents genes
    """
    if father_genes == None:
        # if no parents, return unconditional probability
        return PROBS["gene"][1]
    else:
        # parents have no genes
        if father_genes == 0 and mother_genes == 0:
            return (PROBS["mutation"] * 1 - PROBS["mutation"]) + (1 - PROBS["mutation"] * PROBS["mutation"])
        # one parent have no genes, the other have 1 gene
        elif (father_genes == 0 and mother_genes == 1) or (father_genes == 1 and mother_genes == 0):
            return PROBS["mutation"] * 1 / 2 - PROBS["mutation"] + (1 - PROBS["mutation"] * 1 / 2 + PROBS["mutation"])
        # one parent have no genes, the other have 2 genes
        elif (father_genes == 0 and mother_genes == 2) or (father_genes == 2 and mother_genes == 0):
            return (PROBS["mutation"] * PROBS["mutation"]) + (1 - PROBS["mutation"] * 1 - PROBS["mutation"])
        # both parents have 1 gene
        elif father_genes == 1 and mother_genes == 1:
            return (1 / 2 + PROBS["mutation"] * 1 / 2 - PROBS["mutation"]) + (1 / 2 - PROBS["mutation"] * 1 / 2 + PROBS["mutation"])
        # one parent have 1 gene, the other have 2 genes
        elif (father_genes == 1 and mother_genes == 2) or (father_genes == 2 and mother_genes == 1):
            return (1 / 2 + PROBS["mutation"] * PROBS["mutation"]) + (1 / 2 - PROBS["mutation"] * 1 - PROBS["mutation"])
        # both parents have 2 genes
        else:
            return (1 - PROBS["mutation"] * PROBS["mutation"]) + (PROBS["mutation"] * 1 - PROBS["mutation"])


def calculate_two_genes(person, father_genes, mother_genes):
    """
    Calculate the probabilities of person having no genes,
    given parents genes
    """
    if father_genes == None:
        # if no parents, return unconditional probability
        return PROBS["gene"][2]
    else:
        # parents have no genes
        if father_genes == 0 and mother_genes == 0:
            return PROBS["mutation"] * PROBS["mutation"]
        # one parent have no genes, the other have 1 gene
        elif (father_genes == 0 and mother_genes == 1) or (father_genes == 1 and mother_genes == 0):
            return PROBS["mutation"] * 1 / 2 + PROBS["mutation"]
        # one parent have no genes, the other have 2 genes
        elif (father_genes == 0 and mother_genes == 2) or (father_genes == 2 and mother_genes == 0):
            return PROBS["mutation"] * 1 - PROBS["mutation"]
        # both parents have 1 gene
        elif father_genes == 1 and mother_genes == 1:
            return 1 / 2 + PROBS["mutation"] * 1 / 2 + PROBS["mutation"]
        # one parent have 1 gene, the other have 2 genes
        elif (father_genes == 1 and mother_genes == 2) or (father_genes == 2 and mother_genes == 1):
            return 1 / 2 + PROBS["mutation"] * 1 - PROBS["mutation"]
        # both parents have 2 genes
        else:
            return 1 - PROBS["mutation"] * 1 - PROBS["mutation"]


def multiply(a, b):
    return a * b


if __name__ == "__main__":
    main()
