from __future__ import annotations
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import time, os, json, uuid

class Repository(ABC):
    @abstractmethod
    def save_dataset(self, name: str, meta: Dict[str, Any], rows: List[Dict[str, Any]]) -> str: ...
    @abstractmethod
    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]: ...
    @abstractmethod
    def list_datasets(self) -> List[Dict[str, Any]]: ...

class InMemoryRepository(Repository):
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def save_dataset(self, name, meta, rows):
        dataset_id = str(int(time.time() * 1000))
        self._store[dataset_id] = {"id": dataset_id, "name": name, "meta": meta, "rows": rows}
        return dataset_id

    def get_dataset(self, dataset_id):
        return self._store.get(dataset_id)

    def list_datasets(self):
        return list(self._store.values())

class FileRepository(Repository):
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.manifest_path = os.path.join(self.base_dir, "manifest.json")
        if not os.path.exists(self.manifest_path):
            self._write_manifest({})

    def _read_manifest(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_manifest(self, manifest: Dict[str, Dict[str, Any]]):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    def save_dataset(self, name, meta, rows):
        dataset_id = uuid.uuid4().hex
        record = {"id": dataset_id, "name": name, "meta": meta}
        # write rows to separate file to avoid huge manifest
        rows_path = os.path.join(self.base_dir, f"{dataset_id}.rows.jsonl")
        with open(rows_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        manifest = self._read_manifest()
        manifest[dataset_id] = record
        self._write_manifest(manifest)
        return dataset_id

    def get_dataset(self, dataset_id):
        manifest = self._read_manifest()
        rec = manifest.get(dataset_id)
        if not rec:
            return None
        rows_path = os.path.join(self.base_dir, f"{dataset_id}.rows.jsonl")
        rows: List[Dict[str, Any]] = []
        if os.path.exists(rows_path):
            with open(rows_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        pass
        rec = {**rec, "rows": rows}
        return rec

    def list_datasets(self):
        manifest = self._read_manifest()
        return list(manifest.values())
