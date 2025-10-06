import subprocess


RED: str = "\033[31m"
GREEN: str = "\033[32m"
YELLOW: str = "\033[33m"
BLUE: str = "\033[34m"
PURPLE: str = "\033[35m"
CYAN: str = "\033[36m"
NOCOLOR: str = "\033[0m"

def cpumon() -> dict:
    _sensors: subprocess.CompletedProcess = subprocess.run(args=["sensors"], capture_output=True, text=True)
    _sensors_stdout: list[str] = list(filter(lambda a: a.startswith("Package id"), _sensors.stdout.split("\n")))[0].split()
    _cpu_temp: float = float(_sensors_stdout[3].removesuffix("°C"))
    _cpu_high_temp: float = float(_sensors_stdout[6].removesuffix("°C,"))
    _cpu_crit_temp: float = float(_sensors_stdout[9].removesuffix("°C)"))
    if _cpu_temp < _cpu_high_temp:
        _cpu_temp: str = f"{GREEN}{_cpu_temp}{NOCOLOR}"
    elif _cpu_high_temp <= _cpu_temp < _cpu_crit_temp:
        _cpu_temp: str = f"{YELLOW}{_cpu_temp}{NOCOLOR}"
    else:
        _cpu_temp: str = f"{RED}{_cpu_temp}{NOCOLOR}"

    _mpstat: subprocess.CompletedProcess = subprocess.run(args=["mpstat"], capture_output=True, text=True)
    _not_idle: str = str(round(100 - float(_mpstat.stdout.split("\n")[3].split()[-1]), 2))

    return {"not_idle": _not_idle, "cpu_temp": _cpu_temp}
