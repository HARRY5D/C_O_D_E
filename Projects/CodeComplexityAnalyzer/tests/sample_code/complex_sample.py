"""
Sample Python code with varying complexity levels for testing the analyzer.
"""

import math
from typing import List, Dict, Optional


def simple_function(x: int, y: int) -> int:
    """A simple function with low complexity."""
    return x + y


def moderate_complexity_function(data: List[int], threshold: int = 10) -> List[int]:
    """A function with moderate complexity."""
    result = []
    
    for item in data:
        if item > threshold:
            result.append(item * 2)
        elif item < 0:
            result.append(0)
        else:
            result.append(item)
    
    return result


def high_complexity_function(data: Dict[str, any], mode: str = 'default') -> Dict[str, any]:
    """A function with high cyclomatic complexity for testing."""
    processed_data = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            if mode == 'uppercase':
                if len(value) > 5:
                    processed_data[key] = value.upper()
                else:
                    processed_data[key] = value.capitalize()
            elif mode == 'lowercase':
                processed_data[key] = value.lower()
            else:
                if value.isdigit():
                    processed_data[key] = int(value)
                else:
                    processed_data[key] = value
        elif isinstance(value, int):
            if mode == 'double':
                if value > 0:
                    processed_data[key] = value * 2
                else:
                    processed_data[key] = 0
            elif mode == 'square':
                processed_data[key] = value ** 2
            else:
                if value % 2 == 0:
                    processed_data[key] = value // 2
                else:
                    processed_data[key] = value + 1
        elif isinstance(value, float):
            if mode == 'round':
                processed_data[key] = round(value)
            elif mode == 'ceil':
                processed_data[key] = math.ceil(value)
            elif mode == 'floor':
                processed_data[key] = math.floor(value)
            else:
                processed_data[key] = value
        elif isinstance(value, list):
            if mode == 'sum':
                try:
                    processed_data[key] = sum(value)
                except TypeError:
                    processed_data[key] = len(value)
            elif mode == 'length':
                processed_data[key] = len(value)
            else:
                processed_data[key] = value
        else:
            processed_data[key] = str(value)
    
    return processed_data


def deeply_nested_function(matrix: List[List[int]]) -> int:
    """A function with deep nesting for testing nesting depth calculation."""
    total = 0
    
    for i, row in enumerate(matrix):
        if i % 2 == 0:  # Even rows
            for j, cell in enumerate(row):
                if j % 2 == 0:  # Even columns
                    if cell > 0:
                        if cell % 2 == 0:
                            if cell > 10:
                                if cell < 100:
                                    total += cell * 2
                                else:
                                    total += cell
                            else:
                                total += cell // 2
                        else:
                            total += cell
                    else:
                        total -= abs(cell)
                else:  # Odd columns
                    if cell < 0:
                        total += abs(cell)
                    else:
                        total += cell
        else:  # Odd rows
            for j, cell in enumerate(row):
                if cell != 0:
                    total += cell
    
    return total


def function_with_many_parameters(a, b, c, d, e, f, g, h, i, j):
    """A function with many parameters to test parameter counting."""
    return a + b + c + d + e + f + g + h + i + j


def function_with_exception_handling(data: List[str]) -> List[int]:
    """Function with exception handling to test complexity calculation."""
    results = []
    
    for item in data:
        try:
            value = int(item)
            if value > 0:
                results.append(value)
            else:
                results.append(0)
        except ValueError:
            try:
                value = float(item)
                results.append(int(value))
            except ValueError:
                results.append(-1)
        except Exception:
            results.append(-999)
    
    return results


class SampleClass:
    """A sample class for testing class detection."""
    
    def __init__(self, name: str, value: int = 0):
        """Initialize the sample class."""
        self.name = name
        self.value = value
        self.history = []
    
    def get_name(self) -> str:
        """Simple getter method."""
        return self.name
    
    def set_value(self, new_value: int) -> None:
        """Simple setter method with validation."""
        if isinstance(new_value, int):
            if new_value >= 0:
                self.history.append(self.value)
                self.value = new_value
            else:
                raise ValueError("Value must be non-negative")
        else:
            raise TypeError("Value must be an integer")
    
    def process_complex_data(self, data: Dict[str, any]) -> Dict[str, any]:
        """Complex method for testing method complexity."""
        result = {'processed': True, 'items': []}
        
        for key, value in data.items():
            item_result = {'key': key, 'original': value}
            
            if isinstance(value, str):
                if value.startswith('prefix_'):
                    item_result['type'] = 'prefixed_string'
                    item_result['processed'] = value[7:]  # Remove prefix
                elif value.endswith('_suffix'):
                    item_result['type'] = 'suffixed_string'
                    item_result['processed'] = value[:-7]  # Remove suffix
                else:
                    item_result['type'] = 'normal_string'
                    item_result['processed'] = value.strip()
            elif isinstance(value, int):
                if value > self.value:
                    item_result['type'] = 'large_number'
                    item_result['processed'] = value - self.value
                elif value < self.value:
                    item_result['type'] = 'small_number'
                    item_result['processed'] = self.value - value
                else:
                    item_result['type'] = 'equal_number'
                    item_result['processed'] = value
            elif isinstance(value, list):
                if len(value) > 0:
                    if all(isinstance(x, int) for x in value):
                        item_result['type'] = 'int_list'
                        item_result['processed'] = sum(value)
                    elif all(isinstance(x, str) for x in value):
                        item_result['type'] = 'str_list'
                        item_result['processed'] = ' '.join(value)
                    else:
                        item_result['type'] = 'mixed_list'
                        item_result['processed'] = len(value)
                else:
                    item_result['type'] = 'empty_list'
                    item_result['processed'] = 0
            else:
                item_result['type'] = 'unknown'
                item_result['processed'] = str(value)
            
            result['items'].append(item_result)
        
        return result


