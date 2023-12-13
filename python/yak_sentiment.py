import requests

def analyze_sentiment(text):
    url = f"https://api.iapp.co.th/sentimental-analysis/predict?text={text}"

    payload = {}
    headers = {
        'apikey': 'YWa92l0PnnG3ViGTtiZfdtJTiaro6iCG'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        label_mapping = {'pos': 'H', 'neg': 'S', 'neu': 'N'}
        label = response.json().get('label', '')
        return_result = label_mapping.get(label, label)
        return return_result
    
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None