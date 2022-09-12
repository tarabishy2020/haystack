from typing import Any, List

import logging
from abc import ABC, abstractmethod

import torch

from haystack.schema import ContentTypes


logger = logging.getLogger(__name__)


class HaystackModel(ABC):
    """
    Interface on top of HaystackTransformer and HaystackSentenceTransformer
    """

    def __init__(self, pretrained_model_name_or_path: str, model_type: str, content_type: ContentTypes):
        """
        :param pretrained_model_name_or_path: name of the model to load
        :param model_type: the value of model_type from the model's Config
        :param content_type: the type of data (text, image, ...) the model is supposed to process.
            See the values of `haystack.schema.ContentTypes`.
        """
        logger.info(
            f" 🤖 Loading '{pretrained_model_name_or_path}' "
            f"({self.__class__.__name__} of type '{model_type if model_type else '<unknown>'}' "
            f"for {content_type} data)"
        )
        self.model_name_or_path = pretrained_model_name_or_path
        self.model_type = model_type
        self.content_type = content_type

    @abstractmethod
    def encode(self, data: List[Any], **kwargs) -> torch.Tensor:
        """
        The output dimension of this language model
        """
        raise NotImplementedError("Abstract method, use a subclass.")
