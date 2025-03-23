# A_GIS Framework Rules

1. **Use full import names** - Always use complete import paths when importing modules.
   - Use explicit imports: `import A_GIS.Module1.Module2.function`
   - Never use `from` imports: ❌ `from A_GIS.Module1.Module2 import function`
   - Never use relative imports: ❌ `from .Module2 import function`
   - This ensures all dependencies are explicit and traceable

2. **Functions should be short** - Functions should be concise and rely on other functions within the A_GIS framework.

3. **Google style docstrings** - All functions must have proper Google style documentation.
   - Only one docstring per function file (in the function)
   - No module-level docstrings in function files
   - Test files can have module-level docstrings

4. **Function names start with verbs** - All function names should begin with an action verb.

5. **Local imports** - Imports should occur inside the deepest function where they're needed to reduce dependencies.
   - Exception: Test files can have all imports at the top level
   - Exception: Test helper functions can have imports at the top level

6. **One function per file** - Each function gets its own directory and file.

7. **Keyword-based arguments** - Function argument lists should start with `*` and use named parameters.

8. **Function call format** - Functions should be called as:
   ```python
   import A_GIS.Module1.Module2.do_function
   A_GIS.Module1.Module2.do_function(...)
   ```
   NOT as:
   ```python
   A_GIS.Module1.Module2.do_function.do_function(...)
   ```

9. **Tests location** - Tests should be in the directory:
   ```
   source/A_GIS/Module1/Module2/do_function/tests/__init__.py
   ```

10. **Module names are nouns** - Modules should always be nouns (e.g., "Visual") rather than verbs (e.g., "Visualize").

11. **Directory structure** - Each function gets its own directory, with the function defined in the `__init__.py` file of that directory.

Based on my analysis of the codebase and best practices, I would suggest adding these additional rules to the A_GIS Framework:

12. **Explicit Return Types** - All functions should have explicit return type hints in their docstrings and function signatures.

13. **Error Handling** - Functions should handle errors gracefully:
    - For functions returning structs:
      - Include an `error` field in the return struct
      - Return validation errors as strings in the `error` field instead of raising exceptions
      - Set `error` to empty string ("") when no errors occur
      - Set other fields to appropriate default values when an error occurs
    - For other functions:
      - Return `None` or raise appropriate exceptions with descriptive messages

14. **Test Coverage** - Each function should have comprehensive tests covering:
    - Happy path (expected inputs)
    - Edge cases (empty inputs, boundary conditions)
    - Error cases (invalid inputs, exceptions)

15. **Module Documentation** - Each module's `__init__.py` should have a module-level docstring explaining its purpose and usage.

16. **Private Functions** - Internal/helper functions should be prefixed with underscore and placed in their own directories under the main function's directory.

17. **Dependency Management** - External dependencies should be:
    - Listed in `requirements.txt`
    - Imported only when needed (lazy imports)
    - Have version constraints specified

18. **Code Style** - Follow PEP 8 guidelines with these specific rules:
    - Maximum line length of 88 characters (Black formatter default)
    - Use double quotes for strings
    - Use type hints for all function parameters and return values

19. **API Design** - Public functions should:
    - Have clear, descriptive names
    - Accept the most generic input type possible
    - Return consistent types
    - Be documented with examples

20. **Version Control** - Each function should:
    - Be in its own commit
    - Have a clear commit message following conventional commits format
    - Include tests in the same commit

21. **Image Processing**
    - Use numpy for efficient image operations
    - Support both PIL Image and numpy array inputs
    - Handle different image modes (RGB, RGBA)
    - Implement proper error handling for image operations
    - Use scikit-image for advanced image processing

22. **Image Comparison**
    - Implement MSE for basic comparison
    - Use SSIM for structural similarity
    - Set appropriate similarity thresholds
    - Handle different image sizes and modes
    - Return comparison results with metrics

23. **Test Images**
    - Store test images in a dedicated directory
    - Use consistent image formats
    - Document expected image properties
    - Version control test images
    - Include image generation scripts

24. **Error Handling for Struct-Returning Functions**
    - All functions returning structs must include an `error` field
    - Validation errors should be returned as strings in the `error` field
    - The `error` field should be empty ("") when no errors occur
    - When an error occurs:
      - Set `error` to a descriptive error message
      - Set other fields to appropriate default values
      - Return a valid struct with all fields populated
    - Example:
      ```python
      def my_function(*, arg1: str, arg2: int) -> "type['A_GIS.Code.make_struct']":
          error = ""
          if not isinstance(arg1, str):
              error = "arg1 must be a string"
          if not isinstance(arg2, int):
              error = "arg2 must be an integer"
          
          return A_GIS.Code.make_struct(
              result=some_value if not error else None,
              error=error,
              _arg1=arg1,
              _arg2=arg2
          )
      ```

## Image Comparison Patterns

The system uses a dual-metric approach for image comparison:

1. Mean Squared Error (MSE)
   - Lower values indicate more similar images
   - Used as a primary metric for small images (< 7x7 pixels)
   - Threshold of 100 for considering images different

2. Structural Similarity Index (SSIM)
   - Higher values indicate more similar images (max 1.0)
   - Requires minimum window size of 7x7 pixels
   - Default tolerance of 0.95 for considering images similar
   - Handles different image modes:
     - RGB: Compares all channels together
     - RGBA: Compares RGB and alpha channels separately
     - Grayscale: Direct comparison

3. Special Case Handling
   - Empty images: Returns perfect similarity (SSIM=1.0, MSE=0.0)
   - Small images (< 7x7): Uses MSE only with strict threshold
   - Different dimensions: Raises ValueError
   - Invalid input types: Raises TypeError

