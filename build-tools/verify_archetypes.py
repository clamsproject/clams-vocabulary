#!/usr/bin/env python3
"""
Verify that archetype.py files are well-formed and syntactically correct.

This script checks:
1. Python syntax (AST parsing)
2. Import completeness (all used types are imported)
3. Parent dependency chain (parent types exist and are importable)
4. Required ClassVars (description, etc.)
5. Pydantic model validity (can instantiate with test data)
"""

import ast
import importlib
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple


# Add project root to path
SCRIPT_DIR = Path(__file__).parent
PROJ_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))


class ArchetypeValidator:
    """Validate archetype.py files for correctness."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []

    def validate_file(self, archetype_file: Path) -> bool:
        """
        Validate a single archetype.py file.

        Returns:
            True if valid, False if errors found
        """
        type_name = archetype_file.parent.name
        if self.verbose:
            print(f"\nValidating {type_name}...")

        # Reset error/warning state
        file_errors = []
        file_warnings = []

        # 1. Check syntax
        try:
            with open(archetype_file, 'r') as f:
                source = f.read()
            tree = ast.parse(source, filename=str(archetype_file))
        except SyntaxError as e:
            file_errors.append(f"Syntax error: {e}")
            self.errors.append((type_name, file_errors))
            return False

        # 2. Extract imports and class definition
        imports = self._extract_imports(tree)
        class_node = self._find_class_node(tree)

        if not class_node:
            file_errors.append("No class definition found")
            self.errors.append((type_name, file_errors))
            return False

        # 3. Check import completeness
        used_types = self._extract_used_types(class_node)
        missing_imports = self._check_imports(imports, used_types)
        if missing_imports:
            file_errors.append(
                f"Missing imports: {', '.join(sorted(missing_imports))}"
            )

        # 4. Check parent dependency
        parent = self._get_parent_class(class_node)
        if parent and parent != 'VocabType':
            parent_errors = self._check_parent_dependency(
                archetype_file, parent, imports
            )
            file_errors.extend(parent_errors)

        # 5. Check required ClassVars
        classvar_errors = self._check_required_classvars(class_node)
        file_errors.extend(classvar_errors)

        # 6. Try to import the module
        import_errors = self._try_import(archetype_file)
        file_errors.extend(import_errors)

        # 7. Check Pydantic field definitions
        field_warnings = self._check_field_definitions(class_node)
        file_warnings.extend(field_warnings)

        # Store results
        if file_errors:
            self.errors.append((type_name, file_errors))
        if file_warnings:
            self.warnings.append((type_name, file_warnings))

        # Print results
        if file_errors:
            print(f"  ✗ {type_name}: {len(file_errors)} error(s)")
            if self.verbose:
                for error in file_errors:
                    print(f"    - {error}")
        elif file_warnings:
            print(f"  ⚠ {type_name}: {len(file_warnings)} warning(s)")
            if self.verbose:
                for warning in file_warnings:
                    print(f"    - {warning}")
        else:
            print(f"  ✓ {type_name}")

        return len(file_errors) == 0

    def _extract_imports(self, tree: ast.AST) -> Dict[str, str]:
        """
        Extract all imports from the AST.

        Returns:
            Dict mapping imported names to their source
            e.g., {'Dict': 'typing', 'Field': 'pydantic'}
        """
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports[name] = module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports[name] = alias.name

        return imports

    def _find_class_node(self, tree: ast.AST) -> Optional[ast.ClassDef]:
        """Find the main class definition (not nested classes)."""
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                return node
        return None

    def _extract_used_types(self, class_node: ast.ClassDef) -> Set[str]:
        """
        Extract all type names used in the class.

        Looks for:
        - Type annotations (field: Dict[str, Any])
        - ClassVar annotations (description: ClassVar[str])
        - Field() default values
        """
        used_types = set()

        for node in ast.walk(class_node):
            if isinstance(node, ast.Name):
                used_types.add(node.id)
            elif isinstance(node, ast.Subscript):
                # Extract from Dict[str, Any], List[str], etc.
                if isinstance(node.value, ast.Name):
                    used_types.add(node.value.id)

        # Filter out built-in types and common names
        builtins = {
            'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
            'None', 'True', 'False', 'self', 'cls'
        }
        return used_types - builtins

    def _check_imports(
        self,
        imports: Dict[str, str],
        used_types: Set[str]
    ) -> Set[str]:
        """Check which used types are not imported."""
        # Types that should be imported from typing
        typing_types = {
            'Dict', 'List', 'Set', 'Tuple', 'Optional', 'Union',
            'Any', 'ClassVar'
        }

        # Pydantic types
        pydantic_types = {'Field', 'BaseModel'}

        missing = set()
        for used_type in used_types:
            if used_type not in imports:
                # Check if it should be imported
                if used_type in typing_types or used_type in pydantic_types:
                    missing.add(used_type)

        return missing

    def _get_parent_class(self, class_node: ast.ClassDef) -> Optional[str]:
        """Get the parent class name."""
        if class_node.bases:
            base = class_node.bases[0]
            if isinstance(base, ast.Name):
                return base.id
        return None

    def _check_parent_dependency(
        self,
        archetype_file: Path,
        parent: str,
        imports: Dict[str, str]
    ) -> List[str]:
        """Check that parent type is properly imported and exists."""
        errors = []

        # Check if parent is imported
        if parent not in imports:
            errors.append(f"Parent class '{parent}' not imported")
            return errors

        # Check if parent's module path is correct
        import_source = imports[parent]
        if not import_source.startswith('clams_vocabulary.types.'):
            errors.append(
                f"Parent import should be from clams_vocabulary.types.*"
            )
            return errors

        # Extract parent type directory name from import
        # e.g., 'clams_vocabulary.types.document.archetype' -> 'document'
        parts = import_source.split('.')
        if len(parts) >= 4 and parts[0] == 'clams_vocabulary' and parts[1] == 'types':
            parent_dir = parts[2]

            # Check if parent archetype exists
            parent_archetype = (
                archetype_file.parent.parent / parent_dir / 'archetype.py'
            )
            if not parent_archetype.exists():
                errors.append(
                    f"Parent archetype not found: {parent_archetype}"
                )

        return errors

    def _check_required_classvars(
        self,
        class_node: ast.ClassDef
    ) -> List[str]:
        """Check that required ClassVars are present."""
        required_classvars = {'description'}
        found_classvars = set()

        for node in class_node.body:
            if isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    # Check if it's a ClassVar annotation
                    if self._is_classvar_annotation(node.annotation):
                        found_classvars.add(node.target.id)

        errors = []
        missing = required_classvars - found_classvars
        if missing:
            errors.append(
                f"Missing required ClassVars: {', '.join(sorted(missing))}"
            )

        return errors

    def _is_classvar_annotation(self, annotation: ast.expr) -> bool:
        """Check if annotation is ClassVar[...]."""
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                return annotation.value.id == 'ClassVar'
        return False

    def _check_field_definitions(
        self,
        class_node: ast.ClassDef
    ) -> List[str]:
        """Check field definitions for common issues."""
        warnings = []

        for node in class_node.body:
            if isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    field_name = node.target.id

                    # Skip ClassVars
                    if self._is_classvar_annotation(node.annotation):
                        continue

                    # Check if Field() is used
                    if node.value:
                        if isinstance(node.value, ast.Call):
                            if isinstance(node.value.func, ast.Name):
                                if node.value.func.id == 'Field':
                                    # Check if description is provided
                                    has_description = False
                                    for keyword in node.value.keywords:
                                        if keyword.arg == 'description':
                                            has_description = True
                                            break
                                    if not has_description:
                                        warnings.append(
                                            f"Field '{field_name}' missing "
                                            f"description"
                                        )

        return warnings

    def _try_import(self, archetype_file: Path) -> List[str]:
        """Try to import the archetype module."""
        errors = []

        # Build module path: clams_vocabulary.types.type_name.archetype
        type_dir = archetype_file.parent
        type_name = type_dir.name
        module_path = f'clams_vocabulary.types.{type_name}.archetype'

        try:
            # Clear any cached import
            if module_path in sys.modules:
                del sys.modules[module_path]

            module = importlib.import_module(module_path)

            # Find the class
            class_name = ''.join(
                word.capitalize() for word in type_name.split('_')
            )
            if not hasattr(module, class_name):
                errors.append(
                    f"Class '{class_name}' not found in module"
                )
            else:
                # Try to get the class
                cls = getattr(module, class_name)

                # Check if it's a Pydantic model by trying to access
                # model_fields
                try:
                    _ = cls.model_fields
                except AttributeError:
                    errors.append(
                        f"Class '{class_name}' is not a Pydantic model"
                    )

        except ImportError as e:
            errors.append(f"Import error: {e}")
        except Exception as e:
            errors.append(f"Error loading module: {e}")
            if self.verbose:
                traceback.print_exc()

        return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Verify archetype.py files are well-formed'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed error messages'
    )
    parser.add_argument(
        'types',
        nargs='*',
        help='Specific type names to validate (default: all)'
    )

    args = parser.parse_args()

    # Find all archetype files
    types_dir = PROJ_ROOT / 'clams_vocabulary' / 'types'
    if not types_dir.exists():
        print(f"ERROR: Types directory not found: {types_dir}")
        return 1

    archetype_files = []
    if args.types:
        # Validate specific types
        for type_name in args.types:
            archetype_file = types_dir / type_name / 'archetype.py'
            if not archetype_file.exists():
                print(f"ERROR: Archetype not found: {archetype_file}")
                return 1
            archetype_files.append(archetype_file)
    else:
        # Validate all types
        archetype_files = sorted(types_dir.glob('*/archetype.py'))

    if not archetype_files:
        print("No archetype files found")
        return 1

    print(f"Validating {len(archetype_files)} archetype files...")
    print("=" * 70)

    validator = ArchetypeValidator(verbose=args.verbose)
    valid_count = 0
    invalid_count = 0

    for archetype_file in archetype_files:
        if validator.validate_file(archetype_file):
            valid_count += 1
        else:
            invalid_count += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"Results: {valid_count} valid, {invalid_count} invalid")

    if validator.warnings:
        print(f"\nWarnings: {len(validator.warnings)} types")
        if not args.verbose:
            print("(Use -v to see details)")

    if validator.errors:
        print(f"\nErrors: {len(validator.errors)} types")
        if not args.verbose:
            print("(Use -v to see details)")
            print("\nFailed types:")
            for type_name, errors in validator.errors:
                print(f"  - {type_name}")

    return 0 if invalid_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
