import os
import shutil
import subprocess
from pathlib import Path


# =============================================================
# OPENCODE CLI
# =============================================================

def resolve_opencode_executable():
    """
    Возвращает путь к исполняемому файлу OpenCode CLI.

    На Windows npm ставит opencode как шимы
    (opencode.cmd / opencode.ps1), а не как .exe.
    subprocess с shell=False не умеет запускать шим,
    поэтому сначала ищем настоящий .exe, на который
    указывает opencode.cmd.
    """

    if os.name == "nt":

        executable = shutil.which("opencode.exe")

        if executable:
            return executable

        shim_path = shutil.which("opencode.cmd")

        if shim_path:

            exe_path = (
                Path(shim_path).parent
                / "node_modules"
                / "@opencode"
                / "cli"
                / "bin"
                / "opencode.exe"
            )

            if exe_path.is_file():
                return str(exe_path)

    executable = shutil.which("opencode")

    if executable:
        return executable

    raise RuntimeError(
        "opencode CLI не найден в PATH. "
        "Установите OpenCode и убедитесь, что команда "
        "`opencode --version` работает в этом терминале."
    )


def start_opencode(prompt, cwd):
    """
    Запускает `opencode run` в режиме JSON-событий.

    Каталог проекта передаётся через cwd:
    в opencode v2 у команды run нет флага --dir.
    """

    return subprocess.Popen(
        [
            resolve_opencode_executable(),
            "run",
            "--format",
            "json",
            prompt
        ],
        cwd=Path(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )
