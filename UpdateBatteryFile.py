"""Updates BatterySpecs.txt with battery state of and charge battery voltage."""

def update_battery_file(file_path: str, battery_percent: int,
                        battery_voltage: float) -> None:
    """Opens text file and writes battery percent and battery voltage.

    This is used by the Allsky software to add the values to the GUI
    that is hosted on the Allsky website under the system section.

    Args:
        file_path (str): Path to text file in linux dir
        battery_percent (int): Battery percent to write into file
        battery_voltage (float): Battery voltage to write into file
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "Battery Percent" in line:
            parts = line.split("\t")
            parts[3] = f"{battery_percent}%"
            parts[5] = str(battery_percent)
            lines[i] = "\t".join(parts)
        if "Battery Voltage" in line:
            parts = line.split("\t")
            parts[3] = f"{battery_voltage}v"
            parts[5] = str(battery_voltage)
            lines[i] = "\t".join(parts)


    with open(file_path, "w") as file:
        file.writelines(lines)