class DataProcessor(SampleClass):
    """A more complex class inheriting from SampleClass."""
    
    def __init__(self, name: str, config: Dict[str, any]):
        super().__init__(name)
        self.config = config
        self.processed_count = 0
    
    def validate_config(self) -> bool:
        """Validate the configuration with multiple checks."""
        required_keys = ['input_format', 'output_format', 'validation_rules']
        
        for key in required_keys:
            if key not in self.config:
                return False
            
            if key == 'input_format':
                if self.config[key] not in ['json', 'csv', 'xml']:
                    return False
            elif key == 'output_format':
                if self.config[key] not in ['json', 'csv', 'xml', 'yaml']:
                    return False
            elif key == 'validation_rules':
                if not isinstance(self.config[key], dict):
                    return False
                
                for rule_name, rule_config in self.config[key].items():
                    if not isinstance(rule_config, dict):
                        return False
                    if 'type' not in rule_config:
                        return False
                    if 'required' not in rule_config:
                        return False
        
        return True
    
    def process_batch(self, batch_data: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Process a batch of data with complex validation and transformation."""
        if not self.validate_config():
            raise ValueError("Invalid configuration")
        
        results = []
        
        for item in batch_data:
            try:
                processed_item = self._process_single_item(item)
                if processed_item:
                    results.append(processed_item)
                    self.processed_count += 1
            except Exception as e:
                error_item = {
                    'error': True,
                    'message': str(e),
                    'original_item': item
                }
                results.append(error_item)
        
        return results
    
    def _process_single_item(self, item: Dict[str, any]) -> Optional[Dict[str, any]]:
        """Process a single item according to validation rules."""
        validation_rules = self.config['validation_rules']
        processed_item = {'original': item, 'validated_fields': {}}
        
        for field_name, field_value in item.items():
            if field_name in validation_rules:
                rule = validation_rules[field_name]
                
                if rule['type'] == 'string':
                    if isinstance(field_value, str):
                        if 'min_length' in rule:
                            if len(field_value) < rule['min_length']:
                                if rule.get('required', False):
                                    return None
                                else:
                                    continue
                        if 'max_length' in rule:
                            if len(field_value) > rule['max_length']:
                                field_value = field_value[:rule['max_length']]
                        
                        processed_item['validated_fields'][field_name] = field_value
                    else:
                        if rule.get('required', False):
                            return None
                
                elif rule['type'] == 'number':
                    if isinstance(field_value, (int, float)):
                        if 'min_value' in rule:
                            if field_value < rule['min_value']:
                                if rule.get('required', False):
                                    return None
                                else:
                                    continue
                        if 'max_value' in rule:
                            if field_value > rule['max_value']:
                                field_value = rule['max_value']
                        
                        processed_item['validated_fields'][field_name] = field_value
                    else:
                        if rule.get('required', False):
                            return None
                
                elif rule['type'] == 'list':
                    if isinstance(field_value, list):
                        if 'min_items' in rule:
                            if len(field_value) < rule['min_items']:
                                if rule.get('required', False):
                                    return None
                                else:
                                    continue
                        if 'max_items' in rule:
                            if len(field_value) > rule['max_items']:
                                field_value = field_value[:rule['max_items']]
                        
                        processed_item['validated_fields'][field_name] = field_value
                    else:
                        if rule.get('required', False):
                            return None
            else:
                # Field not in validation rules
                processed_item['validated_fields'][field_name] = field_value
        
        return processed_item


# Module-level variables and constants
DEFAULT_CONFIG = {
    'input_format': 'json',
    'output_format': 'json',
    'validation_rules': {
        'name': {'type': 'string', 'required': True, 'min_length': 1},
        'age': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 150},
        'tags': {'type': 'list', 'required': False, 'max_items': 10}
    }
}

SUPPORTED_FORMATS = ['json', 'csv', 'xml', 'yaml']
