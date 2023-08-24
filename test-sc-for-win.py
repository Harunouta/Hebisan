import sys
import spacy
import ginza
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

from mymodules.accmake import accmake as AM
from mymodules.JoinJoin import JoinVoiceVoxForWin as JV

#初期設定
nlp=spacy.load("ja_ginza")
ginza.set_split_mode(nlp,"C")
soft_flug=0#2:VOICEVOX,1:COEIROINK
voice={}
url=""
#accent関連変数
display_list=[]
display_list_acc=[]
display_list_span=[]
display_list_span_canmove=[]
display_list_aModType=[]
display_list_aConType=[]
#accent関連変数_
aModType=["*","M1@1","M1@0","M4@1","M2@1","M2@2","M2@0"]
aConType=["独立","*",'C1','C2','C3','C4','C5',
 'P1','P2', 'P4', 'P6', 'P13', 'P14',
 'F1','F2','F2@-2','F2@-1','F2@0', 'F2@1', 'F2@2','F2@3', 'F2@4',
 'F3@-1','F3@0', 'F3@1', 'F3@2',
 'F4@-2','F4@-1', 'F4@0', 'F4@1','F4@2',
 'F6@1=|=-1','F6@0=|=-2']#%部分は判定された品詞に合わせて選ぶ。

#挙動制御用変数
display=0
acc_display_flug=0
serectwiget=[]
serecttext=[]
##音声選択部分
voice_list=["メニューバーの設定から設定してください","ここには","voicevoxや","coelroinkの","スタイルを","表示させたい"]
voice_app_list=[]
voice_param=[]

#今分かち書きする部分の指定
nowindex=0

#voice選択
def select_voice(event):
    pass

#コピペ
def Select_text(event):
    global serecttext
    if len(serecttext)!=0:
        serecttext=[]
    serecttext.append(event.widget)

def Copy_command(self):
    global serecttext,root
    if len(serecttext)==1:
        append_text=serecttext[0].get()
        root.clipboard_append(append_text)
    
def Paste_command(self):
    global serecttext,root
    if len(serecttext)==1:
        serecttext[0].delete(0,tk.END)
        serecttext[0].insert(0,root.clipboard_get())

#voicevox設定
def join_voicevox():
    global root,voice_list,voicevox_frame,voicevox_entry,chara_list,soft_flug
    dlg_modal=tk.Toplevel(root)
    dlg_modal.title("VOICEVOXの設定")
    dlg_modal.geometry("500x300")
    dlg_modal.grab_set()
    dlg_modal.focus_set()
    #以下フレーム等等
    voicevox_frame=ttk.Frame(dlg_modal)
    voicevox_label=ttk.Label(voicevox_frame,text="VOICEVOXAPI：")
    voicevox_entry=ttk.Entry(voicevox_frame,width=25)
    voicevox_entry.insert(tk.END,"http://localhost:50021/")
    voicevox_button=ttk.Button(voicevox_frame,text="キャラ取得",command=get_character)
    soft_flug=2
    #各種ウィジェットの設定
    """
        0 1_2
    0
    1
    ...
    """
    voicevox_frame.grid(row=0,column=0)
    voicevox_label.grid(row=0,column=0)
    voicevox_entry.grid(row=0,column=1)
    voicevox_button.grid(row=1,columns=1)
    #キャラ表示部分
    voicevox_chara_frame=ttk.Frame(dlg_modal)
    chara_list_var=tk.StringVar(value=voice_list)
    chara_list=tk.Listbox(voicevox_chara_frame,listvariable=chara_list_var,height=10)
    #各種ウィジェットの設定
    """
        0 1_2
    0
    1
    ...
    """
    voicevox_chara_frame.grid(row=0,column=1)
    chara_list.grid(row=0,column=0)
    
    
