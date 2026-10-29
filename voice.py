import wave
from piper import PiperVoice

# 1. Path to your downloaded ONNX model
model_path = "en_US-amy-medium.onnx"

# 2. Load the voice model
voice = PiperVoice.load(model_path)

# 3. Open a target WAV file to save the speech
class Voice:
    def say_to_wav(words, output_file = "output.wav"):
        with wave.open(output_file, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)     # 2 bytes = 16-bit audio
            wav_file.setframerate(22050)
            # Synthesize text and write audio frames to the file
            voice.synthesize_wav(words, wav_file)

        print(f"Audio successfully saved to {output_file}")
        return output_file
