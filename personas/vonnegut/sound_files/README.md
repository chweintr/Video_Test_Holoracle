# Sound Files

Place your audio assets here:

- `sequence_01.mp3` or `sequence_01.wav` - 8 minutes of Vonnegut-style speaking
- `transcript_01.txt` - Matching transcript for the audio file

**Audio Format Support:**
- **MP3**: Preferred format, automatically converted using pydub
- **WAV**: Also supported, processed directly with librosa
- **Other formats**: May work if ffmpeg is installed

The audio preparation script will process these files and create training chunks in the `chunks/` subdirectory.

**Note:** This should contain a Vonnegut-style voice recording, not authentic Vonnegut audio. The goal is to obtain estate permission for genuine voice training later.