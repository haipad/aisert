from sentence_transformers import SentenceTransformer

from src.modules.validator import BaseValidator


class SemanticValidator(BaseValidator):

    _instances ={}

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        super().__init__()
        self.model = SentenceTransformer(model_name)
        self.threshold = 0.8  # Default threshold for semantic similarity


    def validate(self, text1: str, text2: str) -> bool:
        """
        Compare two texts for semantic similarity.
        
        :param text1: First text to compare.
        :param text2: Second text to compare.
        :return: True if texts are semantically similar, False otherwise.
        """
        if type(text1) is not str or type(text2) is not str:
            self.status = False
            self.reason = "Both inputs must be strings not {} and {}".format(type(text1), type(text2))
        else:
            embeddings1 = self.model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.model.encode(text2, convert_to_tensor=True)
            cosine_similarity = embeddings1 @ embeddings2.T
            similarity_score = cosine_similarity.item()
        
            self.status = similarity_score >= self.threshold
            self.reason = f"Semantic similarity score: {similarity_score}, Threshold: {self.threshold}"
        
        return self.result
    
    def set_threshold(self, threshold: float):
        """
        Set the threshold for semantic similarity.
        
        :param threshold: New threshold value.
        """
        if 0 <= threshold <= 1:
            self.threshold = threshold
            self.logger.info(f"Threshold set to {self.threshold}")
        else:
            self.logger.error("Threshold must be between 0 and 1")
            raise ValueError("Threshold must be between 0 and 1")
    
    @classmethod
    def get_instance(cls, model_name='all-MiniLM-L6-v2'):
        """
        Get an instance of SemanticValidator with specified model and threshold.
        
        :param model_name: Name of the sentence transformer model.
        :param threshold: Threshold for semantic similarity.
        :return: An instance of SemanticValidator.
        """
        if model_name not in cls._instances:
            cls._instances[model_name] = cls(model_name)
        return cls._instances[model_name]
