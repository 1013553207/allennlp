from overrides import overrides

from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.data.tokenizers import WordTokenizer
from allennlp.models import Model
from allennlp.service.predictors.predictor import Predictor


@Predictor.register('hierarchical-tagger')
class HierarchicalTaggerPredictor(Predictor):
    """
    Wrapper for the :class:`~allennlp.models.hierarchical_tagger.HierarchicalTagger` model.
    """
    def __init__(self, model: Model, dataset_reader: DatasetReader) -> None:
        super().__init__(model, dataset_reader)
        self._tokenizer = WordTokenizer()

    @overrides
    def _json_to_instance(self, json: JsonDict) -> Instance:
        """
        Expects JSON that looks like ``{"sentence": "..."}``
        and returns JSON that looks like
        ``{"tags": [...], "class_probabilities": [[...], ..., [...]]}``
        """
        sentence = json["sentence"]
        tokens, _ = self._tokenizer.tokenize(sentence)
        return self._dataset_reader.text_to_instance(tokens)