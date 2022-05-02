from typing import Any, Dict, List, Optional

from py_fieldex.analyzer import Analyzer


class Field:
    def __init__(
        self,
        name: str,
        type_: str,
        analyzer: Optional[Analyzer] = None,
        search_analyzer: Optional[Analyzer] = None,
        fields: Optional[List[Any]] = None,
    ):
        self.name = name
        self.type_ = type_
        self.analyzer = analyzer
        self.search_analyzer = search_analyzer
        self.fields = fields

    def get_field(self) -> Dict[str, Any]:
        field: Dict[str, Any] = {"type": self.type_}
        if self.analyzer:
            field["analyzer"] = self.analyzer.name
        if self.search_analyzer:
            field["search_analyzer"] = self.search_analyzer.name
        if self.fields:
            field["fields"] = {field.name: field.get_field() for field in self.fields}
        return field

    def get_analyzers(self):
        analyzers: Dict[str, Any] = {}
        if self.analyzer:
            analyzers[self.analyzer.name] = self.analyzer
        if self.search_analyzer:
            analyzers[self.search_analyzer.name] = self.search_analyzer
        if self.fields:
            for field in self.fields:
                analyzers.update(field.get_analyzers())
        return analyzers
