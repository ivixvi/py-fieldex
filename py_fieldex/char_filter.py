from typing import Any, Dict, Optional


class CharFilter:
    def __init__(self, name: str, setting: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.setting = setting

    def get_setting(self) -> Dict[str, Any]:
        if self.setting:
            return {self.name: self.setting}
        else:
            return {}
