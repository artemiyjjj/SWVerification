"""
Модуль для вычисления метрик Чидамбера и Кемерера (CK metrics) для Python программ.
Метрики:
- WMC (Weighted Methods per Class) - взвешенное количество методов в классе
- DIT (Depth of Inheritance Tree) - глубина дерева наследования
- NOC (Number of Children) - количество прямых потомков
- CBO (Coupling Between Objects) - связность между объектами
- RFC (Response For a Class) - ответ класса на сообщение
- LCOM (Lack of Cohesion of Methods) - недостаток связности методов
"""

import ast
import os
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class Method:
    """Представление метода класса"""
    
    def __init__(self, name: str, node: ast.FunctionDef, parent_class):
        self.name = name
        self.node = node
        self.parent_class = parent_class
        self.accessed_attributes: Set[str] = set()
        self.called_methods: Set[str] = set()
        self.accessed_classes: Set[str] = set()
    
    def add_accessed_attribute(self, attr: str):
        """Добавить атрибут, к которому обращается метод"""
        self.accessed_attributes.add(attr)
    
    def add_called_method(self, method: str):
        """Добавить вызванный метод"""
        self.called_methods.add(method)
    
    def add_accessed_class(self, class_name: str):
        """Добавить класс, к которому обращается метод"""
        self.accessed_classes.add(class_name)


class ClassModel:
    """Представление класса в модели программы"""
    
    def __init__(self, name: str, node: ast.ClassDef):
        self.name = name
        self.node = node
        self.methods: Dict[str, Method] = {}
        self.attributes: Set[str] = set()
        self.base_classes: List[str] = []
        self.file_path: Optional[str] = None
    
    def add_method(self, method: Method):
        """Добавить метод в класс"""
        self.methods[method.name] = method
    
    def add_attribute(self, attr: str):
        """Добавить атрибут класса"""
        self.attributes.add(attr)
    
    def add_base_class(self, base: str):
        """Добавить базовый класс"""
        self.base_classes.append(base)

    def get_methods(self):
        return self.methods.keys()


class ProgramModel:
    """Модель программы для анализа метрик"""
    
    def __init__(self):
        self.classes: Dict[str, ClassModel] = {}
        self.inheritance_tree: Dict[str, List[str]] = defaultdict(list)  # parent -> children
        self.class_files: Dict[str, str] = {}  # class_name -> file_path
    
    def add_class(self, class_model: ClassModel):
        """Добавить класс в модель"""
        self.classes[class_model.name] = class_model
        for base in class_model.base_classes:
            self.inheritance_tree[base].append(class_model.name)

    def get_class(self, name: str) -> Optional[ClassModel]:
        """Получить класс по имени"""
        return self.classes.get(name)
    
    def get_children(self, class_name: str) -> List[str]:
        """Получить список прямых потомков класса"""
        return self.inheritance_tree.get(class_name, [])
    
    def get_depth(self, class_name: str, visited: Optional[Set[str]] = None) -> int:
        """Вычислить глубину дерева наследования для класса"""
        if visited is None:
            visited = set()
        
        if class_name in visited:
            return 0
        
        visited.add(class_name)
        class_model = self.get_class(class_name)
        if not class_model or not class_model.base_classes:
            return 0
        
        max_depth = 0
        for base in class_model.base_classes:
            if base == 'object' or base not in self.classes:
                depth = 1
            else:
                depth = 1 + self.get_depth(base, visited.copy())
            max_depth = max(max_depth, depth)
        
        return max_depth


