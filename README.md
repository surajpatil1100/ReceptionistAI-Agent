# ReceptionistAI

An AI receptionist named **Shridevi** that handles appointment bookings for a private hospital. The agent interacts with customers in Hindi, collects their details, and saves the appointment information in a CSV file.

## Features
- **Speech-to-Text**: Converts customer speech into text using Vosk.
- **Natural Language Processing**: Uses Hugging Face's IndicBART model for Hindi language understanding.
- **Text-to-Speech**: Converts Shridevi's responses into speech using gTTS.
- **Appointment Scheduling**: Suggests available time slots and saves appointments in `appointments.csv`.

## Requirements
- Python 3.8+
- Libraries: `vosk`, `pyaudio`, `transformers`, `gtts`, `torch`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/surajpatil1100/ReceptionistAI-Agent/tree/main
