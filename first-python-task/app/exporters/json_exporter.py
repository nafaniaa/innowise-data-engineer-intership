from app.exporters.base_exporter import BaseExporter
import json

class JsonExporter(BaseExporter):
    def export(self, data: dict, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)