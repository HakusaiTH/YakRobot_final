import random

def process_touch(traget) :
    if traget == "touching_hand" :
        dialog_hand_options = [
            "สวัสดี! คุณพบแขนของฉันแล้ว วันนี้ฉันจะช่วยคุณได้อย่างไร?",
            "สวัสดี! อย่าลังเลที่จะโต้ตอบกับแขนของฉัน คุณอยากทำสิ่งใดเป็นพิเศษหรือไม่",
            "ทำได้ดีมาก! คุณค้นพบแขนของฉันแล้ว หากคุณมีคำถามใดๆ ฉันพร้อมที่จะช่วยเหลือแล้ว",
            "อ๊ะ คุณจับแขนฉันไว้แล้ว! บอกฉันสิว่าคุณอยากสำรวจหรือเรียนรู้เกี่ยวกับอะไร",
            "ดีใจที่เห็นว่าคุณสนใจแขนของฉัน! หากมีสิ่งใดที่คุณอยากรู้หรือทำก็ถามได้เลย",
            "คุณพบจุดโต้ตอบแล้ว! ฉันจะทำอะไรให้คุณได้บ้างในขณะที่คุณจับแขนของฉัน",
            "การค้นพบที่ยอดเยี่ยม! หากมีฟังก์ชันใดที่คุณสงสัย อย่าลังเลที่จะถาม",
            "สวัสดี! ดูเหมือนว่าคุณจะจับแขนของฉันไว้ เราจะทำให้การโต้ตอบนี้สนุกสนานสำหรับคุณได้อย่างไร",
            "ยินดีต้อนรับสู่การสำรวจอาวุธ! หากมีคุณลักษณะเฉพาะที่คุณสงสัย ฉันพร้อมที่จะแบ่งปัน",
        ]

        return random.choice(dialog_hand_options)