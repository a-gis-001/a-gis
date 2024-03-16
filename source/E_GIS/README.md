This is an example of generating the `E_GIS` code base from a function in `A_GIS`.

Steps are

1. Distill the function in `A_GIS` to its most basic form (no comments/docstring).
2. Generate a hash of the function `<hash>`, e.g. `sha256_9ba676f506954f0fa7093aa63c4e72ff6f666101bf39150d86d5199c9ab4a9eb`.
3. Copy the function to `E_GIS/<hash>___Code__find_root/__init__.py`.