def join_coeiro():
    global root,voice_list,voicevox_frame,voicevox_entry,chara_list,soft_flug
    dlg_modal=tk.Toplevel(root)
    dlg_modal.title("COEIROINK設定")
    dlg_modal.geometry("750x300")
    dlg_modal.grab_set()
    dlg_modal.focus_set()
    #以下フレーム等等
    voicevox_frame=ttk.Frame(dlg_modal)
    voicevox_label=ttk.Label(voicevox_frame,text="COEIROINK(V1は末尾が1,V2は末尾が2)：")
    voicevox_entry=ttk.Entry(voicevox_frame,width=25)
    voicevox_entry.insert(tk.END,"http://localhost:50031/")#version2は"http://localhost:50032/"
    voicevox_button=ttk.Button(voicevox_frame,text="キャラ取得",command=get_character)
    soft_flug=1
    #各種ウィジェットの設定
    """
        0 1_2
    0
    1
    ...
    """
    voicevox_frame.grid(row=0,column=0)
    voicevox_label.grid(row=0,column=0)
    voicevox_entry.grid(row=0,column=1)
    voicevox_button.grid(row=1,columns=1)
    #キャラ表示部分
    voicevox_chara_frame=ttk.Frame(dlg_modal)
    chara_list_var=tk.StringVar(value=voice_list)
    chara_list=tk.Listbox(voicevox_chara_frame,listvariable=chara_list_var,height=10)
    #各種ウィジェットの設定
    """
        0 1_2
    0
    1
    ...
    """
    voicevox_chara_frame.grid(row=0,column=1)
    chara_list.grid(row=0,column=0)
    
    
    
#キャラ取得部分
def get_character():
    global voice_list,voicevox_entry,voice,chara_list_var,chara_list,voice_combobox,soft_flug,url
    url=voicevox_entry.get()
    if soft_flug==2:
        voice=JV.get_speaker_id(url)
    else:
        pass
    voice_list=list(voice.keys())
    chara_list_var=tk.StringVar(value=voice_list)
    chara_list["listvariable"]=chara_list_var
    voice_combobox["values"]=voice_list
    voice_combobox.set(voice_list[0])


#再生
def play():
    global voice_param,voice_combobox,soft_flug
    voice_param=[speed.get(),tone.get(),high_low.get(),Volumne.get(),start_none.get(),end_none.get()]
    ##このタイミングでアクセント合成もしないといけない(読み(これはlist管理していないから作る)、アクセント核,Con,Modを前部持って行く)
    display_list_kana=[]
    for n in range(len(display_list)):
        display_list_kana.append(display_list[n]["text"])
    Talk_sentence=AM.sentence_compound(display_list_kana,display_list_acc,display_list_aModType,display_list_aConType,display_list_span)
    #print(Talk_sentence)
    if soft_flug==2:
        JV.play_words(url,Talk_sentence,voice[voice_combobox.get()],\
    voice_param[0],voice_param[1],voice_param[2],voice_param[3],voice_param[4],voice_param[5])
        pass
    
#この単語だけ再生
def play_word():
    global voice_param,voice_combobox,serectwiget,soft_flug,voice
    voice_param=[speed.get(),tone.get(),high_low.get(),Volumne.get(),start_none.get(),end_none.get()]
##このタイミングでアクセント合成もしないといけない(ここで必要なのは地味にアクセント核だけ)
    now_kana=serectwiget[-1]["text"]
    now_acc=display_list_acc[display_list.index(serectwiget[-1])]
    Talk_sentence=AM.word_compound(now_kana,now_acc)
    if soft_flug==0:
        JV.play_words(url,Talk_sentence,voice[voice_combobox.get()],\
    voice_param[0],voice_param[1],voice_param[2],voice_param[3],voice_param[4],voice_param[5])
        #print(Talk_sentence)
        #print(voice[voice_combobox.get()])
    pass
    
    
#アクセント表示(アクセント核を変更するたびに追加)
def acc_show():
    global display_list_acc,serectwiget,ac_spinbix,ac_Canvas,acc_display_flug,var
    new_text=ac_kana_entry.get()
    acc_num=int(ac_spinbix.get())
    if acc_num >len(AM.kana2readly_kana(new_text)):
        acc_num=len(AM.kana2readly_kana(new_text))
    display_list_acc[display_list.index(serectwiget[-1])]=acc_num
    var.set(acc_num)
    #表示
    startpoint_up=[10,25]
    startpoint_down=[10,75]
    point_width=int(180/len(AM.kana2readly_kana(new_text)))
    if acc_display_flug!=0:
        #削除処理
        ac_Canvas.delete("acc")
    acc_display_flug=1
    #表示
    XY=[5,25]
    #描画
    for n in range(len(AM.kana2readly_kana(new_text))):
        if acc_num==1:
            if n ==0:
                XY=XY+[point_width*n+10,25]
            else:
                XY=XY+[point_width*n+10,75]
        elif acc_num==0:
            if n ==0:
                XY=[5,75]
                XY=XY+[point_width*n+10,75]
            else:
                XY=XY+[point_width*n+10,25]
        else:
            if n ==0:
                XY=[5,75]
                XY=XY+[point_width*n+10,75]
            elif n+1>acc_num:
                XY=XY+[point_width*n+10,75]
            else:
                XY=XY+[point_width*n+10,25]
    def line_acc(*xy):
        global ac_Canvas
        ac_Canvas.create_line(xy,tag="acc")
    line_acc(*XY)
    
