from app.exporters.base_exporter import BaseExporter
import json
from decimal import Decimal

class JsonExporter(BaseExporter):
    def export(self, data: dict, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
           json.dump(data, f, ensure_ascii=False, indent=2, default=lambda o: float(o) if isinstance(o, Decimal) else o)