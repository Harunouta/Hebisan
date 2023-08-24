import requests
import json
import time
#url
url="http://localhost:50021/"

def get_speaker_id(now_url):
    Speaker_id={}
    Core_Versions=requests.get(now_url+"core_versions")
    #print("Core_Versions:",Core_Versions.json())
    speakers=requests.get(now_url+"speakers",Core_Versions.json()[0])
    speakers_json=speakers.json()
    #name-style[name]-style[id]を取ってきたい
    for n in range(len(speakers_json)):
        speaker_nm=speakers_json[n]['name']
        for m in range(len(speakers_json[n]['styles'])):
            speaker_style=speakers_json[n]['styles'][m]['name']
            speaker_id=speakers_json[n]['styles'][m]['id']
            Speaker_id[speaker_nm+"-"+speaker_style]=speaker_id
    return Speaker_id
    
def play_words(now_url,sentence,chara_ID,voice_param_0,voice_param_1,voice_param_2,voice_param_3,voice_param_4,voice_param_5):
    res1=requests.post(now_url+"audio_query",params={"text":sentence.replace("'","").replace("/","").replace("_",""),"speaker":chara_ID})
    res2=requests.post(now_url+"accent_phrases",params={"text":sentence,"speaker":chara_ID,"is_kana":"True"})
    old_json=res1.json()
    aques_json=res2.json()
    #param書き換え
    old_json["accent_phrases"]=aques_json
    old_json["speedScale"]=voice_param_0
    old_json["pitchScale"]=voice_param_1
    old_json["intonationScale"]=voice_param_2
    old_json["volumeScale"]=voice_param_3
    old_json["prePhonemeLength"]=voice_param_4
    old_json["postPhonemeLength"]=voice_param_5
    new_json=json.dumps(old_json)
    res3=requests.post(now_url+"synthesis",params={"speaker":chara_ID},data=new_json)
    data=res3.content
    with open("test.wav",mode="wb")as f:
        f.write(res3.content)
    #閉じる
    return 0

#print(get_speaker_id("http://localhost:50021/"))
#play_words(url,"ナ'ガノ/シンカ'ンセン/シャリョウセ'ンタア",1)