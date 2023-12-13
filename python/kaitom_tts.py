import iapp_ai

def generate_and_play_audio(text):
    apikey = 'YWa92l0PnnG3ViGTtiZfdtJTiaro6iCG' #YWa92l0PnnG3ViGTtiZfdtJTiaro6iCG

    api = iapp_ai.api(apikey)

    output_file = "output.mp3"
    response = api.thai_thaitts_kaitom(text)

    with open(output_file, "wb") as f:
        f.write(response.content)

    return True

# generate_and_play_audio("สภาพอากาศ")