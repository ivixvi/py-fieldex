from typing import Any, Dict, List

from py_fieldex.char_filter import CharFilter
from py_fieldex.filter import Filter
from py_fieldex.tokenizer import Tokenizer


class Analyzer:
    def __init__(
        self,
        name: str,
        filters: List[Filter],
        tokenizer: Tokenizer,
        char_filters: List[CharFilter],
    ):
        self.name = name
        self.filters = filters
        self.tokenizer = tokenizer
        self.char_filters = char_filters

    def get_setting(self) -> Dict[str, Any]:
        return {
            "type": "custom",
            "tokenizer": self.tokenizer.name,
            "filters": [filter_.name for filter_ in self.filters],
            "char_filters": [char_filter.name for char_filter in self.char_filters],
        }
