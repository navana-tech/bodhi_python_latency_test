# Project Name

## How to Run

1. Create Virtual Environment

   ```bash
    python3 -m venv venv
   ```

2. Activate Virtual Environment

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install Requirements

   ```bash
   pip install -r requirements.txt

   ```

4. Add all wav files in audios folder for latency test.

5. Run Latency Test
   ```bash
   python non-streaming.py
   ```

## Requirements

- Python 3.x
