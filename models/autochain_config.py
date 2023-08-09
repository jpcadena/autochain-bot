"""
A module for autochain config in the models package.
"""

import torch
from autochain.chain.chain import Chain
from sklearn.metrics import accuracy_score
from torch import Tensor
from transformers import BatchEncoding

from models.bert_agent import BertAgent


class AutoChainConfig:
    """
    AutoChainConfig class for configuring and training AutoChain.
    """

    def __init__(self, model_name: str = "bert-base-uncased"):
        """
        Initialize the AutoChainConfig.
        """
        self.autochain = Chain()
        self.bert_agent = BertAgent(model_name)

    def train(
        self,
        x_train: list[str],
        y_train: Tensor,
        x_test: list[str],
        y_test: Tensor,
    ) -> float:
        """
        Train AutoChain with the given data and evaluate on the test set.
        :param x_train: Training text data
        :type x_train: list[str]
        :param y_train: Training labels
        :type y_train: Tensor
        :param x_test: Testing text data
        :type x_test: list[str]
        :param y_test: Testing labels
        :type y_test: Tensor
        :return: Accuracy score on the test set
        :rtype: float
        """
        train_inputs: list[BatchEncoding] = [
            self.bert_agent.tokenize(text) for text in x_train
        ]
        test_inputs: list[BatchEncoding] = [
            self.bert_agent.tokenize(text) for text in x_test
        ]
        for inputs, labels in zip(train_inputs, y_train):
            self.bert_agent.train(inputs, labels)
        y_pred_logits: list[Tensor] = [
            self.bert_agent.predict(inputs.data) for inputs in test_inputs
        ]
        y_pred: Tensor = torch.argmax(torch.cat(y_pred_logits), dim=1)
        return float(accuracy_score(y_test, y_pred.cpu().numpy()))
