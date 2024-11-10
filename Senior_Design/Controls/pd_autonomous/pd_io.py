from typing import Tuple

"""
Functions to retrieve starting input values.
"""

def get_init_gain(dimension: str, filename: str = "init_val.txt") -> Tuple[float, float]:
    """
    This function parses init_val and returns initial gain values along the input dimension.

    Parameters:
    - dimension should be either (but exactly): "pitch" or "yaw"
    - filename: the name of the file where initial values are stored
        - "init_val.txt" if not provided

    Returns:
    - A tuple containing floating values for (Kp, Kd)
    """
    try:
        with open(filename, "r") as init_val:
            # Ignore header
            init_val.readline()

            # Tokenize init_val
            values = init_val.readline().strip().split(',')

            # Extract Kp and Kd for appropriate dimension
            if (dimension == "pitch"):
                Kp = float(values[0])
                Kd = float(values[1])
            elif (dimension == "yaw"):
                Kp = float(values[4])
                Kd = float(values[5])
            else:
                print ("Invalid dimension parameter.")
                return None

            return (Kp, Kd)
        
    except FileNotFoundError:
        print("File not found.")
        return None
    
    except ValueError:
        print("Error processing file. Please check the file format.")
        return None
    

def get_init_desired(dimension: str, filename: str = "init_val.txt") -> float | Tuple[float, float]:
    """
    This function parses init_val and returns desired values along the input dimension.

    Parameters:
    - dimension should be either (and exactly): "pitch" or "yaw"
    - filename: the name of the file where initial values are stored
        - "init_val.txt" if not provided

    Returns:
    - Either
        - A single float of desired_angle_yaw
        - A tuple containing floating values for (desired_depth, desired_angle_pitch)
    """
    try:
        with open(filename, "r") as init_val:
            # Ignore header
            init_val.readline()
            
            # Tokenize init_val
            values = init_val.readline().strip().split(',')

            # Extract Kp and Kd for appropriate dimension
            if (dimension == "pitch"):
                return (float(values[2]), float(values[3]))
            elif (dimension == "yaw"):
                return float(values[6])
            else:
                print ("Invalid dimension parameter.")
                return None
        
    except FileNotFoundError:
        print("File not found.")
        return None
    
    except ValueError:
        print("Error processing file. Please check the file format.")
        return None


def write_out(
    Kp: float,
    Kd: float,
    dimension: str
) -> None:
    """
    Appends new Kp/Kd values out to:
        * out_val_pitch.txt     if writing "pitch" data
        * out_val_yaw.txt       if writing "yaw" data

    Format is:
        Kp, Kd

    Note that data is appended to the end.
    """
    # Set valid dimension filename
    if (dimension not in ["pitch", "yaw"]):
        raise ValueError(f"Invalid dimension to write along: {dimension}")
    filename = f"out_val_{dimension}.txt"

    # Append values to the end of filename
    try:
        with open(filename, "a") as out_file:
            out_file.write(f"{Kp}, {Kd}\n")

    except:
        print(f"Error writing values out to {filename}.")