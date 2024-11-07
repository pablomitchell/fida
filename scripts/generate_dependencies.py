# scripts/generate_dependencies.py
import tomli
import os

def generate_setup_py(config):
    """Generate setup.py from pyproject.toml"""
    print("Generating setup.py...")
    setup_content = """# Generated from pyproject.toml - do not edit directly
from setuptools import setup, find_packages

setup(
    name="{name}",
    version="{version}",
    packages=find_packages(),
    python_requires="{python_requires}",
    install_requires={install_requires!r},
    extras_require={extras_require!r},
)
""".format(
        name=config["project"]["name"],
        version=config["project"]["version"],
        python_requires=config["project"]["requires-python"],
        install_requires=config["project"]["dependencies"],
        extras_require={
            "test": config["project"]["optional-dependencies"]["test"],
            "dev": config["project"]["optional-dependencies"]["dev"]
        }
    )
    
    with open("setup.py", "w") as f:
        f.write(setup_content)
    print("Generated setup.py")

def write_requirements(deps, filename, include_core=False, include_test=False):
    """Write dependencies to a .in file"""
    print(f"\nWriting to {filename}")
    with open(filename, "w") as f:
        if include_core:
            f.write("-r requirements.in\n")
        if include_test:
            f.write("-r requirements-test.in\n")
        
        for dep in deps:
            package = dep.partition('>=')[0].partition('==')[0].strip()
            print(f"  {package}")
            f.write(f"{package}\n")

def main():
    print("Starting dependency generation...")
    
    # Read pyproject.toml
    with open("pyproject.toml", "rb") as f:
        config = tomli.load(f)
    
    # Generate setup.py
    generate_setup_py(config)
    
    # Generate requirements files
    write_requirements(
        config["project"]["dependencies"],
        "requirements.in"
    )
    
    write_requirements(
        config["project"]["optional-dependencies"]["test"],
        "requirements-test.in",
        include_core=True
    )
    
    write_requirements(
        config["project"]["optional-dependencies"]["dev"],
        "requirements-dev.in",
        include_core=True,
        include_test=True
    )
    
    # Compile with uv
    print("\nCompiling requirements files...")
    os.system("uv pip compile requirements.in -o requirements.txt")
    os.system("uv pip compile requirements-test.in -o requirements-test.txt")
    os.system("uv pip compile requirements-dev.in -o requirements-dev.txt")

    # Show generated files
    print("\nGenerated files:")
    for filename in ["setup.py", "requirements.txt", "requirements-test.txt", "requirements-dev.txt"]:
        print(f"- {filename}")

if __name__ == "__main__":
    main()