---
package: ExpressionPOP
summary: 'Per-point attribute expressions for POPs: write lines like P = P + N * 0.1 and they compile to a GLSL compute shader, with local variables carried between lines. An alternative for the Math Combine POP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Writing expressions
    anchor: writing-expressions
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Point math in plain lines
    anchor: how-to-use-it
    does: 'Write one expression per line, such as `P = P + N * 0.1`, and read any point attribute of the input by its name.'
  - name: GPU compute shader from your lines
    anchor: how-to-use-it
    does: 'The lines compile into a GLSL compute shader on the GPU, so the math stays fast however many points come in.'
  - name: Local variables
    anchor: writing-expressions
    does: 'Typed locals such as `vec3 offset = N * 0.2` carry over to every later line, so a long calculation splits into readable steps.'
  - name: GLSL code and compile errors
    anchor: how-to-use-it
    does: 'The viewer switches between the points, the generated GLSL and the compile result, and the code and the result also come out as DATs.'
  - name: Replace a Math Combine POP
    anchor: how-to-use-it
    does: 'Offered in place of a Math Combine POP, wired into the same spot, when you create one with the alternatives shortcut held.'
---

## Why use it

Small per-point jobs come up all the time in POPs: push the points out along
their normals, colour them by position, scale them by some attribute. With
stock operators that is either a chain of Math Combine and Math Mix POPs, each
set up through menus and attribute scopes, or a GLSL POP where you write the
compute shader yourself, boilerplate and all.

ExpressionPOP lets you write the math the way you would say it. Each line is
one expression, like `P = P + N * 0.1`, and ExpressionPOP writes the GLSL
compute shader around your lines, so it runs on the GPU however many points
come in.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Or create a Math
   Combine POP with the alternatives shortcut held, pick ExpressionPOP, and it
   lands in that spot with the wiring kept.
2. Wire points into it: a Grid POP, a Sphere POP, the output of a particle
   system.
3. Type a line into **Attribute Expression**, for example `P = P + N * 0.1`.
   The left side is the attribute it writes, and on the right any point
   attribute of the input is read by its name.
4. Add more lines with the sequence's **+** button. They run in order, on every
   point.
5. Check the result. **Info** shows the compile result, so a typo shows up
   there as a shader error. Set **View** to Code to see the GLSL your lines
   turned into, or to Info to read the compile result in the viewer.

**Out Attrs** lists every attribute the lines write, collected from their left
sides, which is a quick check that a line writes what you meant.

## Writing expressions

The right side of a line is GLSL, so vector types, swizzles and the built-in
functions all work: `sin()`, `mix()`, `length()`, `normalize()` and the rest.

```glsl
P = P + N * 0.1
Color = vec4(P, 1)
```

The first line pushes every point along its normal, the second colours each
point by its position.

To split a longer calculation into steps, use a local. Switch on
**OutAttr/Local** for that line and give the left side a GLSL type; every later
line can then use the name:

1. `vec3 offset = N * 0.2`, with **OutAttr/Local** on.
2. `P = P + offset * length(P)`, with it off.

A line is split at its `=` signs, so comparisons that contain one (`==`, `>=`,
`<=`, `!=`) do not work inside a line. `<`, `>` and `step()` still do.

## Inputs and outputs

- **in1** (POP): the points to process.
- **out_pop** (POP): the points with the expressions applied.
- **out_code** (DAT): the generated shader code.
- **out_info** (DAT): the compile result.
