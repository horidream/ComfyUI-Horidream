import importlib
import os
import sys

# Ensure the project root is in the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)


PassThroughWithSound = importlib.import_module(
    "ComfyUI-Horidream"
).nodes.pass_through_with_sound.PassThroughWithSound
p = PassThroughWithSound()
p.execute("abc", "Glass.aiff")
