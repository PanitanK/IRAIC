import serial
import pynmea2

def parse_gga_sentence(data):
    try:
        sentence = pynmea2.parse(data)
        if isinstance(sentence, pynmea2.GGA):
            latitude = sentence.latitude
            longitude = sentence.longitude
            return latitude, longitude
        else:
            return None, None
    except pynmea2.ParseError as e:
        print(f"Error parsing GGA sentence: {e}")
        return None, None

def display_serial_data(com_port, baud_rate):
    try:
        ser = serial.Serial(com_port, baud_rate)
        print(f"Reading data from {com_port} at {baud_rate} baud rate...")

        while True:
            data = ser.readline().decode().strip()
            if data.startswith("$GNGGA"):
                print(f"Incoming GGA sentence: {data}")

                latitude, longitude = parse_gga_sentence(data)
                if latitude is not None and longitude is not None:
                    print(f"Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")

    except KeyboardInterrupt:
        print("\nExiting the program.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    # Use the correct COM port '/dev/ttyACM0' and the desired baud rate.
    com_port_to_read = 'COM8'
    baud_rate = 9600

    display_serial_data(com_port_to_read, baud_rate)