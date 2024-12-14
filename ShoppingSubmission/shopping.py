import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.DictReader(f)
        evidence = []
        labels = []

        months = {
            "January": 0,
            "February": 1,
            "March": 2,
            "April": 3,
            "May": 4,
            "June": 5,
            "July": 6,
            "August": 7,
            "September": 8,
            "October": 9,
            "November": 10,
            "December": 11
        }

        for row in reader:
            ind_row = []

            #integer & float casting
            ind_row.append(int(row["Administrative"]))
            ind_row.append(float(row["Administrative_Duration"]))
            ind_row.append(int(row["Informational"]))
            ind_row.append(float(row["Informational_Duration"]))
            ind_row.append(int(row["ProductRelated"]))
            ind_row.append(float(row["ProductRelated_Duration"]))
            ind_row.append(float(row["BounceRates"]))
            ind_row.append(float(row["ExitRates"]))
            ind_row.append(float(row["PageValues"]))
            ind_row.append(float(row["SpecialDay"]))

            #Month
            ind_row.extend(months[item] for item in months.keys() if row["Month"] in item)

            ind_row.append(int(row["OperatingSystems"]))
            ind_row.append(int(row["Browser"]))
            ind_row.append(int(row["Region"]))
            ind_row.append(int(row["TrafficType"]))

            #visitor
            ind_row.append(1 if row["VisitorType"] == 'Returning_Visitor' else 0)

            #Weekend
            ind_row.append(1 if row["Weekend"] is True else 0)

            evidence.append(ind_row)
            labels.append(1 if row["Revenue"] is True else 0)

        return (evidence,labels)
    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    X_training = evidence
    Y_training = labels
    model.fit(X_training,Y_training)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    sensitivity_count = 0
    specificity = 0
    specificity_count = 0

    for i in range(len(labels)):
        if labels[i] == 1:
            sensitivity_count += 1
            if labels[i] == predictions[i]:
                sensitivity += 1
        elif labels[i] == 0:
            specificity_count += 1
            if labels[i] == predictions[i]:
                specificity +=1

    sensitivity = sensitivity/sensitivity_count
    specificity = specificity/specificity_count

    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