class CKMetricsCalculator:
    """Калькулятор метрик Чидамбера и Кемерера"""
    
    def __init__(self, model: ProgramModel):
        self.model = model
    
    def wmc(self, class_name: str) -> int:
        """
        WMC (Weighted Methods per Class) - Взвешенные методы на класс.
        sum (1..n) c[i]
        Цикломатическая Сложность методов не учитывается
        """
        class_model = self.model.get_class(class_name)
        if not class_model:
            return 0
        return len(class_model.methods)
    
    def dit(self, class_name: str) -> int:
        """
        DIT (Depth of Inheritance Tree) - глубина дерева наследования.
        Для класса без базовых классов (кроме object) DIT = 0.
        """
        return self.model.get_depth(class_name)
    
    def noc(self, class_name: str) -> int:
        """
        NOC (Number of Children) - количество прямых потомков класса.
        """
        return len(self.model.get_children(class_name))
    
    def cbo(self, class_name: str) -> int:
        """
        CBO (Coupling Between Objects) - количество классов, с которыми связан данный класс.
        Связь возникает при:
        1. Использовании атрибутов другого класса
        2. Вызове методов другого класса
        3. Использовании типа другого класса
        """
        class_model = self.model.get_class(class_name)
        if not class_model:
            return 0
        
        coupled_classes: Set[str] = set()
        
        # Проходим по всем методам класса
        for method in class_model.methods.values():
            # Добавляем классы, к которым обращаются методы
            coupled_classes.update(method.accessed_classes)
        
        # Исключаем сам класс и базовые классы (наследование не считается coupling)
        coupled_classes.discard(class_name)
        for base in class_model.base_classes:
            coupled_classes.discard(base)
        
        return len(coupled_classes)
    
    def rfc(self, class_name: str) -> int:
        """
        RFC (Response For a Class) - количество методов, которые могут быть вызваны
        в ответ на сообщение классу. Включает методы самого класса и методы,
        вызываемые из методов класса.
        """
        class_model = self.model.get_class(class_name)
        if not class_model:
            return 0
        
        all_methods = []
        for model_class in self.model.classes.values():
            all_methods.extend(model_class.get_methods())
        
        # Множество всех методов, которые могут быть вызваны
        response_set: Set[str] = set()
        
        # Добавляем все методы класса
        response_set.update(class_model.methods.keys())
        
        # Добавляем методы, вызываемые из методов класса, если методы других классов модели (а не только стандартных)
        for method in class_model.methods.values():
            for called_method in method.called_methods:
                # Проверка совпадения имени вызываемой функции с методами классов модели
                if called_method in all_methods:
                    response_set.update(called_method)
                    # print(called_method)
        
        return len(response_set)
    
    def lcom(self, class_name: str) -> int:
        """
        LCOM (Lack of Cohesion of Methods) - недостаток связности методов.
        LCOM = количество пар методов, которые не используют общие атрибуты,
        минус количество пар методов, которые используют общие атрибуты.
        Если результат отрицательный, LCOM = 0.
        """
        class_model = self.model.get_class(class_name)
        if not class_model:
            return 0
        
        methods = list(class_model.methods.values())
        if len(methods) <= 1:
            return 0
        
        # Подсчитываем пары методов
        pairs_without_common_attrs = 0
        pairs_with_common_attrs = 0
        
        for i in range(len(methods)):
            for j in range(i + 1, len(methods)):
                attrs_i = methods[i].accessed_attributes
                attrs_j = methods[j].accessed_attributes
                
                # Проверяем пересечение атрибутов
                if attrs_i & attrs_j:  # Есть общие атрибуты
                    pairs_with_common_attrs += 1
                else:
                    pairs_without_common_attrs += 1
        
        lcom_value = pairs_without_common_attrs - pairs_with_common_attrs
        return max(0, lcom_value)
    
    def calculate_all_metrics(self, class_name: str) -> Dict[str, int]:
        """Вычислить все метрики для класса"""
        return {
            'WMC': self.wmc(class_name),
            'DIT': self.dit(class_name),
            'NOC': self.noc(class_name),
            'CBO': self.cbo(class_name),
            'RFC': self.rfc(class_name),
            'LCOM': self.lcom(class_name)
        }


