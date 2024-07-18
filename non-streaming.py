import os
import time
import requests
import uuid
import mimetypes
from tabulate import tabulate

directory_path = "audios"
results = []  # Array to store results from API calls


# Function to send a single audio file with a delay
def send_audio_file_with_delay(file_path, delay):
    time.sleep(delay)

    with open(file_path, "rb") as file:
        files = {
            "audio_file": (
                os.path.basename(file_path),
                file,
                mimetypes.guess_type(file_path)[0],
            )
        }
        data = {
            "transaction_id": str(uuid.uuid4()),
            "model": "hi-general-v2-8khz",
            "aux": "TRUE",
        }

        headers = {
            "x-customer-id": "<Bodhi Customer ID>",
            "x-api-key": "<Bodhi API Key>",
        }

        start_time = time.time()  # Start time in seconds

        try:
            response = requests.post(
                url="https://bodhi.navana.ai/api/transcribe",
                files=files,
                data=data,
                headers=headers,
            )
            end_time = time.time()  # End time in seconds
            duration = end_time - start_time  # Calculate duration in seconds

            response_data = response.json()
            transcription = response_data["text"]
            request_time = response_data["aux_info"]["request_time"]
            received_request_time = response_data["aux_info"]["received_request_time"]

            # Calculate the difference between received_request_time and start_time in seconds
            difference_in_seconds = received_request_time - start_time

            # Push result to array
            results.append(
                {
                    "file_name": os.path.basename(file_path),
                    "network_latency": duration,
                    "request_time_at_server": request_time,
                    "request_time_at_client": difference_in_seconds,
                    "transcription": transcription,
                }
            )

            print(
                f"File {os.path.basename(file_path)}: API request took {duration} seconds, difference: {difference_in_seconds} seconds"
            )

        except Exception as error:
            print(f"Error sending file {os.path.basename(file_path)}:", error)


# Function to loop through all audio files in a directory
def process_audio_files(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                send_audio_file_with_delay(file_path, 0)

        # Print results as table after all requests finish
        print(tabulate(results, headers="keys", tablefmt="grid"))

    except Exception as error:
        print("Error reading directory:", error)


# Start processing audio files in the specified directory
process_audio_files(directory_path)
