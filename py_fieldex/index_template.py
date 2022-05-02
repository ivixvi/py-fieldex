from typing import Any, Dict, List

from py_fieldex.analyzer import Analyzer
from py_fieldex.field import Field


class IndexTemplate:
    def __init__(
        self,
        name: str,
        fields: List[Field],
        index_patterns: List[str],
    ) -> None:
        self.name = name
        self.index_patterns = index_patterns
        self.fields = fields

    def _get_distinct_analyzers(self) -> List[Analyzer]:
        analyzers: Dict[str, Analyzer] = {}
        for field in self.fields:
            analyzers.update(field.get_analyzers())
        return list(analyzers.values())

    def _get_analyzers(self) -> Dict[str, Any]:
        return {
            analyzer.name: analyzer.get_setting()
            for analyzer in self._get_distinct_analyzers()
        }

    def _get_filters(self) -> Dict[str, Any]:
        analyzers = self._get_distinct_analyzers()
        filters: Dict[str, Any] = {}
        for analyzer in analyzers:
            for filter in analyzer.filters:
                filters.update(filter.get_setting())
        return filters

    def _get_char_filters(self) -> Dict[str, Any]:
        analyzers = self._get_distinct_analyzers()
        char_filters: Dict[str, Any] = {}
        for analyzer in analyzers:
            for char_filter in analyzer.char_filters:
                char_filters.update(char_filter.get_setting())
        return char_filters

    def _get_tokenizers(self) -> Dict[str, Any]:
        analyzers = self._get_distinct_analyzers()
        tokenizers: Dict[str, Any] = {}
        for analyzer in analyzers:
            tokenizers.update(analyzer.tokenizer.get_setting())
        return tokenizers

    def _get_properties(self):
        return {field.name: field.get_field() for field in self.fields}

    def build_template(self):
        return {
            "index_patterns": self.index_patterns,
            "settings": {
                "analysis": {
                    "analyzers": self._get_analyzers(),
                    "tokenizer": self._get_tokenizers(),
                    "filters": self._get_filters(),
                    "char_filters": self._get_char_filters(),
                }
            },
            "mappings": {"properties": self._get_properties()},
        }

    def put_path(self):
        return f"PUT _index_template/{self.name}"
