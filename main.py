import csv
import urllib.request
import json

class Config:
    def __init__(self):
        self.package_name = ""
        self.repo_url = ""
        self.test_mode = False
        self.ascii_tree = False
        self.max_depth = 0

def read_config(filename):
    config = Config()
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            row = next(reader)
            
            config.package_name = row['package_name']
            config.repo_url = row['repo_url']
            config.test_mode = row['test_mode'].lower() == 'true'
            config.ascii_tree = row['ascii_tree'].lower() == 'true'
            config.max_depth = int(row['max_depth'])
            
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return None
    except KeyError as e:
        print(f"Ошибка: в конфиге нет ключа {e}")
        return None
    except ValueError as e:
        print(f"Ошибка: неправильное значение в конфиге {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None
    
    return config

def get_dependencies(package_name, repo_url):
    try:
        # Для NuGet репозитория
        if "nuget.org" in repo_url:
            # API NuGet для получения информации о пакете
            api_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
            
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read())
                
            # Берем последнюю версию пакета
            latest_version = data['versions'][-1]
            
            version_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/{latest_version}/{package_name.lower()}.nuspec"
            
            with urllib.request.urlopen(version_url) as response:
                nuspec_content = response.read().decode('utf-8')
                
            # Парсим зависимости из nuspec
            dependencies = []
            if '<dependency' in nuspec_content:
                # Упрощенный парсинг - ищем блоки dependency
                start_idx = nuspec_content.find('<dependencies>')
                if start_idx != -1:
                    end_idx = nuspec_content.find('</dependencies>', start_idx)
                    deps_section = nuspec_content[start_idx:end_idx]
                    
                    
                    dep_start = 0
                    while True:
                        dep_start = deps_section.find('<dependency', dep_start)
                        if dep_start == -1:
                            break
                            
                        dep_end = deps_section.find('/>', dep_start)
                        if dep_end == -1:
                            dep_end = deps_section.find('</dependency>', dep_start)
                            
                        if dep_end != -1:
                            dep_line = deps_section[dep_start:dep_end]
                            id_start = dep_line.find('id="') + 4
                            id_end = dep_line.find('"', id_start)
                            if id_start != -1 and id_end != -1:
                                dep_id = dep_line[id_start:id_end]
                                dependencies.append(dep_id)
                                
                        dep_start = dep_end + 1
                        
            return dependencies
            
        else:
            print("Пока поддерживается только nuget.org")
            return []
            
    except Exception as e:
        print(f"Ошибка при получении зависимостей: {e}")
        return []

def main():
    config = read_config('config.csv')
    
    if config is None:
        return
    
    print("Настройки из конфига:")
    print(f"Имя пакета: {config.package_name}")
    print(f"URL репозитория: {config.repo_url}")
    print(f"Тестовый режим: {config.test_mode}")
    print(f"ASCII-дерево: {config.ascii_tree}")
    print(f"Макс. глубина: {config.max_depth}")
    print()
    
    
    print("Прямые зависимости пакета:")
    dependencies = get_dependencies(config.package_name, config.repo_url)
    
    if dependencies:
        for dep in dependencies:
            print(f"- {dep}")
    else:
        print("Зависимости не найдены или пакет не имеет зависимостей")

if __name__ == "__main__":
    main()  