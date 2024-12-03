"""
AST Analyzer for intelligent code analysis
"""
import ast
from typing import Dict, Any, List
from pathlib import Path
from loguru import logger
from pydantic import BaseModel
from code_analyzer.crews.base_crew import BaseCrew

class ClassAnalysis(BaseModel):
    """Class structure analysis results"""
    name: str
    methods: List[str]
    attributes: List[str]
    inheritance: List[str]
    decorators: List[str]
    metrics: Dict[str, float]

class FunctionAnalysis(BaseModel):
    """Function analysis results"""
    name: str
    parameters: List[str]
    return_type: str
    docstring: str
    complexity: float
    dependencies: List[str]

class ASTAnalyzer(BaseCrew):
    """Crew for analyzing Python code structure"""
    
    def __init__(self, target_path: str):
        super().__init__("ASTAnalyzer", target_path)
        self.analysis_results = {}
    
    async def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file's structure"""
        async with self.managed_operation():
            try:
                # Read and parse file
                content = await self.read_file(file_path)
                tree = ast.parse(content)
                
                # Analyze components
                classes = await self._analyze_classes(tree)
                functions = await self._analyze_functions(tree)
                imports = await self._analyze_imports(tree)
                patterns = await self._identify_patterns(tree)
                
                # Calculate metrics
                metrics = await self._calculate_metrics(tree)
                
                return {
                    "file": file_path,
                    "classes": classes,
                    "functions": functions,
                    "imports": imports,
                    "patterns": patterns,
                    "metrics": metrics,
                    "timestamp": self.get_timestamp()
                }
                
            except Exception as e:
                self.logger.error(f"Analysis failed for {file_path}: {e}")
                return {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": self.get_timestamp()
                }
    
    async def _analyze_classes(self, tree: ast.AST) -> List[ClassAnalysis]:
        """Extract and analyze class definitions"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = ClassAnalysis(
                    name=node.name,
                    methods=self._extract_methods(node),
                    attributes=self._extract_attributes(node),
                    inheritance=self._extract_inheritance(node),
                    decorators=self._extract_decorators(node),
                    metrics=self._calculate_class_metrics(node)
                )
                classes.append(class_info)
        return classes
    
    async def _analyze_functions(self, tree: ast.AST) -> List[FunctionAnalysis]:
        """Extract and analyze function definitions"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = FunctionAnalysis(
                    name=node.name,
                    parameters=self._extract_parameters(node),
                    return_type=self._extract_return_type(node),
                    docstring=ast.get_docstring(node) or "",
                    complexity=self._calculate_complexity(node),
                    dependencies=self._extract_dependencies(node)
                )
                functions.append(func_info)
        return functions 