from sys import argv
import os

# port mapping for uvicron
PORT: int = int(argv[1]) if len(argv) > 1 else None

# launch command for uvicorn
BASE_COMMAND = "uvicorn view:app --reload"

# launch fastapit server
if bool(PORT) is True:
    os.system(f"{BASE_COMMAND} --port {PORT}")
else:
    os.system(BASE_COMMAND)