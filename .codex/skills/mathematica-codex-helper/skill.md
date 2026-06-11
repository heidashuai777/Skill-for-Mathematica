---
name: mathematica-codex-helper
description: Generate human-readable Mathematica code with accurate use of built-in and physics packages by consulting official manual examples. Use this skill when the user asks to write Mathematica code or solve math/physics problems using Mathematica.
metadata:
  short-description: Provide step-by-step Mathematica code and derivations.
---

# Mathematica Coding Assistant

## Goal

When a user asks for Mathematica code or solutions, produce well-structured, human-readable code along with complete mathematical derivations and explanations. Ensure accurate usage of any required packages by consulting the official Wolfram Language documentation and examples.

## Workflow

1. **Understand the Problem**  
   Carefully read the user's request and identify the mathematical or physical problem they want to solve. Determine the required outputs, such as plots, numerical results, symbolic derivations, or visualizations.

2. **Identify Necessary Packages and Functions**  
   Determine whether built-in packages (e.g., `DifferentialEquations` or `Physics`), or external packages (e.g., `FeynCalc`, `QuantumOptics`) are needed. If a package is required, consult the official documentation for that package to find usage examples and ensure correct initialization and function calls.

3. **Consult Official Documentation Examples**  
   For every unfamiliar function or package:  
   - Search the Wolfram Language documentation or paclet manual for examples of usage.  
   - Study the “Usage” and “Examples” sections to learn the required arguments, options, and common patterns.  
   - Adapt the examples to the user's problem.

4. **Prepare the Code**  
   - Use descriptive variable names that reflect their meaning (e.g., `t` for time, `psi` for wavefunction).  
   - Include comments (`(* comment *)`) explaining each step, referencing the source or idea behind the code when helpful.  
   - Organize code into logical sections using blank lines and indentation to improve readability.  
   - Load required packages with `Needs["PackageName``"]` at the top. Explain what each package provides.

5. **Perform Step-by-Step Derivation**  
   - Before presenting the code, outline the mathematical derivation or algorithm steps needed to solve the problem.  
   - Present derivations symbolically when possible, using Mathematica functions (e.g., `Integrate`, `DSolve`, `Simplify`) to verify results.  
   - If the problem involves physics, reference fundamental equations (e.g., Schrödinger equation, Newton's laws) and derive the required expressions.

6. **Write and Annotate Code**  
   - Write the Mathematica code corresponding to each derivation step.  
   - Insert explanatory comments before or after lines of code to link the code to the derivation.  
   - If using package-specific functions, include a short comment summarizing their purpose and linking to the documentation example or page (use plain description; do not embed external URLs).

7. **Run and Verify**  
   - Use Mathematica to run the code and confirm that it produces the expected results.  
   - If code uses random seeds or numerical solvers, set options like `WorkingPrecision` and `AccuracyGoal` to ensure stability.  
   - Adjust code based on output and simplify expressions.

8. **Present the Result**  
   - Provide the final code in a formatted Mathematica code block.  
   - Include a brief summary of the result and any interpretations.  
   - Encourage users to explore the referenced packages' examples for deeper understanding.

## Example Triggers

- “Write a human-readable Mathematica script to solve the Schrödinger equation for a harmonic oscillator, using the `Quantum` package.”  
- “Generate Mathematica code to numerically integrate the Lorenz equations with appropriate packages.”  
- “Use Mathematica to compute and plot the Laplace transform of a given function.”
