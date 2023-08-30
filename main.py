import threading
import queue
import GPS_Module

def main():
    com_port_to_read = 'COM8'  # Update with the correct COM port
    baud_rate = 9600

    # Create a queue to store GPS coordinates
    gps_queue = queue.Queue(maxsize=10)

    def gps_worker():
        try:
            GPS_Module.display_serial_data(com_port_to_read, baud_rate, gps_queue)
        except Exception as e:
            print(f"An error occurred in GPS thread: {e}")

    gps_thread = threading.Thread(target=gps_worker)
    gps_thread.start()

    while True:
        try:
            gps_data = gps_queue.get(timeout=10)  # Get GPS data from the queue with a timeout
            if gps_data is not None:
                latitude, longitude, timestamp = gps_data
                print(f"Received GPS Data: Latitude={latitude:.6f}, Longitude={longitude:.6f}, Timestamp={timestamp}")
                # Do something with the GPS data in main.py
        except queue.Empty:
            print("No GPS data received in the last 10 seconds.")

if __name__ == "__main__":
    main()
