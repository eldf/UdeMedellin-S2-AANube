from pathlib import Path


def create_ml_structure():
    # Definición de la estructura: carpetas y archivos
    structure = {
        "data": [],  # Directorio para datos
        "notebooks": [],  # Directorio para EDA
        "scripts": [
            "data_prep.py",
            "train.py",
            "evaluate.py",
            "tasks.py",
        ],  # Directorio para scripts de ML
        "main_flow.py": None,  # Archivo de orquestación (Prefect)
        "pyproject.toml": None,  # Gestión de dependencias
    }

    print("🏗️  Iniciando la creación de la estructura del proyecto...\n")

    for folder, content in structure.items():
        if content is None:
            # Es un archivo en la raíz
            Path(folder).touch()
            print(f"📄 Archivo creado: {folder}")
        else:
            # Es un directorio
            Path(folder).mkdir(exist_ok=True)
            print(f"📁 Directorio creado: {folder}/")

            # Si tiene archivos internos
            for file in content:
                file_path = Path(folder) / file
                file_path.touch()
                print(f"   └── 📄 Archivo creado: {file}")

    print("\n✅ ¡Estructura lista para empezar a trabajar!")


if __name__ == "__main__":
    create_ml_structure()
