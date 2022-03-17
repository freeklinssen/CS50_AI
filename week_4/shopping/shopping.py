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
    
    evidence = list()
    labels = list()
    
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            temp = []
                
            if row["Revenue"] == "FALSE":
                labels.append(0)
            else:
                labels.append(1)
                
            temp.append(int(row["Administrative"]))
            temp.append(float(row["Administrative_Duration"]))
            temp.append(int(row["Informational"]))
            temp.append(float(row["Informational_Duration"]))
            temp.append(int(row["ProductRelated"]))
            temp.append(float(row["ProductRelated_Duration"]))
            temp.append(float(row["BounceRates"]))
            temp.append(float(row["ExitRates"]))
            temp.append(float(row["PageValues"]))
            temp.append(float(row["SpecialDay"]))
            if row["Month"] == "Jan":
                temp.append(0)
            elif row["Month"] == "Feb":
                temp.append(1)
            elif row["Month"] == "Mar":
                temp.append(2)
            elif row["Month"] == "Apr":
                temp.append(3)
            elif row["Month"] == "May":
                temp.append(4)
            elif row["Month"] == "June":
                temp.append(5)
            elif row["Month"] == "Jul":
                temp.append(6)
            elif row["Month"] == "Aug":
                temp.append(7)
            elif row["Month"] == "Sep":
                temp.append(8)
            elif row["Month"] == "Oct":
                temp.append(9)
            elif row["Month"] == "Nov":
                temp.append(10)
            elif row["Month"] == "Dec":
                temp.append(11)
            temp.append(int(row["OperatingSystems"]))
            temp.append(int(row["Browser"]))
            temp.append(int(row["Region"]))
            temp.append(int(row["TrafficType"]))
            if row["VisitorType"] == "Returning_Visitor":
                temp.append(1)
            else:
                temp.append(0)
            if row["Weekend"] == "TRUE":
                temp.append(1)
            else:
                temp.append(0)
                
            evidence.append(temp)
                
    return evidence, labels
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neighbor = KNeighborsClassifier(n_neighbors=1)
    neighbor.fit(evidence, labels)

    return neighbor


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0 
    true_positive = 0
    true_negative = 0
    
    for i in range(len(labels)):
        if labels[i] == 1:
            true_positive += 1
            if predictions[i] == 1:
                sensitivity += 1
        if labels[i] == 0:
            true_negative += 1
            if predictions[i] == 0:
                specificity += 1
        
    sensitivity = sensitivity / true_positive
    specificity = specificity / true_negative
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
