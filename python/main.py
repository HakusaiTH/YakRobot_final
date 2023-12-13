import os
from fastapi import FastAPI, HTTPException, Request
from wether_and_pm25_module import weather, pm25
from chatbot_module import answer_question
from yak_dailog import detect_intent
from kaitom_tts import generate_and_play_audio
from yak_sentiment import analyze_sentiment 
from touchEvent import process_touch 

import firebase_admin
from firebase_admin import credentials, db, storage

# Initialize Firebase
cred = credentials.Certificate('D:\\sanbot_final\\pythonbackend\\my-robot-9fdff-firebase-adminsdk-37upn-709ad75796.json')
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'my-robot-9fdff.appspot.com',
    'databaseURL': 'https://my-robot-9fdff-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

user_room = "A1"
print("user_room:", user_room)

# Map for LED control
key_map_sl = {
    'ไฟภายในห้อง': 'led_1',
    'ไฟหลังห้อง': 'led_2',
    'ไฟนอกห้อง': 'led_3',
    'เปิด': 'ON',
    'ปิด': 'OFF'
}

# Function to control LED
def control_led(led_n, led_sta):  
    db_key = key_map_sl[led_n]
    db_value = key_map_sl[led_sta]
    led_ref = db.reference(f'/room/{user_room}/{db_key}/')
    led_ref.set(db_value)
    print(f"Set {led_sta} to {led_n}")

def robot_sentiment(content) :
    robot_sentiment_result = analyze_sentiment(content)

    print(robot_sentiment_result)
    robot_sentiment_ref = db.reference(f'/room/{user_room}/Robot/robot_status/sentiment')  # /room/{user_room}/Robot/robot_status/sentiment
    robot_sentiment_ref.set(robot_sentiment_result)

def upload_mp3_to_firebase(file_path, storage_path="audio"):
    bucket = storage.bucket()

    file_name = os.path.basename(file_path)
    destination_path = f"{storage_path}/{file_name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_name} uploaded to Firebase Storage at {destination_path}")

    robot_talk_ref = db.reference(f'/room/{user_room}/Robot/robot_status/talk_status')  # /room/{user_room}/Robot/robot_status/talk_status
    robot_talk_ref.set(True)

# Function to process robot
def process_robot(content,or_not):
    print("content:", content)
    if or_not :
        robot_sentiment(content)
    else :
        robot_sentiment_ref = db.reference(f'/room/{user_room}/Robot/robot_status/sentiment')  
        robot_sentiment_ref.set("H")
    
    if generate_and_play_audio(content) :
        upload_mp3_to_firebase("output.mp3")

# FastAPI instance
app = FastAPI()

# API endpoint
@app.post("/receive-data")
async def receive_data(request: Request):
    try:
        data = await request.json()
        talkvalue, sentence = data.get("somevalue"), data.get("sentence")
        print("Received data - somevalue:", talkvalue, "sentence:", sentence)

        # Process robot
        if talkvalue == "t" :
            print("touch robot")
            process_touch_result = process_touch(sentence)  # api อาจจะไม่พอ
            process_robot(process_touch_result,False)

            return {"status": "success", "message": "robot_call"}

        elif talkvalue == "gpt_call":
            print("user gpt input")
            process_robot(answer_question(sentence),True)
            return {"status": "success", "message": "robot_call"}
        else:
            value_intent = detect_intent(sentence)

            if value_intent == "gpt":
                print("gpt call")
                return {"status": "success", "message": "gpt_call"}
            
            elif value_intent in ["สภาพอากาศ", "pm25"]:
                print(f"{value_intent} call")
                process_robot(weather() if value_intent == "สภาพอากาศ" else pm25(),True)
                return {"status": "success", "message": "robot_call"}
            
            else:
                print("iot call")
                led_n, led_sta = value_intent[:2]
                return_result = f'{led_n} {led_sta}'
                process_robot(return_result,False)

                control_led(led_n, led_sta)
                return {"status": "success", "message": "robot_call"}
            
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
