import serial
import pynmea2
import time

def parse_gga_sentence(data):
    try:
        sentence = pynmea2.parse(data)
        if isinstance(sentence, pynmea2.GGA):
            latitude = sentence.latitude
            longitude = sentence.longitude
            timestamp = sentence.timestamp.strftime("%Y-%m-%d %H:%M:%S") if sentence.timestamp else "N/A"
            print(sentence)
            return latitude, longitude, timestamp
        else:
            return None, None , None
    except pynmea2.ParseError as e:
        print(f"Error parsing GGA sentence: {e}")
        return None, None, None

def display_serial_data(com_port, baud_rate, gps_queue):
    while True:
        try:
            ser = serial.Serial(com_port, baud_rate)
            print(f"Reading data from {com_port} at {baud_rate} baud rate...")

            while True:
                data = ser.readline().decode().strip()
                if data.startswith("$GNGGA"):
                    print(f"Incoming GGA sentence: {data}")

                    latitude, longitude, timestamp = parse_gga_sentence(data)
                    if latitude is not None and longitude is not None:
                        gps_queue.put((latitude, longitude, timestamp))  # Put coordinates into the queue

        except FileNotFoundError as file_error:
            print(f"Error opening port '{com_port}': {file_error}")
            time.sleep(2)  # Wait for 2 seconds before retrying
        except KeyboardInterrupt:
            print("\nExiting the program.")
            break
        except Exception as e:
            print(f"There is an error occurred: {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
        finally:
            if ser and ser.is_open:
                ser.close()