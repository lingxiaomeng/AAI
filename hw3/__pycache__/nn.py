import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, input_dim):
        super(Net, self).__init__()

        # Our network consists of 3 layers. 1 input, 1 hidden and 1 output layer
        # This applies Linear transformation to input data.
        self.fc1 = nn.Linear(input_dim, 30)

        # This applies linear transformation to produce output data
        self.fc2 = nn.Linear(30, 60)
        self.fc3 = nn.Linear(60, 30)
        self.fc4 = nn.Linear(30, 30)
        self.o = nn.Linear(30, 2)

    # This must be implemented
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = F.dropout(x, 0.4)

        x = self.fc3(x)
        x = F.relu(x)
        x = self.o(x)
        return x

    # This function takes an input and predicts the class, (0 or 1)
    def predict(self, x):
        # Apply softmax to output
        pred = F.softmax(self.forward(x))
        ans = []
        for t in pred:
            if t[0] > t[1]:
                ans.append(0)
            else:
                ans.append(1)
        return torch.tensor(ans).cuda()


class NNClassifier:
    def __init__(self, epochs) -> None:
        self.model = None
        self.epochs = epochs

    def fit(self, X, y):
        input_dim = X.shape[1]
        model = Net(input_dim=input_dim).cuda()
        # Define loss criterion
        criterion = nn.CrossEntropyLoss().cuda()
        # Define the optimizer
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

        X = torch.from_numpy(X).type(torch.cuda.FloatTensor)
        y = torch.from_numpy(y).type(torch.cuda.LongTensor)

        # Number of epochs
        epochs = self.epochs
        # List to store losses
        losses = []
        for i in range(epochs):
            # Precit the output for Given input
            y_pred = model.forward(X)
            # Compute Cross entropy loss
            loss = criterion(y_pred, y)
            # Add loss to the list
            losses.append(loss.item())
            # Clear the previous gradients
            optimizer.zero_grad()
            # Compute gradients
            loss.backward()
            # Adjust weights
            optimizer.step()

            # print("epoch %d train loss: %.5f" % (i, loss.item()))
        self.model = model
        return self

    def predict(self,X):
        X = torch.from_numpy(X).type(torch.cuda.FloatTensor)
        with torch.no_grad():
            y = self.model.predict(X)
        return y.cpu().numpy()
        


if __name__ == "__main__":
    traindata = load_txt('./traindata.txt')
    trainlabel = load_txt('trainlabel.txt')
    trainlabel[trainlabel >= 1] = 1
    testdata = load_txt('./testdata.txt')
    testlabel = load_txt('original_testdata_label.csv')
    testlabel[testlabel >= 1] = 1

    print(trainlabel)
    print(testlabel)

    traindata_size = len(trainlabel)
    testdata_size = len(testlabel)

    # Initialize the model
    model = Net(input_dim=13).cuda()
    # Define loss criterion
    criterion = nn.CrossEntropyLoss().cuda()
    # Define the optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

    X = torch.from_numpy(traindata).type(torch.cuda.FloatTensor)
    y = torch.from_numpy(trainlabel).type(torch.cuda.LongTensor)
    # y = F.one_hot(y).to('cuda')

    X_test = torch.from_numpy(testdata).type(torch.cuda.FloatTensor)
    y_test = torch.from_numpy(testlabel).type(torch.cuda.LongTensor)
    # y_test = F.one_hot(y).to('cuda')

    # Number of epochs
    epochs = 1000
    # List to store losses
    losses = []
    for i in range(epochs):
        # Precit the output for Given input
        y_pred = model.forward(X)
        y_pred_test = model.forward(X_test)
        # print(y)
        # print(y_pred)

        # Compute Cross entropy loss
        loss = criterion(y_pred, y)
        test_loss = criterion(y_pred_test, y_test)

        train_acc = torch.sum(model.predict(X) == y)/traindata_size
        test_acc = torch.sum(model.predict(X_test) == y_test)/testdata_size

        # Add loss to the list
        losses.append(loss.item())
        # Clear the previous gradients
        optimizer.zero_grad()
        # Compute gradients
        loss.backward()
        # Adjust weights
        optimizer.step()

        print("epoch %d train loss: %.5f, train acc:%.5f test loss: %.5f test acc: %.5f" % (
            i, loss.item(), train_acc, test_loss.item(), test_acc))

y_test = load_txt('original_testdata_label.csv')
y_test[y_test>=1] = 1
dt = DecisionTreeClassifier(random_state=0)
dt.fit(X, y)
y_pred = dt.predict(X_test)
print(accuracy_score(y_test, y_pred))

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X, y)
y_pred = knn.predict(X_test)
print(accuracy_score(y_test, y_pred))

svm = SVC(kernel='linear', random_state=0)
svm.fit(X, y)
y_pred = svm.predict(X_test)
print(accuracy_score(y_test, y_pred))

nn = MLPClassifier(hidden_layer_sizes=(
    10, 10), max_iter=10000, activation="relu",random_state=0)
nn.fit(X, y)
y_pred = nn.predict(X_test)
print(accuracy_score(y_test, y_pred))

estimators = [('DecisionTree', dt),
              ('knn', knn),
              ('svm', svm),
              ('nn', nn)]
ensemble = StackingClassifier(estimators=estimators)
ensemble.fit(X, y)
y_pred = ensemble.predict(X_test)
print(accuracy_score(y_test, y_pred))