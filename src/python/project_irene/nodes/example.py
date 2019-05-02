# QUANTUMBLACK CONFIDENTIAL
#
# Copyright (c) 2016 - present QuantumBlack Visual Analytics Ltd. All
# Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of
# QuantumBlack Visual Analytics Ltd. and its suppliers, if any. The
# intellectual and technical concepts contained herein are proprietary to
# QuantumBlack Visual Analytics Ltd. and its suppliers and may be covered
# by UK and Foreign Patents, patents in process, and are protected by trade
# secret or copyright law. Dissemination of this information or
# reproduction of this material is strictly forbidden unless prior written
# permission is obtained from QuantumBlack Visual Analytics Ltd.

"""Example code for the nodes in the example pipelines. This code is meant
just for illustrating basic KernelAI features.

PLEASE DELETE THIS FILE ONCE YOU START WORKING ON YOUR OWN PROJECT!
"""
# pylint: disable=invalid-name, too-many-locals, invalid-slice-index
from typing import Dict, Any

import logging

import numpy as np
import pandas as pd


def split_data(data: pd.DataFrame,
               parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Node for splitting the classical Iris data set into training and test
    sets, each split into features and labels.
    The split ratio parameter is taken from conf/project/parameters.yml.
    The data and the parameters will be loaded and provided to your function
    automatically when the pipelines is executed and it is time to run this node.
    """
    test_data_ratio = parameters['example_test_data_ratio']
    data.columns = ['sepal_length', 'sepal_width',
                    'petal_length', 'petal_width',
                    'target']
    classes = sorted(data['target'].unique())
    # One-hot encoding for the target variable
    data = pd.get_dummies(data, columns=['target'], prefix='', prefix_sep='')

    # Shuffle all the data
    data = data.sample(frac=1).reset_index(drop=True)

    # Split to training and testing data
    n = data.shape[0]
    n_test = int(n * test_data_ratio)
    training_data = data.iloc[n_test:, :].reset_index(drop=True)
    test_data = data.iloc[:n_test, :].reset_index(drop=True)

    # Split the data to features and labels
    train_data_x = training_data.loc[:, 'sepal_length':'petal_width']
    train_data_y = training_data[classes]
    test_data_x = test_data.loc[:, 'sepal_length':'petal_width']
    test_data_y = test_data[classes]

    # When returning many variables, it is a good practice to give them names:
    return dict(train_x=train_data_x, train_y=train_data_y,
                test_x=test_data_x, test_y=test_data_y)


def train_model(train_x: pd.DataFrame,
                train_y: pd.DataFrame,
                parameters: Dict[str, Any]) -> np.ndarray:
    """Node for training a simple multi-class logistic regression model. The
    number of training iterations as well as the learning rate are taken from
    conf/project/parameters.yml. All of the data as well as the parameters
    will be provided to this function at the time of execution.
    """
    num_iter = parameters['example_num_train_iter']
    lr = parameters['example_learning_rate']
    X = train_x.values
    Y = train_y.values

    # Add bias to the features
    bias = np.ones((X.shape[0], 1))
    X = np.concatenate((bias, X), axis=1)

    weights = []
    # Train one model for each class in Y
    for k in range(Y.shape[1]):
        # Initialise weights
        theta = np.zeros(X.shape[1])
        y = Y[:, k]
        for _ in range(num_iter):
            z = np.dot(X, theta)
            h = _sigmoid(z)
            gradient = np.dot(X.T, (h - y)) / y.size
            theta -= lr * gradient
        # Save the weights for each model
        weights.append(theta)

    # Return a joint multi-class model with weights for all classes
    return np.vstack(weights).transpose()


def predict(model: np.ndarray,
            test_x: pd.DataFrame) -> np.ndarray:
    """Node for making predictions given a pre-trained model and a test set
    """
    X = test_x.values

    # Add bias to the features
    bias = np.ones((X.shape[0], 1))
    X = np.concatenate((bias, X), axis=1)

    # Predict "probabilities" for each class
    result = _sigmoid(np.dot(X, model))

    # Return the index of the class with max probability for all samples
    return np.argmax(result, axis=1)


def report_accuracy(predictions: np.ndarray,
                    test_y: pd.DataFrame) -> None:
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """
    # Get true class index
    target = np.argmax(test_y.values, axis=1)
    # Calculate accuracy of predictions
    accuracy = np.sum(predictions == target) / target.shape[0]
    # Log the accuracy of the model
    log = logging.getLogger(__name__)
    log.info("Model accuracy on test set: {0:.2f}%".format(accuracy * 100))


def _sigmoid(z):
    """A helper sigmoid function used by the training and the scoring nodes"""
    return 1 / (1 + np.exp(-z))
