import copy
yoon=["キャ","キュ","キョ",\
"ギャ","ギュ","ギョ",\
"シャ","シュ","シェ","ショ",\
"ジャ","ジュ","ジェ","ジョ",\
"スィ","ズィ",\
"チャ","チュ","チェ","チョ",\
"ツァ","ツィ","ツェ","ツォ",\
"ティ","テュ",\
"ディ","デュ",\
"トゥ","ドゥ",\
"ニャ","ニュ","ニェ","ニョ",\
"ヒャ","ヒュ","ヒェ","ヒョ",\
"ファ","フィ","フュ","フェ","フォ",\
"ビャ","ビュ","ビェ","ビョ",\
"ピャ","ピュ","ピェ","ピョ",\
"ミャ","ミュ","ミェ","ミョ",\
"イェ","リャ","リュ","リョ",\
"ウィ","ウェ","ウォ"]
min_aiueo={"ァ":"ア","ィ":"イ","ゥ":"ウ","ェ":"エ","ォ":"オ","ャ":"ヤ","ュ":"ユ","ョ":"ヨ"}
bo_aiueo={"ァ":"ア","ィ":"イ","ゥ":"ウ","ェ":"エ","ォ":"オ",\
"ア":"ア","イ":"イ","ウ":"ウ","エ":"エ","オ":"オ",\
"カ":"ア","サ":"ア","タ":"ア","ナ":"ア","ハ":"ア","マ":"ア","ヤ":"ア","ラ":"ア","ワ":"ア","ガ":"ア","ザ":"ア","ダ":"ア","バ":"ア","パ":"ア",\
"キ":"イ","シ":"イ","チ":"イ","ニ":"イ","ヒ":"イ","ミ":"イ","リ":"イ","ギ":"イ","ジ":"イ","ヂ":"イ","ビ":"イ","ピ":"イ",\
"ク":"ウ","ス":"ウ","ツ":"ウ","ヌ":"ウ","フ":"ウ","ム":"ウ","ユ":"ウ","ル":"ウ","ン":"ウ","グ":"ウ","ズ":"ウ","ヅ":"ウ","ブ":"ウ","プ":"ウ",\
"ケ":"エ","セ":"エ","テ":"エ","ネ":"エ","ヘ":"エ","メ":"エ","レ":"エ","ゲ":"エ","ゼ":"エ","デ":"エ","ベ":"エ","ペ":"エ",\
"コ":"オ","ソ":"オ","ト":"オ","ノ":"オ","ホ":"オ","モ":"オ","ヨ":"オ","ロ":"オ","ヲ":"オ","ゴ":"オ","ゾ":"オ","ド":"オ","ボ":"オ","ポ":"オ"
}
def bo2on(kana):
    """
    summary:repalce(ー,[所定の仮名])
    param:str(カタカナ)
    return:str(カタカナ)
    """
    newkana=""
    for n in range(len(kana)):
        if n!=0:
            if kana[n]=="ー":
                newkana=newkana+bo_aiueo[kana[n-1]]
            else:
                newkana=newkana+kana[n]
        else:
            if kana[n]=="ー":
                newkana="ウ"
            else:
                newkana=kana[0]
    return newkana

def kana2readly_kana(kanamozi):
    """
    summary:return 音素
    param:str(カタカナ)
    return:list(音素)
    """
    read_kana=""
    yoon_flug=0
    #拗音処理
    kana=bo2on(kanamozi)
    for n in range(len(kana)-1):
        if kana[(n+1)*(-1)] in min_aiueo:
            if kana[(n+1+1)*(-1)]+kana[(n+1)*(-1)] in yoon:
                read_kana=kana[(n+1+1)*(-1)]+kana[(n+1)*(-1)]+"/"+read_kana
                yoon_flug= 1
            else:
                read_kana=min_aiueo[kana[(n+1)*(-1)]]+"/"+read_kana
        else:
        #その他の音処理
            if yoon_flug==1:
                yoon_flug=0
            else:
                read_kana=kana[(n+1)*(-1)]+"/"+read_kana
    if yoon_flug==1:
        yoon_flug=0
    else:
        if kana[0] in min_aiueo:
            read_kana=min_aiueo[kana[0]]+"/"+read_kana
        else:
            read_kana=kana[0]+"/"+read_kana

    list_read_kana=read_kana.split("/")
    
    if list_read_kana.count("")!=0:
        for n in range(list_read_kana.count("")):
            list_read_kana.remove("")
    return list_read_kana
    