#単語の読みとアクセントを変える部分を表示する
def open_acc(event):
    global serectwiget,button_apply,acCon_combobox, acMod_combobox
    button_apply["state"]="normal"
    ac_spinbix["state"]="normal"
    acCon_combobox["state"]="normal"
    acMod_combobox["state"]="normal"
    play_word_button["state"]="normal"
    #初期値格納
    ac_kana_entry.delete(0,tk.END)
    ac_kana_entry.insert(0,event.widget.cget("text"))
    var.set(display_list_acc[display_list.index(event.widget)])
    acCon_combobox.set(display_list_aConType[display_list.index(event.widget)])
    acMod_combobox.set(display_list_aModType[display_list.index(event.widget)])
    if len(serectwiget)!=0:
        serectwiget=[]
    serectwiget.append(event.widget)
    #もし係り受け変更可能だったらボタン押す
    if display_list_span_canmove[display_list.index(event.widget)]==1:
        span_move_down["state"]="normal"
        span_move_up["state"]="disable"
    elif display_list_span_canmove[display_list.index(event.widget)]==2:
        span_move_up["state"]="normal"
        span_move_down["state"]="disable"
    elif display_list_span_canmove[display_list.index(event.widget)]==3:
        span_move_up["state"]="normal"
        span_move_down["state"]="normal"
    else:
        span_move_up["state"]="disable"
        span_move_down["state"]="disable"
    #アクセント核表示部分をやっておく
    acc_show()

#単語の読みとアクセントの変更を反映する
def apply_acc():
    global serectwiget,display_list_aModType,display_list_aConType
    new_text=ac_kana_entry.get()
    serectwiget[-1]["text"]="".join(AM.kana2readly_kana(new_text))
    acc_num=int(ac_spinbix.get())
    if acc_num >len(AM.kana2readly_kana(new_text)):
        acc_num=len(AM.kana2readly_kana(new_text))
    display_list_acc[display_list.index(serectwiget[-1])]=acc_num
    display_list_aModType[display_list.index(serectwiget[-1])]=acMod_combobox.get()
    display_list_aConType[display_list.index(serectwiget[-1])]=acCon_combobox.get()
    
    #次押すまで待機
    span_move_up["state"]="disable"
    span_move_down["state"]="disable"
    button_apply["state"]="disable"
    acCon_combobox["state"]="disable"
    acMod_combobox["state"]="disable"
    play_word_button["state"]="disable"
    
