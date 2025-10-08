import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from file_service.utils import safe_check_path

ROUTER = APIRouter(prefix="/files", tags=["files"])
ROOT_DIRECTORY = Path(os.environ.get("ROOT_DIRECTORY", "DEFAULT_ROOT"))


@ROUTER.post("/create")
def create_file(file_path: str, file_data: str):
    file_path: Path = ROOT_DIRECTORY / file_path
    safe_check_path(file_path, ROOT_DIRECTORY)
    try:
        with open(file_path, "w") as file:
            file.write(file_data)
            return {"message": f"File created at {file_path}"}
    except FileExistsError:
        raise HTTPException(status_code=400, detail="File already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ROUTER.get("/read")
def read_file(file_path: str):
    file_path = ROOT_DIRECTORY / file_path
    safe_check_path(file_path, ROOT_DIRECTORY)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        file_contents = None
        with open(file_path, "r") as file:
            file_contents = file.read()
        return file_contents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ROUTER.put("/update")
def rename_file(original_path: str, new_file_name: str):
    old_path = (ROOT_DIRECTORY / original_path).resolve()
    new_path = (ROOT_DIRECTORY / new_file_name).resolve()
    safe_check_path(new_path, ROOT_DIRECTORY)
    Path.rename(old_path, new_path)
    return new_path


@ROUTER.delete("/delete")
def delete_file(path: str):
    dir_path = (ROOT_DIRECTORY / path).resolve(strict=True)
    safe_check_path(dir_path, ROOT_DIRECTORY)

    if not dir_path.exists() or dir_path.is_dir():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        dir_path.unlink(missing_ok=True)
        return {"message": f"File deleted: {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
