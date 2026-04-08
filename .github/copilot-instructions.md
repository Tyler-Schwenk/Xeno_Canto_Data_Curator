## Source of Truth (READ FIRST)

The resources in C:\Users\tyler\important\projects\Frog\2026\Xeno_Canto_Data_Curator\docs are authoritative and must be referenced before making changes.  
They must also be kept up to date as changes are made.

- docs/
  - Contains all project documentation, organized into subfolders
  - You may reorganize or improve documentation structure as needed
  - Documentation must reflect the current system behavior and data formats
- In-code docstrings
  - Must always be accurate and up to date
  - Treated as first-class documentation for future AI code companions

---

## Global Coding Rules (MANDATORY)

All code must comply with the following rules without exception:

1. Use clear, well-structured code that prioritizes readability, reuse, and correctness.
2. Avoid deep nesting:
   - Maximum of 3 indentation levels in most cases
   - Prefer early returns, helper functions, or refactoring over nesting
3. No magic numbers.
   - All constants must be named and centralized
4. No emojis anywhere in code, logs, comments, or documentation.
6. Reuse existing code whenever possible.
   - Reduce duplication
   - Fewer lines are acceptable only if clarity and maintainability are preserved
7. Optimize for long-term maintainability and readability.
8. Do not document change history or current changes and issues.
   - Only document how the system works today
   - Focus on data formats, schemas, APIs, and behavior
9. When modifying a file:
   - You must read the entire file
   - Ensure no compile, runtime, or logical errors are introduced
10. All functions and classes must have docstrings.
    - Follow PEP 257 conventions
    - Google or NumPy style is acceptable
    - Docstrings must describe:
      - Purpose
      - Inputs
      - Outputs
      - Side effects (if any)
