"""Updates BatterySpecs.txt with battery state of and charge battery voltage."""

def update_battery_file(file_path_progress: str,
                        file_path_static: str,
                        battery_percent: int,
                        battery_voltage: float) -> None:
    """Opens text file and writes battery percent and battery voltage.

    This is used by the Allsky software to add the values to the GUI
    that is hosted on the Allsky website under the system section.

    Args:
        file_path_progress (str): Path to text file in linux dir for progress
        bars
        file_path_static (str): Path to text file in linux dir for static data
        battery_percent (int): Battery percent to write into file
        battery_voltage (float): Battery voltage to write into file
    """
    with open(file_path_progress, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "Battery Percent" in line:
            parts = line.split("\t")
            parts[3] = f"{battery_percent}%"
            parts[5] = str(battery_percent)
            lines[i] = "\t".join(parts)


    with open(file_path_progress, "w") as file:
        file.writelines(lines)


    with open(file_path_static, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "Battery Voltage" in line:
            parts = line.split("\t")
            parts[3] = f"{battery_voltage}v"
            lines[i] = "\t".join(parts)


    with open(file_path_static, "w") as file:
        file.writelines(lines)