#係り受け移動部分(上)
def apply_span_up():
    global serectwiget,display_list_span_canmove,display_list_span,display_list
    
    #display_list_span_canmoveとdisplay_list_spanの更新(ここで全部やる)
    #display_list_spanの更新
    display_list_span[display_list.index(serectwiget[-1])]=display_list_span[display_list.index(serectwiget[-1])]-1
    #空数字が無いように穴埋め
    sorted_span=sorted(list(set(display_list_span)),reverse=False)
    for n in range(len(display_list_span)):
        display_list_span[n]=sorted_span.index(display_list_span[n])
        
    #display_list_span_canmoveのふり直し
    display_list_span_canmove=[]
    now_index=-1
    for n in range(len(display_list_span)):
        if display_list_span[n]!=now_index:
            if n!=0:
                display_list_span_canmove[n-1]=display_list_span_canmove[n-1]+1
            display_list_span_canmove.append(2)
            now_index=display_list_span[n]
        else:
            display_list_span_canmove.append(0)
    display_list_span_canmove[-1]=display_list_span_canmove[-1]+1
            
    #アクセント・読み現状の反映部分
    new_text=ac_kana_entry.get()
    serectwiget[-1]["text"]="".join(AM.kana2readly_kana(new_text))
    acc_num=int(ac_spinbix.get())
    if acc_num >len(AM.kana2readly_kana(new_text)):
        acc_num=len(AM.kana2readly_kana(new_text))
    display_list_acc[display_list.index(serectwiget[-1])]=acc_num
    display_list_aModType[display_list.index(serectwiget[-1])]=acMod_combobox.get()
    display_list_aConType[display_list.index(serectwiget[-1])]=acCon_combobox.get()
    
    #ボタンふり直し部分(現状の値格納)
    new_kana_list=[]
    for n in range(len(display_list)):
        new_kana_list.append(display_list[n]["text"])
    #ボタンふり直し部分破壊
    for n in range(len(display_list)):
        display_list[n].destroy()
    #新規作成分を適用
    display_list=[]
    for n in range(len(new_kana_list)):
        #display_list_span_canmoveから動きを確認
        display_list.append(ttk.Button(span_tree[display_list_span[n]],text=new_kana_list[n]))
        display_list[-1].bind("<ButtonPress>",open_acc)
        display_list[-1].pack(side="left")
    #次押すまで待機
    span_move_up["state"]="disable"
    span_move_down["state"]="disable"
    button_apply["state"]="disable"
    acCon_combobox["state"]="disable"
    acMod_combobox["state"]="disable"
    play_word_button["state"]="disable"
    
#係り受け移動部分(下)
def apply_span_down():
    global serectwiget,display_list_span_canmove,display_list_span,display_list
    
    #display_list_span_canmoveとdisplay_list_spanの更新(ここで全部やる)
    #display_list_spanの更新
    display_list_span[display_list.index(serectwiget[-1])]=display_list_span[display_list.index(serectwiget[-1])]+1
    #空数字が無いように穴埋め
    sorted_span=sorted(list(set(display_list_span)),reverse=False)
    for n in range(len(display_list_span)):
        display_list_span[n]=sorted_span.index(display_list_span[n])
        
    #display_list_span_canmoveのふり直し
    display_list_span_canmove=[]
    now_index=-1
    for n in range(len(display_list_span)):
        if display_list_span[n]!=now_index:
            if n!=0:
                display_list_span_canmove[n-1]=display_list_span_canmove[n-1]+1
            display_list_span_canmove.append(2)
            now_index=display_list_span[n]
        else:
            display_list_span_canmove.append(0)
    display_list_span_canmove[-1]=display_list_span_canmove[-1]+1
            
    #アクセント・読み現状の反映部分
    new_text=ac_kana_entry.get()
    serectwiget[-1]["text"]="".join(AM.kana2readly_kana(new_text))
    acc_num=int(ac_spinbix.get())
    if acc_num >len(AM.kana2readly_kana(new_text)):
        acc_num=len(AM.kana2readly_kana(new_text))
    display_list_acc[display_list.index(serectwiget[-1])]=acc_num
    display_list_aModType[display_list.index(serectwiget[-1])]=acMod_combobox.get()
    display_list_aConType[display_list.index(serectwiget[-1])]=acCon_combobox.get()
    
    #ボタンふり直し部分(現状の値格納)
    new_kana_list=[]
    for n in range(len(display_list)):
        new_kana_list.append(display_list[n]["text"])
    #ボタンふり直し部分破壊
    for n in range(len(display_list)):
        display_list[n].destroy()
    #新規作成分を適用
    display_list=[]
    for n in range(len(new_kana_list)):
        #display_list_span_canmoveから動きを確認
        display_list.append(ttk.Button(span_tree[display_list_span[n]],text=new_kana_list[n]))
        display_list[-1].bind("<ButtonPress>",open_acc)
        display_list[-1].pack(side="left")
    #次押すまで待機
    span_move_up["state"]="disable"
    span_move_down["state"]="disable"
    button_apply["state"]="disable"
    acCon_combobox["state"]="disable"
    acMod_combobox["state"]="disable"
    play_word_button["state"]="disable"
    
