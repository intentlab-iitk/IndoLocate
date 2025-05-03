.PHONY: all clean build develop install uninstall

all:
	@echo "\n[#] Building indolocate..."
	@python -m build
	@echo ""

clean:
	@python -c "import os, shutil; \
    [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.mypy_cache', 'build', 'dist', 'models'] if os.path.exists(p)]; \
    [shutil.rmtree(os.path.join(root, d), ignore_errors=True) for root, dirs, _ in os.walk('src') for d in dirs if d == '__pycache__']; \
    [shutil.rmtree(os.path.join(root, d), ignore_errors=True) for root, dirs, _ in os.walk('src') for d in dirs if d.endswith('.egg-info')]"
	@echo "\n[#] Cleaned the artifacts."
	@echo ""

develop: all
	@echo "\n[#] Running editable install..."
	@pip install -e .
	@echo ""

install: uninstall all
	@echo "\n[#] Installing the package..."
	@pip install dist/*.whl
	@echo ""

uninstall:
	@echo "\n[#] Uninstalling the package..."
	@pip uninstall -y indolocate
	@echo ""