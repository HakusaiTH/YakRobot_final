import openai

api_key = "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"
openai.api_key = api_key

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        max_tokens=3800,
        stop=None,
        temperature=0.7,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content

def answer_question(user_input):
    message_log = [
          {"role": "system", "content": "Yak Robot เป็นหุ่นยนต์ที่จะทำให้ห้องของคุณสะดวกสบายยิ่งขึ้นด้วยความสามารถในการควบคุมผ่าน Internet of thing"},
          {"role": "system", "content": "เรายินดีเสมอที่จะช่วยเหลือหากมีคำถามหรืองานที่เกี่ยวข้องกับ Yak Robot และเทคโนโลยี Internet of thing"},
          {"role": "system", "content": "Yakhotel เป็นโรงแรมแห่งอนาคตที่ผสมผสานเทคโนโลยีหุ่นยนต์ อินเทอร์เน็ตของสรรพสิ่ง และความเป็นไทย..."},
    ]

    first_request = True

    if first_request:
        message_log.append({"role": "user", "content": user_input})
        response = send_message(message_log)
        message_log.append({"role": "assistant", "content": response})
        return response
        first_request = False
    else:
        message_log.append({"role": "user", "content": user_input})
        response = send_message(message_log)
        message_log.append({"role": "assistant", "content": response})
        return response
    
# print(answer_question("Yak Robot คืออะไร"))