#係り受け見る部分
def kakariuke():
    span_flug=0
    global display_list,display,Play_audio,Split_mode_combobox,display_list_aModType,display_list_aConType
    mode=Split_mode_combobox.get()
    ginza.set_split_mode(nlp,mode)
    #次押すまで待機
    span_move_up["state"]="disable"
    span_move_down["state"]="disable"
    button_apply["state"]="disable"
    acCon_combobox["state"]="disable"
    acMod_combobox["state"]="disable"
    play_word_button["state"]="disable"
    #有効にするボタン
    Play_audio["state"]="normal"
    speed["state"]="normal"
    tone["state"]="normal"
    high_low["state"]="normal"
    Volumne["state"]="normal"
    start_none["state"]="normal"
    end_none["state"]="normal"

    
    if display!=0:
        for n in range(len(display_list)):
            display_list[n].destroy()
    else:
        display=1
    display_list=[]
    text=entry.get().replace("\n","").replace("\r","").replace("\r\n","")
    if text !="":
        doc=nlp(text)
        frame_tree_num=0
        for sent in doc.sents:
            for span in ginza.bunsetu_spans(sent):
                display_list_span_canmove.append(2)
                span_flug=1
                #係り受け句内
                for token in span:
                    Yomi=token.morph.get("Reading")[-1].split("/")
                    if len(Yomi)==4:
                        if Yomi[0]!="":
                            display_list.append(ttk.Button(span_tree[frame_tree_num],text=Yomi[0]))
                        else:
                            display_list.append(ttk.Button(span_tree[frame_tree_num],text="ホニャララ"))
                        display_list[-1].bind("<ButtonPress>",open_acc)
                        display_list[-1].pack(side="left")
                        ##このタイミングでアクセント格納もしないといけない
                        if Yomi[1]!="":
                            display_list_acc.append(int(Yomi[1].split(".")[0]))
                        else:
                            display_list_acc.append(0)
                        if Yomi[3]!="":
                            display_list_aModType.append(Yomi[3])
                        else:
                            display_list_aModType.append("*")
                        display_list_aConType.append("C4")
                        if Yomi[2]!="":
                            if "," in Yomi[2]:
                                #この仕様きつい（途中で切れてしまう「動詞F6@M,K」とりあえず初期値を採用しちゃうけど、辞書の格納を検討する）
                                Con=Yomi[2].split(",")
                                if len(Con)==1:
                                    display_list_aConType[-1]=Con.split("%")[1]
                                else:
                                    for n in range(len(Con)):
                                        if token.pos_.split("-")[0] in Con[n]:
                                            display_list_aConType[-1]=Con[n].split("%")[1]
                            display_list_aConType[-1]=Yomi[2]
                        else:
                            display_list_aConType[-1]=("C4")
                    else:
                        display_list.append(ttk.Button(span_tree[frame_tree_num],text=Yomi[0]))
                        display_list[-1].bind("<ButtonPress>",open_acc)
                        display_list[-1].pack(side="left")
                        ##このタイミングでアクセント格納もしないといけない
                        display_list_acc.append(0)
                        display_list_aModType.append("*")
                        display_list_aConType.append("C4")
                    display_list_span.append(frame_tree_num)
                    if span_flug!=1:
                        display_list_span_canmove.append(0)
                    else:
                        span_flug=0
                #それ以外
                #係り受け句内最終であるフラグ
                display_list_span_canmove[-1]=display_list_span_canmove[-1]+1
                frame_tree_num+=1

#rootフレームの設定
root = tk.Tk()
root.title("係り受け表示テスト")
root.geometry("1280x720")#ここ小文字のxなの、激おこ。

#メニューバー    
menu=tk.Menu(root)
root.config(menu=menu)
menu_setting=tk.Menu(root)
menu_editing=tk.Menu(root)
menu.add_cascade(label="編集",menu=menu_editing)
menu_editing.add_command(label="コピー",command=Copy_command,accelerator="Command+c")#windowsはCtrにちゃんと書き換えること
menu_editing.add_command(label="ペースト",command=Paste_command,accelerator="Command+v")#windowsはCtrにちゃんと書き換えること
menu_editing.bind_all("<Command-c>",Copy_command)
menu_editing.bind_all("<Command-v>",Paste_command,)
menu.add_cascade(label="設定",menu=menu_setting)
menu_setting.add_command(label="VoiceVox設定",command=join_voicevox)
#menu_setting.add_command(label="COEIROINK設定",command=join_coeiro)