def kana_count(katakana):
    """
    summary:count 音素
    param:str(カタカナ)
    return:int(音素数)
    """
    moto=kana2readly_kana(katakana)
    return len(moto)

def word_compound(kanamozi,acc_num):
    """
    summary:カタカナ、アクセント核->aquestalk-like記法
    param:str(カタカナ)、int(アクセント核)
    return:str(aquestlike記法)
    """
    #文末、疑問文がきた時の処理を挟む
    kana=bo2on(kanamozi)
    if int(acc_num)==0:
        return kana+"'"
    else:
        minikana=""
        readly_kana=kana2readly_kana(kana)
        for n in range(len(readly_kana)):
            if n==int(acc_num)-1:
                minikana=minikana+readly_kana[n]+"'"
            else:
                minikana=minikana+readly_kana[n]
        return minikana
    
#======【編集中】===========
def sentence_compound(list_kana,list_acc,list_aModType,list_aConType,list_span):
    """
    summary:分かち書きした情報からaquestalk記法に持って行く
    param:list(仮名),list(アクセント核),list(aModType),list(aConType),list(係り受け番号)
    return:str(aquestlike記法)
    """
    #句読点、はてなは係り受け末尾にあるやつだけ残す。残したものは/がわりになる。
    replace_kigo=[["?","ハテナ",1,"C1"],\
                ["？","ハテナ",1,"C1"],\
                [",","テン",0,"C3"],\
                ["、","テン",0,"C3"],\
                ["。","マル",0,"C3"],\
                [",","マル",0,"C3"]]
    replace_kigo_end=[[",","、"],[".","。"],["?","？"]]
    for n in range(len(list_kana)-1):
        if list_span[n]==list_span[n+1]:
            for m in range(len(replace_kigo)):
                if list_kana[n]==replace_kigo[m][0]:
                    #置換
                     list_kana[n]=replace_kigo[m][1]
                     list_acc[n]=replace_kigo[m][2]
                     list_aConType[n]=replace_kigo[m][3]
        else:
            for m in range(len(replace_kigo_end)):
                if list_kana[n]==replace_kigo_end[m][0]:
                    list_kana[n]=replace_kigo_end[m][1]
                    list_aConType[n]="*"
    #末尾処理
    for m in range(len(replace_kigo_end)):
        if list_kana[-1]==replace_kigo_end[m][0]:
            list_kana[-1]=replace_kigo_end[m][1]
            list_aConType[-1]="*"
    
    span_apply=0
    for n in range(len(list_kana)):
        #まず独立句を探して前後のMod,Conを無効にする
        if list_aConType[n]=="独立":
            if n==0:
                list_aConType[n+1]="*"
            elif n==len(list_kana)-1:
                list_aModType[n-1]="*"
            else:
                list_aConType[n+1]="*"
                list_aModType[n-1]="*"
            #係り受け句を一個ずつずらす
            span_apply=span_apply+1
        if n!=len(list_kana)-1:
            list_span[n+1]=copy.deepcopy(list_span[n+1])+span_apply
    #係り受け区間ごとに格納する==【編集中・検討中】==
    new_list_kana=[]
    new_list_acc=[]
    new_list_aModType=[]
    new_list_aConType=[]
    mini_list_kana=[list_kana[0]]
    mini_list_acc=[list_acc[0]]
    mini_list_aModType=[list_aModType[0]]
    mini_list_aConType=[list_aConType[0]]
    for n in range(len(list_kana)-1):
        if list_span[n+1]==list_span[n]:
            mini_list_kana.append(list_kana[n+1])
            mini_list_acc.append(list_acc[n+1])
            mini_list_aModType.append(list_aModType[n+1])
            mini_list_aConType.append(list_aConType[n+1])
        else:
            new_list_kana.append(mini_list_kana)
            new_list_acc.append(mini_list_acc)
            new_list_aModType.append(mini_list_aModType)
            new_list_aConType.append(mini_list_aConType)
            #
            mini_list_kana=[list_kana[n+1]]
            mini_list_acc=[list_acc[n+1]]
            mini_list_aModType=[list_aModType[n+1]]
            mini_list_aConType=[list_aConType[n+1]]
    new_list_kana.append(mini_list_kana)
    new_list_acc.append(mini_list_acc)
    new_list_aModType.append(mini_list_aModType)
    new_list_aConType.append(mini_list_aConType)
    ###実際に結合法則に則ってやってみる##【編集中:deepcopyする！！！】#
    for m in range(len(new_list_kana)):
        for n in range(len(new_list_kana[m])):
            #アクセント修飾型の設定(アクセント核を更新して、更新した際に巻き込んだ側を[-]にする。)
            if n!=len(new_list_kana[m])-1:
                if "M1" in new_list_aModType[m][n]:
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n]))-new_list_aModType[m][n].split("@")[1]
                elif "M2" in new_list_aModType[m][n]:
                    if new_list_acc[n]==0:
                        new_list_acc[n]=kana_count(bo2on(new_list_kana[m][n]))-new_list_aModType[m][n].split("@")[1]
                elif "M4" in new_list_aModType[m][n]:
                    if new_list_acc[n]!=0 and list_acc[n]!=1:
                        new_list_acc[n]=kana_count(bo2on(new_list_kana[m][n]))-new_list_aModType[m][n].split("@")[1]
                else:
                    pass
    
    for m in range(len(new_list_kana)):
        for n in range(len(new_list_kana[m])):
            #aConTypeP(アクセント核を更新して、更新した際に巻き込んだ側を[-]にする。前に押して行く、)
            if n!=len(new_list_kana[m])-1:
                if new_list_aConType[m][n]=="P1":
                    if new_list_acc[m][n]!=0 and new_list_acc[m][n]!=kana_count(bo2on(new_list_kana[m][n])):
                        new_list_acc[m][n+1]=kana_count(bo2on(new_list_kana[m][n]))+copy.deepcopy(new_list_acc[m][n+1])
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                    else:
                        new_list_acc[m][n+1]=0
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                elif new_list_aConType[m][n]=="P2":
                    if new_list_acc[m][n]!=0 and new_list_acc[m][n]!=kana_count(bo2on(new_list_kana[m][n])):
                        new_list_acc[m][n+1]=kana_count(bo2on(new_list_kana[m][n]))+copy.deepcopy(new_list_acc[m][n+1])
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                    else:
                        new_list_acc[m][n+1]=kana_count(bo2on(new_list_kana[m][n]))+1
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                elif new_list_aConType[m][n]=="P4":
                    if new_list_acc[m][n]!=0 and new_list_acc[m][n]!=kana_count(bo2on(new_list_kana[m][n])):
                        new_list_acc[m][n+1]=copy.deepcopy(new_list_acc[m][n])
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                    else:
                        new_list_acc[m][n+1]=kana_count(bo2on(new_list_kana[m][n]))+1
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                elif new_list_aConType[m][n]=="P6":
                    new_list_acc[m][n+1]=0
                    new_list_acc[m][n]="-"
                    new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                    new_list_kana[m][n]="-"
                elif new_list_aConType[m][n]=="P13":
                    new_list_acc[m][n+1]=copy.deepcopy(new_list_acc[m][n])
                    new_list_acc[m][n]="-"
                    new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                    new_list_kana[m][n]="-"
                elif new_list_aConType[m][n]=="P14":
                    if new_list_acc[m][n]!=0 and list_acc[n]!=kana_count(bo2on(new_list_kana[m][n])):
                        new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n]))+copy.deepcopy(new_list_acc[m][n+1])
                        new_list_acc[m][n+1]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                    else:
                        new_list_acc[m][n+1]=copy.deepcopy(new_list_acc[m][n])
                        new_list_acc[m][n]="-"
                        new_list_kana[m][n+1]=copy.deepcopy(new_list_kana[m][n])+copy.deepcopy(new_list_kana[m][n+1])
                        new_list_kana[m][n]="-"
                else:
                    pass
                    
    for m in range(len(new_list_kana)):
        for n in range(len(new_list_kana[m])):
            #aConTypeF(アクセント核を更新して、更新した際に巻き込んだ側を[-]にする。前に押して行く、)
            if n!=0:
                if new_list_aConType[m][n]=="F1":
                    new_list_acc[m][n]=copy.deepcopy(new_list_acc[m][n-1])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_kana[m][n-1]="-"
                elif "F2" in new_list_aConType[m][n]:
                    if new_list_acc[m][n]==0:
                        new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+int(new_list_aConType[m][n].split("@")[1])
                        new_list_acc[m][n-1]="-"
                        new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                        new_list_kana[m][n-1]="-"
                    else:
                        new_list_acc[m][n]=copy.deepcopy(new_list_acc[m][n-1])
                        new_list_acc[m][n-1]="-"
                        new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                        new_list_kana[m][n-1]="-"
                elif "F3" in new_list_aConType[m][n]:
                    if new_list_acc[m][n-1]!=0:
                        new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+int(new_list_aConType[m][n].split("@")[1])
                        new_list_acc[m][n-1]="-"
                        new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                        new_list_kana[m][n-1]="-"
                    else:
                        new_list_acc[m][n]=copy.deepcopy(new_list_acc[m][n-1])
                        new_list_acc[m][n-1]="-"
                        new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                        new_list_kana[m][n-1]="-"
                elif "F4" in new_list_aConType[m][n]:
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+int(new_list_aConType[m][n].split("@")[1])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_kana[m][n-1]="-"
                elif "F5" in new_list_aConType[m][n]:
                    new_list_acc[m][n]=0
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_kana[m][n-1]="-"
                elif "F6" in new_list_aConType[m][n]:#ホントは複数パラメーター出ていて、平板型かいなかでアクセントの結合が異なるものの、そこまで辞書が対応していないので出来次第修正する、
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+int(new_list_aConType[m][n].split("@")[1])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_kana[m][n-1]="-"
                else:
                    pass
                    
    for m in range(len(new_list_kana)):
        for n in range(len(new_list_kana[m])):
            #aConTypeC(アクセント核を更新して、更新した際に巻き込んだ側を[-]にする。前に押して行く、)
            if n!=0:
                if new_list_aConType[m][n]=="C1":
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+new_list_acc[m][n]
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
                elif new_list_aConType[m][n]=="C2":
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))+1
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
                elif new_list_aConType[m][n]=="C3":
                    new_list_acc[m][n]=kana_count(bo2on(new_list_kana[m][n-1]))
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
                elif new_list_aConType[m][n]=="C4":
                    new_list_acc[m][n]=0
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
                elif new_list_aConType[m][n]=="C5":
                    new_list_acc[m][n]=copy.deepcopy(new_list_acc[m][n-1])
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
                else:#何にも値が入っていない時も想定する(?とかで終わる時)
                    new_list_acc[m][n]=copy.deepcopy(new_list_acc[m][n-1])
                    new_list_kana[m][n]=copy.deepcopy(new_list_kana[m][n-1])+copy.deepcopy(new_list_kana[m][n])
                    new_list_acc[m][n-1]="-"
                    new_list_kana[m][n-1]="-"
    #===合成してAquestalk出力編集中=#
    output=""
    #デバッグ用
    #print(new_list_kana)
    #print(list_span)
    for m in range(len(new_list_kana)):
        for n in range(len(new_list_kana[m])):
            #独立句以外くっつける(アクセント核を更新して、更新した際に巻き込んだ側を[-]にする)「?、。」残したものは/がわりになる。
            if new_list_kana[m][n]!="-":
                if new_list_kana[m][n] not in ["、","。","？"]:
                    mini_output=word_compound(new_list_kana[m][n],new_list_acc[m][n])
                    if "'" not in mini_output:
                        mini_output=mini_output+"'"
                    output=output+mini_output.replace("、","").replace("。","").replace("？","")+"/"
                else:
                    output=output[0:-1]+new_list_kana[m][n]
    if output[-1] in ["/","、","。"]:
        output=output[0:-1]
    return output
#test
#x="ボウズガビョウブニジョウズニボウズノエヲカイタ"
#print(x,kana2readly_kana(x),kana_count(x))
#print("スモモ",0)
#print(bo2on("スモーモ"))