class ModelBuilder:
    """Построитель модели программы из AST"""
    
    def __init__(self):
        self.model = ProgramModel()
        self.current_class: Optional[str] = None
        self.current_method: Optional[str] = None
    
    def build_from_file(self, file_path: str) -> ProgramModel:
        """Построить модель из файла"""
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=file_path)
        self._visit_node(tree, file_path)
        return self.model
    
    def build_from_source(self, source: str, file_path: str = "<string>") -> ProgramModel:
        """Построить модель из исходного кода"""
        tree = ast.parse(source, filename=file_path)
        self._visit_node(tree, file_path)
        return self.model
    
    def _visit_node(self, node: ast.AST, file_path: str):
        """Рекурсивный обход AST"""
        if isinstance(node, ast.ClassDef):
            self._visit_class(node, file_path)
        elif isinstance(node, ast.FunctionDef):
            self._visit_function(node)
        elif isinstance(node, ast.Module):
            for child in node.body:
                self._visit_node(child, file_path)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, ast.AST):
                    self._visit_node(item, file_path)
    
    def _visit_class(self, node: ast.ClassDef, file_path: str):
        """Обработка определения класса"""
        class_model = ClassModel(node.name, node)
        class_model.file_path = file_path
        
        # Обработка базовых классов
        for base in node.bases:
            if isinstance(base, ast.Name):
                class_model.add_base_class(base.id)
            elif isinstance(base, ast.Attribute):
                # Обработка случаев типа ParentClass
                class_model.add_base_class(self._get_full_name(base))
        
        old_class = self.current_class
        self.current_class = node.name
        
        # Обработка тела класса
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self._visit_method(item, class_model)
            elif isinstance(item, ast.Assign):
                # Обработка атрибутов класса (на уровне класса)
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_model.add_attribute(target.id)
        
        self.model.add_class(class_model)
        self.current_class = old_class
    
    def _visit_method(self, node: ast.FunctionDef, class_model: ClassModel):
        """Обработка метода класса"""
        method = Method(node.name, node, class_model)
        
        old_method = self.current_method
        self.current_method = node.name
        
        # Обход тела метода для поиска обращений к атрибутам и вызовов методов
        for child in ast.walk(node):
            if isinstance(child, ast.Attribute):
                self._process_attribute_access(child, method, class_model)
            elif isinstance(child, ast.Call):
                self._process_call(child, method, class_model)
            elif isinstance(child, ast.Assign):
                # Обработка присваиваний атрибутов (self.attr = value)
                for target in child.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                            method.add_accessed_attribute(target.attr)
                            class_model.add_attribute(target.attr)
            elif isinstance(child, ast.Name):
                if isinstance(child.ctx, ast.Load):
                    # Проверяем, является ли это атрибутом класса
                    if child.id in class_model.attributes:
                        method.add_accessed_attribute(child.id)
        
         # Обработка аннотаций типов параметров метода
        for arg in node.args.args:  # Исправлено с node.args на node.args.args
            if isinstance(arg, ast.arg):
                # Обработка аннотаций типов
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        if arg.annotation.id in self.model.classes:
                            method.add_accessed_class(arg.annotation.id)
                    elif isinstance(arg.annotation, ast.Subscript):
                        # Обработка типов вроде List[SomeClass], Optional[SomeClass]
                        if isinstance(arg.annotation.value, ast.Name):
                            if arg.annotation.value.id in self.model.classes:
                                method.add_accessed_class(arg.annotation.value.id)

        class_model.add_method(method)
        self.current_method = old_method
    
    def _visit_function(self, node: ast.FunctionDef):
        """Обработка функции вне класса (пропускаем)"""
        pass
    
    def _process_attribute_access(self, node: ast.Attribute, method: Method, class_model: ClassModel):
        """Обработка обращения к атрибуту"""
        if isinstance(node.value, ast.Name):
            var_name = node.value.id
            attr_name = node.attr
            
            # Если это self.attr, то это атрибут класса
            if var_name == 'self':
                method.add_accessed_attribute(attr_name)
                class_model.add_attribute(attr_name)
            # Если это obj.attr, где obj - другой объект
            elif var_name in self.model.classes:
                method.add_accessed_class(var_name)
        elif isinstance(node.value, ast.Call):
            # Обработка вызовов типа obj.method().attr
            self._process_call(node.value, method, class_model)
    
    def _process_call(self, node: ast.Call, method: Method, class_model: ClassModel):
        """Обработка вызова метода"""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                var_name = node.func.value.id
                method_name = node.func.attr
                
                if var_name == 'self':
                    # Вызов метода того же класса
                    method.add_called_method(method_name)
                elif var_name in self.model.classes:
                    # Вызов метода другого класса
                    method.add_accessed_class(var_name)
                    method.add_called_method(method_name)
            elif isinstance(node.func.value, ast.Call):
                # Обработка цепочки вызовов (obj.method().other_method())
                self._process_call(node.func.value, method, class_model)
                method.add_called_method(node.func.attr)
        elif isinstance(node.func, ast.Name):
            # Прямой вызов функции
            method.add_called_method(node.func.id)
            if node.func.id in self.model.classes:
                # Это создание экземпляра класса
                method.add_accessed_class(node.func.id)
    
    def _get_full_name(self, node: ast.Attribute) -> str:
        """Получить полное имя из атрибута"""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_full_name(node.value)}.{node.attr}"
        return node.attr


def build_model_from_file(file_path: str) -> ProgramModel:
    """Удобная функция для построения модели из файла"""
    builder = ModelBuilder()
    return builder.build_from_file(file_path)


def build_model_from_source(source: str) -> ProgramModel:
    """Удобная функция для построения модели из исходного кода"""
    builder = ModelBuilder()
    return builder.build_from_source(source)

