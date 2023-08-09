"""
A module for bert agent in the models package.
"""
from typing import Any

import torch
from torch import Tensor
from transformers import (
    BatchEncoding,
    BertForSequenceClassification,
    BertTokenizer,
)


class BertAgent:
    """
    BertAgent class for handling BERT related functions.
    """

    def __init__(self, model_name: str = "bert-base-uncased"):
        """
        Initialize the BertAgent with specific model name.
        :param model_name: Name of the BERT model to use
        :type model_name: str
        """
        self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained(
            model_name
        )
        self.model = BertForSequenceClassification.from_pretrained(model_name)

    def tokenize(self, text: str) -> BatchEncoding:
        """
        Tokenizes the given text using BERT tokenizer.
        :param text: Text to be tokenized
        :type text: str
        :return: Tokenized output as a BatchEncoding object
        :rtype: BatchEncoding
        """
        return self.tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        )

    def train(self, inputs: dict[str, Any], labels: Tensor) -> None:
        """
        Trains the BERT model with given inputs and labels.
        :param inputs: Input data for training
        :type inputs: dict[str, Any]
        :param labels: Labels for training
        :type labels: Tensor
        """
        outputs = self.model(**inputs, labels=labels)
        loss = outputs.loss
        loss.backward()

    def predict(self, inputs: dict[str, Any]) -> Tensor:
        """
        Predicts the outputs for given inputs using the BERT model.
        :param inputs: Input data for prediction
        :type inputs: dict[str, Any]
        :return: Predicted outputs
        :rtype: Tensor
        """
        with torch.no_grad():
            return Tensor(self.model(**inputs).logits)
