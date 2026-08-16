"""پروفایل سخت‌افزار سیستم برای انتخاب مدل هوش مصنوعی."""

from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class HardwareProfile:
    """اطلاعات سخت‌افزار موردنیاز انتخاب مدل."""

    operating_system: str
    cpu_cores: int
    ram_gb: float
    gpu_name: str | None
    vram_gb: float | None
    disk_free_gb: float


def _ram_gb() -> float:
    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024**3), 1)
    except ImportError:
        return 0.0


def _gpu_info() -> tuple[str | None, float | None]:
    """اطلاعات NVIDIA را در صورت در دسترس بودن بدون اجبار به نصب CUDA می‌خواند."""
    executable = shutil.which("nvidia-smi")
    if not executable:
        return None, None
    try:
        import subprocess
        result = subprocess.run(
            [executable, "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        first = result.stdout.strip().splitlines()[0]
        name, memory = [item.strip() for item in first.split(",", 1)]
        return name, round(float(memory) / 1024, 1)
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None, None


def detect_hardware() -> HardwareProfile:
    """پروفایل سخت‌افزار فعلی را تولید می‌کند."""
    free = shutil.disk_usage(Path.home()).free / (1024**3)
    gpu, vram = _gpu_info()
    return HardwareProfile(
        operating_system=platform.platform(),
        cpu_cores=os.cpu_count() or 1,
        ram_gb=_ram_gb(),
        gpu_name=gpu,
        vram_gb=vram,
        disk_free_gb=round(free, 1),
    )


from pathlib import Path
