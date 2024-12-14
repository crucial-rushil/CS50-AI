import csv
import itertools
import sys
import copy
import numpy as np

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
    probs = 1
    for person in people:
        #get the number of genes and if they have trait
        number_genes = 0
        has_trait = False
        if person in two_genes:
            number_genes = 2
        elif person in one_gene:
            number_genes = 1
        if person in have_trait:
            has_trait = True

        mom = people[person]["mother"]
        dad = people[person]["father"]

        if mom == None or dad == None:
            probs = probs * PROBS["gene"][number_genes] * PROBS["trait"][number_genes][has_trait]

        else:
            #get the number of genes parents have
            num_genes_mom = 0
            num_genes_dad = 0
            if mom in one_gene:
                num_genes_mom = 1
            elif mom in two_genes:
                num_genes_mom = 2
            if dad in one_gene:
                num_genes_dad = 1
            if dad in two_genes:
                num_genes_dad = 2

            #get probabilities
            prob_mom = 0
            prob_dad = 0
            if num_genes_mom == 0:
                prob_mom = PROBS["mutation"]
            elif num_genes_mom == 1:
                prob_mom = (1 - PROBS["mutation"])*0.5
            else:
                prob_mom = 1 - PROBS["mutation"]

            if num_genes_dad == 0:
                prob_dad = PROBS["mutation"]
            elif num_genes_mom == 1:
                prob_dad = (1 - PROBS["mutation"])*0.5
            else:
                prob_dad = 1 - PROBS["mutation"]

            #do calcuations
            if number_genes == 0:
                not_prob_mom_and_dad = (1 - prob_mom)*(1 - prob_dad)
                probs = probs * not_prob_mom_and_dad*PROBS["trait"][0][has_trait]

            elif number_genes == 1:
                prob_mom_not_dad = (prob_mom*(1 - prob_dad))
                prob_dad_not_mom = (prob_dad*(1 - prob_mom))
                probs = probs * (prob_mom_not_dad + prob_dad_not_mom)*PROBS["trait"][1][has_trait]

            elif number_genes == 2:
                prob_mom_and_dad = prob_dad*prob_mom
                probs = probs * prob_mom_and_dad*PROBS["trait"][2][has_trait]

    return probs

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        num_genes = 0
        has_trait = False
        if person in two_genes:
            num_genes = 2
        elif person in one_gene:
            num_genes = 1
        if person in have_trait:
            has_trait = True
        probabilities[person]["gene"][num_genes] += p
        probabilities[person]["trait"][has_trait] += p

    #raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        #normalize the gene distribution
        distrubtions = []
        for i in range(3):
            distrubtions.append(probabilities[person]["gene"][i])
        vals = np.array(distrubtions)
        vals = vals/vals.sum()

        for i in range(len(vals)):
            probabilities[person]["gene"][i] = vals[i]

        #normalize trait distribution
        trait_distributions = []
        trait_distributions.append(probabilities[person]["trait"][True])
        trait_distributions.append(probabilities[person]["trait"][False])
        values = np.array(trait_distributions)
        values = values/values.sum()
        probabilities[person]["trait"][True] = values[0]
        probabilities[person]["trait"][False] = values[1]


if __name__ == "__main__":
    main()
