#!/usr/bin/env python3
"""
Тестовый скрипт для проверки обработки ошибок
"""

import csv
import tempfile
import os
from main import PackageManagerVisualizer, ConfigError


def create_test_config(params):
    """Создание временного конфигурационного файла для тестирования"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['parameter', 'value'])
        for key, value in params.items():
            writer.writerow([key, value])
        return f.name


def test_valid_config():
    """Тест валидной конфигурации"""
    print("Тест 1: Валидная конфигурация")
    config_params = {
        'package_name': 'numpy',
        'repository_url': 'https://github.com/numpy/numpy',
        'test_repo_mode': 'false',
        'ascii_tree_output': 'true',
        'max_depth': '5'
    }
    
    config_file = create_test_config(config_params)
    visualizer = PackageManagerVisualizer()
    
    try:
        config = visualizer.load_config(config_file)
        print("✅ Успешно загружена валидная конфигурация")
        visualizer.display_config(config)
    except ConfigError as e:
        print(f"❌ Ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_missing_parameter():
    """Тест отсутствующего параметра"""
    print("\nТест 2: Отсутствующий параметр")
    config_params = {
        'package_name': 'numpy',
        'repository_url': 'https://github.com/numpy/numpy',
        'test_repo_mode': 'false',
        # Отсутствует ascii_tree_output
        'max_depth': '5'
    }
    
    config_file = create_test_config(config_params)
    visualizer = PackageManagerVisualizer()
    
    try:
        config = visualizer.load_config(config_file)
        print("❌ Ожидалась ошибка отсутствующего параметра")
    except ConfigError as e:
        print(f"✅ Корректно обработана ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_invalid_max_depth():
    """Тест невалидного max_depth"""
    print("\nТест 3: Невалидный max_depth")
    config_params = {
        'package_name': 'numpy',
        'repository_url': 'https://github.com/numpy/numpy',
        'test_repo_mode': 'false',
        'ascii_tree_output': 'true',
        'max_depth': 'invalid'
    }
    
    config_file = create_test_config(config_params)
    visualizer = PackageManagerVisualizer()
    
    try:
        config = visualizer.load_config(config_file)
        print("❌ Ожидалась ошибка валидации max_depth")
    except ConfigError as e:
        print(f"✅ Корректно обработана ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_invalid_boolean():
    """Тест невалидного булевого значения"""
    print("\nТест 4: Невалидное булево значение")
    config_params = {
        'package_name': 'numpy',
        'repository_url': 'https://github.com/numpy/numpy',
        'test_repo_mode': 'maybe',  # Невалидное значение
        'ascii_tree_output': 'true',
        'max_depth': '5'
    }
    
    config_file = create_test_config(config_params)
    visualizer = PackageManagerVisualizer()
    
    try:
        config = visualizer.load_config(config_file)
        print("❌ Ожидалась ошибка валидации булевого значения")
    except ConfigError as e:
        print(f"✅ Корректно обработана ошибка: {e}")
    finally:
        os.unlink(config_file)


if __name__ == "__main__":
    test_valid_config()
    test_missing_parameter()
    test_invalid_max_depth()
    test_invalid_boolean()