import uvicorn
from pathlib import Path

if __name__ == "__main__":


    print(Path("database.db").resolve())
    uvicorn.run('App.app:app', host='0.0.0.0', port=8000, reload=True)
