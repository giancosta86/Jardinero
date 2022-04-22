from typing import Optional

import requests
from info.gianlucacosta.eos.core.functional import ContinuationProvider
from info.gianlucacosta.eos.core.io.files.temporary import TemporaryPath, Uuid4TemporaryPath


def download_file_as_temp(
    url: str, continuation_provider: ContinuationProvider, chunk_bytes: int = 4 * 1024
) -> Optional[TemporaryPath]:
    """
    Downloads a file from the given url, letting the client cancel the request.

    As long as the given ContinuationProvider returns True, the download will proceed.

    Returns the temporary path to the downloaded file upon completion, None if the process
    was canceled.
    """
    temp_file_path = Uuid4TemporaryPath()
    request = requests.get(url, stream=True)

    with open(temp_file_path, "wb") as temp_file:
        for chunk in request.iter_content(chunk_size=chunk_bytes):
            if not continuation_provider():
                return None

            if chunk:
                temp_file.write(chunk)

    return temp_file_path
