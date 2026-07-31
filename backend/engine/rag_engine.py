import os
import sys
import importlib.util

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_engine_path = os.path.join(root_dir, "engine", "rag_engine.py")

spec = importlib.util.spec_from_file_location("root_rag_engine", root_engine_path)
root_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_module)

RAGEngine = root_module.RAGEngine
safe_print = root_module.safe_print

__all__ = ["RAGEngine", "safe_print"]

