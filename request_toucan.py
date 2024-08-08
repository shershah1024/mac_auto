import requests


def synthesize_text_and_save_audio(text, output_file_path):
    url = "https://ybcj168u50s5p8-8080.proxy.runpod.net/synthesize/"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Write the response content to a file
        with open(output_file_path, 'wb') as f:
            f.write(response.content)
        print("Audio saved to:", output_file_path)
    else:
        print("Failed to synthesize audio. Status code:", response.status_code)
        print("Response:", response.text)


# Example usage:
synthesize_text_and_save_audio("Hello, this is a test message!", "synthesized_audio.wav")