#フレームの作成と位置
#分かち書き部分:デフォルトは50句入るようにする
#Canvas-上下左右バー-Frame-Frame(50句)
Canvas_tree=tk.Canvas(root,
    width=100,
    height=300,
    scrollregion=(0, 0, 1000, 1000)
)
frame_wakati=ttk.Frame(Canvas_tree)
frame_wakati.grid()

# 水平方向のスクロールバーを作成
xbar = tk.Scrollbar(
    root,  # 親ウィジェット
    orient=tk.HORIZONTAL,  # バーの方向
)
# 垂直方向のスクロールバーを作成
ybar = tk.Scrollbar(
    root,  # 親ウィジェット
    orient=tk.VERTICAL,  # バーの方向
)

#水平方向の設定
xbar.config(
    command=Canvas_tree.xview
)
Canvas_tree.config(
    xscrollcommand=xbar.set
)
#垂直方向の設定
ybar.config(
    command=Canvas_tree.yview
)
Canvas_tree.config(
    yscrollcommand=ybar.set
)
span_tree=[]
for n in range(50):
    span_tree.append(ttk.Frame(frame_wakati))
    span_tree[-1].grid(column=1,row=n,sticky=tk.NSEW,padx=5,pady=10)
    
#スクロールを実装したい。
Canvas_tree.create_window((0, 0), window=frame_wakati, anchor="nw")


#文章入力部分
frame=ttk.Frame(root)
#各種ウィジェットの設定
#=入力セット=#
voice_combobox=ttk.Combobox(frame,values=voice_list,state="readonly")
voice_combobox.set(voice_list[0])
voice_combobox.bind("<<ComboboxSelected>>",select_voice)
Split_mode_combobox=ttk.Combobox(frame,values=["A","B","C"],state="readonly")
Split_mode_combobox.set("C")
label=ttk.Label(frame,text="解析したい文章：")
entry=ttk.Entry(frame,width=50)
entry.bind("<ButtonPress>",Select_text)
button_execute=ttk.Button(frame,text="分かち書き",command=kakariuke)
#==#


#各種ウィジェットの設定
"""
 0 1_2
0
1
...
"""
voice_combobox.grid(row=0,column=0)
Split_mode_combobox.grid(row=0,column=1)
label.grid(row=1,column=0)
entry.grid(row=1,column=1)
button_execute.grid(row=2,columns=1)


#音速調整等部分
frame_setup=ttk.Frame(root)
Play_audio=ttk.Button(frame_setup,text="wav出力",state="disable",command=play)
#話速 0.5 1 2
sp= tk.IntVar(root)
sp.set(1)  #初期値セット
speed_label=ttk.Label(frame_setup,text="話速：")
speed=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=0.5,to=2,variable=sp,resolution=0.01,state="disable")
#音高 -0.15 0 0.15
tn= tk.IntVar(root)
tn.set(0)  #初期値セット
tone_label=ttk.Label(frame_setup,text="音高：")
tone=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=-0.15,to=0.15,variable=tn,resolution=0.01,state="disable")
#抑揚 0 1 2
hl= tk.IntVar(root)
hl.set(1)  #初期値セット
high_low_label=ttk.Label(frame_setup,text="抑揚：")
high_low=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=0,to=2,variable=hl,resolution=0.01,state="disable")
#音量 0 1 2
Vm= tk.IntVar(root)
Vm.set(1)  #初期値セット
Volumne_label=ttk.Label(frame_setup,text="音量：")
Volumne=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=0,to=2,variable=Vm,resolution=0.01,state="disable")
#開始無音 0 0.10 1.50
st_none= tk.IntVar(root)
st_none.set(0.10)  #初期値セット
start_none_label=ttk.Label(frame_setup,text="開始無音：")
start_none=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=0,to=1.50,variable=st_none,resolution=0.01,state="disable")
#終了無音 0 0.10 1.50
ed_none= tk.IntVar(root)
ed_none.set(0.10)  #初期値セット
end_none_label=ttk.Label(frame_setup,text="終了無音：")
end_none=tk.Scale(frame_setup,orient=tk.HORIZONTAL,from_=0,to=1.50,variable=ed_none,resolution=0.01,state="disable")
#各種ウィジェットの設定
"""
 0 1_2
0
1
...
"""
Play_audio.grid(row=0,column=0)
#パラメータ群
speed_label.grid(row=1,column=0)
speed.grid(row=1,column=1)
tone_label.grid(row=2,column=0)
tone.grid(row=2,column=1)
high_low_label.grid(row=3,column=0)
high_low.grid(row=3,column=1)
Volumne_label.grid(row=4,column=0)
Volumne.grid(row=4,column=1)
start_none_label.grid(row=5,column=0)
start_none.grid(row=5,column=1)
end_none_label.grid(row=6,column=0)
end_none.grid(row=6,column=1)

