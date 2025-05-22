import json
import platform
import subprocess
import re
def read_json(path):
    """
    Reads a JSON file and returns a dictionary with the data and a boolean
    indicating whether all required variables have values.

    Parameters
    ----------
    path : str
        The path to the JSON file.

    Returns
    -------
    dict
        A dictionary with the data and a boolean indicating whether all required
        variables have values. The boolean value is True if all required variables
        have values, and False otherwise.
    """
    data = json.dumps(path, indent=4, ensure_ascii=False)
    data = json.loads(data)
    if data["var_value_1"] == "" or data["var_value_2"] == "" or data["var_value_3"] == "" or data["var_value_4"] == "":
        var = False
    else:
        var = True
    return {"data": data, "var": var}

def list_active_printers():
    """
    Returns a list of active printers on the system.

    This function uses different methods for Windows, Linux, and macOS to
    determine which printers are active. On Windows, it uses the win32print
    module to query the print spooler. On Linux and macOS, it uses the
    lpstat command to get the status of the printers.

    Returns an empty list if no active printers are found or if the
    system is not supported.

    :return: A list of active printer names
    """
    system = platform.system()
    if system == "Windows":
        import win32print
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        # Filter only active printers
        active_printers = []
        for printer in printers:
            handle = win32print.OpenPrinter(printer[2])
            status = win32print.GetPrinter(handle, 2)  # Level 2 for detailed info
            if status['Status'] == 0:  # Status 0 usually means active/ready
                active_printers.append(printer[2])
            win32print.ClosePrinter(handle)
        return active_printers
    elif system in ["Linux", "Darwin"]:  # Darwin is macOS
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            active_printers = [
                line.split(" ")[1]
                for line in lines
                if "idle" in line.lower() or "printing" in line.lower()
            ]
            return active_printers
        else:
            return []
    else:
        return []
    

def extract_data(text):
    data = {}

    try:
        # Extraer Producto
        match_product = re.search(r'Producto:\s*(.+?)\s*Color:', text)
        if match_product:
            data["Producto"] = match_product.group(1).strip()

        # Extraer Color
        match_color = re.search(r'Color:\s*(.+?)\s*\d+\s*[\d.]+KG', text)
        if match_color:
            data["Color"] = match_color.group(1).strip()

        # Extraer Peso (antes de 'KG', toma el número)
        match_weight = re.search(r'([\d.]+)\s*KG', text)
        if match_weight:
            data["Peso"] = float(match_weight.group(1))

        # Extraer Lote
        match_lot = re.search(r'LOTE:\s*(\d+)', text)
        if match_lot:
            data["Lote"] = match_lot.group(1)
    except Exception as e:
        data = {}

    return data

