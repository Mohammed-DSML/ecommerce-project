import subprocess
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parent
file_path = Path(sys.argv[1]).resolve()

relative_path = file_path.relative_to(project_root)
module = ".".join(relative_path.with_suffix("").parts)

subprocess.run(
    [sys.executable, "-m", module],
    cwd=project_root
)