#アクセント設定部分
frame_accents=ttk.Frame(root)
#=入力セット=#
ac_label=ttk.Label(frame_accents,text="読み：")
ac_kana_entry=ttk.Entry(frame_accents,width=50)
ac_kana_entry.bind("<ButtonPress>",Select_text)
ac_core_label=ttk.Label(frame_accents,text="アクセント核の位置：")
span_move_up=ttk.Button(frame_accents,text="上へ移動",state="disable",command=apply_span_up)
span_move_down=ttk.Button(frame_accents,text="下へ移動",state="disable",command=apply_span_down)
play_word_button=ttk.Button(frame_accents,text="この単語だけ再生する",state="disable",command=play_word)

#Spinboxの値格納用変数
var = tk.IntVar(root)
var.set(0)  #初期値セット
ac_spinbix=tk.Spinbox(frame_accents,textvariable=var,from_=0,to=100,increment=1,state="disable",command=acc_show)
button_apply=ttk.Button(frame_accents,text="適用",command=apply_acc,state="disable")

#アクセント結合型用
acCon_label=ttk.Label(frame_accents,text="アクセント結合型：")
acCon_combobox=ttk.Combobox(frame_accents,values=aConType,state="disable")
#acCon_combobox.bind("<<ComboboxSelected>>",select_voice)
#アクセント修飾形用
acMod_label=ttk.Label(frame_accents,text="アクセント修飾型：")
acMod_combobox=ttk.Combobox(frame_accents,values=aModType,state="disable")
#acMod_combobox.bind("<<ComboboxSelected>>",select_voice)

#アクセント表示用Canvas
ac_Canvas=tk.Canvas(frame_accents,
    width=400,
    height=100,
)
#各種ウィジェットの設定
"""
 0 1_2
0
1
...
"""
ac_label.grid(row=0,column=0)
ac_kana_entry.grid(row=0,column=1)
ac_core_label.grid(row=1,column=0)
span_move_up.grid(row=2,column=0)
span_move_down.grid(row=2,column=1)
ac_spinbix.grid(row=1,column=1)
button_apply.grid(row=2,column=2)
acCon_label.grid(row=3,column=0)
acCon_combobox.grid(row=3,column=1)
acMod_label.grid(row=4,column=0)
acMod_combobox.grid(row=4,column=1)
play_word_button.grid(row=4,column=2)
ac_Canvas.grid(row=5,column=1)

#=================================
#フレーム配置
"""
 0 1_2_3
0
1
2
...
"""
frame.grid(column=0,row=0,sticky=tk.NSEW,padx=5,pady=10)
frame_setup.grid(column=0,row=2,sticky=tk.NSEW,padx=5,pady=10)
frame_accents.grid(column=1,row=2,sticky=tk.NSEW,padx=5,pady=10)
Canvas_tree.grid(column=1,row=0,sticky=tk.NSEW,padx=5,pady=10)
# キャンバスの右に垂直方向のスクロールバーを配置
ybar.grid(
    column=2, row=0,  # キャンバスの右の位置を指定
    sticky=tk.N + tk.S  # 上下いっぱいに引き伸ばす
)
xbar.grid(
    column=1,  row=1, # キャンバスの下の位置を指定
    sticky=tk.W + tk.E  # 左右いっぱいに引き伸ばす
)

#記入例
entry.insert(tk.END,"季も桃も桃のうち")

root.mainloop()