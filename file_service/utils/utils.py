import traceback
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException


def safe_check_path(path: Path, base_path: Path) -> None:
    """
    Check to ensure the path contains the base path and that it does not
    resolve to some other directory.
    :param path: the path (folder) to check
    :param base_path: base path to check against
    :return:
    """
    try:
        resolved_path = path.resolve(strict=False)
        resolved_base_path = base_path.resolve(strict=False)

        if not path.parent.exists():
            raise HTTPException(
                status_code=404, detail="The folder being written to does not exist."
            )
        if not resolved_path.is_relative_to(resolved_base_path):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Invalid path being accessed."
            )
        if path.is_dir():
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="This route does not accept Folders.",
            )
        if "." not in path.name:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="This specified File does not have an extension.",
            )

    except Exception as arr:
        print("Unknown exception encountered of type ", type(arr))
        traceback.print_exc()
        raise arr
