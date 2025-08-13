import threading

from ..models.result import Result
from .validator import BaseValidator


class SemanticValidator(BaseValidator):
    _instances = {}
    _lock = threading.RLock()

    def __init__(self, model_name):
        from sentence_transformers import SentenceTransformer  # lazy import

        super().__init__("SemanticValidator")
        self.model = SentenceTransformer(model_name)

    def validate(self, text1: str, text2: str, threshold: float=0.8) -> Result:
        """
        Compare two texts for semantic similarity.

        :param text1: First text to compare.
        :param text2: Second text to compare.
        :param threshold: minimum semantic similarity in the range (0-1)
        :return: True if texts are semantically similar, False otherwise.
        """
        from sentence_transformers import util  # lazy import

        if 1<= threshold <=0:
            return Result(False, "Threshold must be between 0 and 1")

        if type(text1) is not str or type(text2) is not str:
            return Result(False, "Both inputs must be strings not {} and {}".format(
                type(text1), type(text2)
            ))
        else:
            embeddings1 = self.model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.model.encode(text2, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
            return Result(similarity_score >= threshold,
                          f"Semantic similarity score: {similarity_score}, Threshold: {threshold}")

    @classmethod
    def get_instance(cls, model_name: str):
        """
        Get an instance of SemanticValidator with specified model and threshold.

        :param model_name: Name of the sentence transformer model.
        :return: An instance of SemanticValidator.
        """
        with cls._lock:
            if model_name not in cls._instances:
                print(f"Creating new instance of SemanticValidator for model {model_name}")
                cls._instances[model_name] = cls(model_name)
            return cls._instances[model_name]

    def clear_cache(self, model_instance: int = 3):
        """
        Clear the cache of sentence transformer models.

        :param model_instance: Number of models to keep in cache.
        """
        while len(SemanticValidator._instances) > model_instance:
            try:
                SemanticValidator._instances.pop(next(iter(SemanticValidator._instances)))
            except Exception as e:
                self.logger.warning(f"Error clearing cache: {e}")
