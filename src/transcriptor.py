from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pygame

# Inicializa pygame para reproducir el sonido
pygame.mixer.init()

def reproducir_sonido(wav_path):
    pygame.mixer.music.load(wav_path)
    pygame.mixer.music.play()

def detectar_palabras_clave():
    # Cargar el modelo de Vosk
    model = Model("c:/Users/ivost/OneDrive/Escritorio/speech-main/vosk-model-small-es-0.42")  # Cambia a la ruta donde descargaste el modelo
    recognizer = KaldiRecognizer(model, 16000)

    # Inicializar PyAudio para capturar audio en tiempo real
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2000)  # Tamaño de buffer ajustado para mejor latencia
    stream.start_stream()

    print("Escuchando palabras clave...")

    try:
        while True:
            # Leer datos del stream de audio
            data = stream.read(2000, exception_on_overflow=False)
            
            if len(data) == 0:
                continue

            # Reconocer el audio en tiempo real
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')

                if text:
                    print(f"Texto detectado: {text}")

                    # Verificar si se detecta la palabra clave "pico"
                    if "pico" in text.lower():
                        print("¡Palabra clave 'pico' detectada! Reproduciendo sonido...")
                        reproducir_sonido("c:/Users/ivost/OneDrive/Escritorio/speech-main/yaaina.wav")  # Ruta al archivo de sonido
                        
                    # Verificar si el usuario quiere detener el programa
                    if "detener" in text.lower():
                        print("Palabra 'detener' detectada. Terminando el programa.")
                        break
    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Deteniendo...")

    # Finalizar el stream de audio
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    detectar_palabras_clave()
