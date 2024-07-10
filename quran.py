import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import os.path
from pygame import mixer

st.set_page_config(layout='wide')
with open('Style.css') as Style:
    st.markdown(f'<style>{Style.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv('hafs_smart_v8.csv', low_memory=False, index_col='id', usecols=['id','aya_text_emlaey','sura_name_ar','sura_no','aya_no','jozz','sura_no'])
df['aya_text'] = pd.read_csv('./quran_emlay')['text'].values
df = df[['sura_name_ar','aya_text','aya_text_emlaey','aya_no','jozz','sura_no']]
# print(df[df.index == 6235]['aya_text'].values[0])
def t():
    if 'counter' in st.session_state:
     st.session_state.clear()
sb = st.sidebar
mode = sb.selectbox('حدد ما تريد : ',['قراءة القرءان الكريم', 'الإختبار في القرءان الكريم'])
mode = 'reading' if mode == 'قراءة القرءان الكريم' else 'testing'
if mode == 'reading':
    suraname = sb.selectbox('Enter Sura Name - أدخل اسم السورة:',df['sura_name_ar'].unique(), on_change=t)

    ExamOrNot = sb.selectbox('الإختبار في السورة ؟ ',['لا','نعم'], on_change=t)
    ExamOrNot = True if ExamOrNot =='نعم' else False
    if ExamOrNot:
        Easy = sb.selectbox('حدد نوع الإختبار : ',['سهل','صعب'], on_change=t)
        Easy = True if Easy == 'سهل' else False

    sb.markdown("Made with [Eng/Mohamed Saad](https://www.facebook.com/profile.php?id=61557483869983):heart_eyes:")

    st.markdown(f"<p style='margin : -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>اسم السورة : {suraname}</p>", unsafe_allow_html=True)
    suraNumber = df[df['sura_name_ar'] == suraname]['sura_no'].values[0]
    st.markdown(f"<p style='font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>رقم السورة : {suraNumber}</p>", unsafe_allow_html=True)


    sura_ayat = df[df['sura_name_ar'] == f'{suraname}']['aya_text'].values
    ayat_numbers = len(sura_ayat)
    st.markdown(f"<p style='margin : -38px 0px -20px 0; font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>عدد الآيات: {ayat_numbers}</p>", unsafe_allow_html=True)
    aya_no = 0

    if ExamOrNot:
        rand_aya = np.random.choice(sura_ayat)
        if 'rand_aya' not in st.session_state or 'counter' not in st.session_state or 'ques_num' not in st.session_state:
            st.session_state['rand_aya'] = rand_aya
            st.session_state['counter'] = 0
            st.session_state['ques_num'] = 1

        st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>السؤال رقم : {st.session_state['ques_num']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>أكمل من قوله تعالى : </p>", unsafe_allow_html=True)
        
            
        def next_aya():
            global rand_aya
            rand_aya = st.session_state['rand_aya']
            index = df[df['aya_text'] == rand_aya].index[0]
            rand_aya = df.iloc[index]['aya_text']
            st.session_state['rand_aya'] = rand_aya
            if not Easy:
                st.session_state['counter'] += 2
            
            
        def prev_aya():
            global rand_aya
            rand_aya = st.session_state['rand_aya']
            index = df[df['aya_text'] == rand_aya].index[0]
            rand_aya = df.iloc[index-2]['aya_text']
            st.session_state['rand_aya'] = rand_aya
            if not Easy:
                st.session_state['counter'] -= 5

        def next_ques():
            global rand_aya
            st.session_state['rand_aya'] = np.random.choice(sura_ayat)
            st.session_state['ques_num'] += 13
            st.session_state['counter'] = 0

        def skip_ques():
            global rand_aya
            st.session_state['rand_aya'] = np.random.choice(sura_ayat)
            st.session_state['counter'] = 0
            
        if Easy:
          s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
          st.markdown(s, unsafe_allow_html=True)
        else:
            if st.session_state['counter'] == 0:
                aya = st.session_state['rand_aya'].split(" ")
                aya = aya[:2] if len(aya) < 5 else aya[:5]
                aya = " ".join(aya) 
                aya += '...'
                s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya}</p>"
                st.markdown(s, unsafe_allow_html=True)
            else:
                s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
                st.markdown(s, unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns((20,20,20,10))
        c1.button('الآية التالية', on_click=next_aya)   
        c2.button('الآية السابقة', on_click=prev_aya)   
        c3.button('السؤال التالي', on_click=next_ques)   
        c4.button('تخطي السؤال', on_click=skip_ques)   
        

                


    else:
        if 'Running' not in st.session_state:
            st.session_state['Running'] = None
        def Reciting (sura_no, aya_no):
            sura_no = str(sura_no).zfill(3)
            aya_no = str(aya_no).zfill(3)

            if st.session_state['Running'] == None or st.session_state['Running'] != r'{}{}'.format(sura_no, aya_no) :
                 sound = f'''<audio controls autoplay>
                            <source src= "https://verses.quran.com/AbdulBaset/Mujawwad/mp3/{sura_no}{aya_no}.mp3"
                                    type="audio/mpeg">
                        </audio>
                        '''
                 st.html(sound)
                 st.session_state['Running'] = r'{}{}'.format(sura_no, aya_no)
            else:
                 sound = f'''<audio controls autoplay>
                            <source src= "https://verses.quran.com/AbdulBaset/MujawwadNotExist/mp3/{sura_no}{aya_no}.mp3"
                                    type="audio/mpeg">
                        </audio>
                        '''
                 st.html(sound)
                 st.session_state['Running'] = None 
             
        for aya in sura_ayat:
            sura_no = df[df['sura_name_ar'] == suraname]['sura_no'].values[0]
            aya_no += 1
            s = f"<p class = 'aya' >{aya} ({aya_no}) </p>"
            st.markdown(s, unsafe_allow_html=True)
            st.button('&#9658;', key=aya_no, on_click=Reciting, args=[sura_no, aya_no])    

else:
    def startTest():
        st.session_state['ques_num'] = 1
        st.session_state['choosed_index'] = 0
        st.session_state['numTrue'] = 0
        st.session_state['trueAya'] = []
        st.session_state['falseAya'] = []
        st.session_state['counter'] = 0
        st.session_state['Running'] = False
        st.session_state['dicBar'] =  {
                    'sura' : [],
                    'answer' : []
                }
    sbTest = st.sidebar
    tMode = sbTest.selectbox('حدد نوع الإختبار : ',['الاختبار في جزء معين','الاختبار في عدد أجزاء معين','سؤال من كل جزء'], on_change = startTest)
    tMode = 'one' if tMode == 'الاختبار في جزء معين' else 'Multi' if tMode == 'الاختبار في عدد أجزاء معين' else 'oneForAll'
    def Testing(Easy = True, oneForJuzz = False):
        global my_df
        if st.session_state['ques_num'] <= quesNumbers :
            if oneForJuzz:
             st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>سؤال الجزء : {st.session_state['ques_num']}</p>", unsafe_allow_html=True)
            else:
             st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>السؤال رقم : {st.session_state['ques_num']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>أكمل من قوله تعالى : </p>", unsafe_allow_html=True)
            if Easy:
                s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
                st.markdown(s, unsafe_allow_html=True)
            else :
                if st.session_state['counter'] == 0:
                    aya = st.session_state['rand_aya'].split(" ")
                    aya = aya[:2] if len(aya) < 5 else aya[:5]
                    aya = " ".join(aya) 
                    aya += '...'
                    s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya}</p>"
                    st.markdown(s, unsafe_allow_html=True)
                else:
                    s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
                    st.markdown(s, unsafe_allow_html=True)
            def next_aya():
                global rand_aya
                st.session_state['choosed_index'] += 1
                index = st.session_state['choosed_index']
                rand_aya = df.iloc[index-1]['aya_text']
                st.session_state['rand_aya'] = rand_aya
                if not Easy:
                    st.session_state['counter'] += 22

                
                
            def prev_aya():
                global rand_aya
                st.session_state['choosed_index'] -= 1
                index = st.session_state['choosed_index']
                rand_aya = df.iloc[index-1]['aya_text']
                st.session_state['rand_aya'] = rand_aya
                


            def next_ques(trueOrfalse):
                global rand_aya, my_df
                st.session_state['ques_num'] += 1 
                st.session_state['counter'] = 0
                if trueOrfalse :
                    st.session_state['numTrue'] += 1
                    st.session_state['trueAya'].append(st.session_state['rand_aya'])
                    st.session_state['dicBar']['sura'].append(df[df['aya_text'] == st.session_state['rand_aya']]['sura_name_ar'].values[0])
                    st.session_state['dicBar']['answer'].append('إجابة صحيحة')
                    
                else:
                    st.session_state['falseAya'].append(st.session_state['rand_aya'])
                    st.session_state['dicBar']['sura'].append(df[df['aya_text'] == st.session_state['rand_aya']]['sura_name_ar'].values[0])
                    st.session_state['dicBar']['answer'].append('إجابة خاطئة')
                if oneForJuzz and st.session_state['ques_num'] <= 30:
                    my_df = df[df['jozz'] == st.session_state['ques_num']]['aya_text']
                if oneForJuzz and st.session_state['ques_num'] == 31:
                    my_df = df[df['jozz'] == 1]['aya_text']
                st.session_state['choosed_index'] = np.random.choice(my_df.index)
                st.session_state['rand_aya'] = my_df.loc[st.session_state['choosed_index']]
                if st.session_state['ques_num'] > quesNumbers:
                    def show_results():
                        st.session_state['Running'] = False 
                        st.session_state['ques_num'] = 1
                        c1,c2,c3,c4 = st.columns((20,20,20,10))
                        c1.metric("عدد الاسئلة", quesNumbers)
                        c2.metric('الإجابات الصحيحة', st.session_state['numTrue'])
                        c3.metric('الإجابات الخاطئة', (quesNumbers - st.session_state['numTrue']))
                        c4.metric('النسبة', ((st.session_state['numTrue'] / quesNumbers) * 100).__round__(2))
                        st.divider()
                        #bar chart for the questions:
                        dfBar = pd.DataFrame(st.session_state['dicBar'])
                        dfBar = dfBar.groupby(['sura']).value_counts().to_frame().reset_index(level=['answer','sura'])
                        Bar = px.bar(data_frame=dfBar, x = 'sura',y = 'count',color='answer', labels={'sura':'اسم السورة','count':'العدد','answer':'الإجابة'},color_discrete_map={'إجابة خاطئة':'rgb(245, 55, 33)','إجابة صحيحة':'rgb(51, 245, 33)'})
                        st.plotly_chart(Bar, use_container_width=True)

                        s = f"<p style= 'margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:#86EE7C; direction: rtl;'>الإجابات الصحيحة : {st.session_state['numTrue']}</p>"
                        st.markdown(s, unsafe_allow_html=True)
                        for aya in st.session_state['trueAya']:
                            s = f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya} </p>"
                            st.markdown(s, unsafe_allow_html=True)
                            s = f"<p style='margin : 0px 0px -38px 0px; color:#8B22F4; font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>اسم السورة : {df[df['aya_text'] == aya]['sura_name_ar'].values[0]} </p>"
                            st.markdown(s, unsafe_allow_html=True)
                            st.divider()
                        st.divider()
                        s = f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>الإجابات الخاطئة : {quesNumbers - st.session_state['numTrue']}</p>"
                        st.markdown(s, unsafe_allow_html=True)
                        for aya in st.session_state['falseAya']:
                            s = f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya}</p>"
                            st.markdown(s, unsafe_allow_html=True)
                            s = f"<p style='margin : 0px 0px -38px 0px; color:#8B22F4; font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>اسم السورة : {df[df['aya_text'] == aya]['sura_name_ar'].values[0]} </p>"
                            st.markdown(s, unsafe_allow_html=True)
                            st.divider()

                    st.button('عرض النتائج', on_click = show_results, type='primary')

            def skip_ques():
                global rand_aya, my_df
                st.session_state['choosed_index'] = np.random.choice(my_df.index)
                rand_aya = my_df.loc[st.session_state['choosed_index']]
                st.session_state['rand_aya'] = rand_aya
            c1,c2,c3,c4 = st.columns((20,20,20,10))
            c1.button('الآية التالية', on_click=next_aya)   
            c2.button('الآية السابقة', on_click=prev_aya)   
            c3.button('إجابة صحيحة', on_click=next_ques, args =[True])   
            c3.button('! إجابة خاطئة', on_click=next_ques, args = [False])   
            c4.button('تخطي السؤال', on_click=skip_ques)
    if tMode == 'one':
        quesNumbers = sbTest.number_input('أدخل عدد الأسئلة : ', min_value = 1, max_value = 30, on_change = startTest)
        if 'ques_num' not in st.session_state:
            startTest()
        jozzNumber = sbTest.selectbox('أدخل رقم الجزء : ',[jozz for jozz in range(1,31)], on_change = startTest)
        my_df = df[df['jozz'] == jozzNumber]['aya_text']
        def startTestone():
            choosed_index = np.random.choice(my_df.index)
            rand_aya = my_df.loc[choosed_index]
            startTest()
            st.session_state['choosed_index'] = choosed_index
            st.session_state['rand_aya'] = rand_aya
            st.session_state['Running'] = True
        sbTest.button('بدء الاختبار', on_click = startTestone)
        if len(st.session_state) > 1 and st.session_state['Running'] :
            Testing()
        
    elif tMode == 'Multi' :
        quesNumbers = sbTest.number_input('أدخل عدد الأسئلة : ', min_value = 1, max_value = 30, on_change = startTest)
        fromJuzz = sbTest.number_input('من الجزء : ', min_value = 1, max_value = 30, on_change = startTest)
        toJuzz = sbTest.number_input('إلى الجزء : ', min_value = (fromJuzz+1), max_value = 30, on_change = startTest)
        Easy = sb.selectbox('حدد نوع الإختبار : ',['سهل','صعب'], on_change=startTest)
        Easy = True if Easy == 'سهل' else False
        my_df = df[(df['jozz'] >= fromJuzz) & (df['jozz'] <= toJuzz)]['aya_text']

        def startTesttwo():
            choosed_index = np.random.choice(my_df.index)
            rand_aya = my_df.loc[choosed_index]
            startTest()
            st.session_state['choosed_index'] = choosed_index
            st.session_state['rand_aya'] = rand_aya
            st.session_state['Running'] = True
        if 'rand_aya' not in st.session_state:
            startTesttwo()
        sb.button('بدء الاختبار', on_click = startTesttwo)
        if Easy and st.session_state['Running']:
            Testing()
        elif (not Easy) and st.session_state['Running']:
            Testing(Easy=False)
    else:
        if 'ques_num' not in st.session_state:
            startTest()
        quesNumbers = 30
        my_df = df[df['jozz'] == st.session_state['ques_num']]['aya_text']
        def startTestthree():
            choosed_index = np.random.choice(my_df.index)
            rand_aya = my_df.loc[choosed_index]
            startTest()
            st.session_state['choosed_index'] = choosed_index
            st.session_state['rand_aya'] = rand_aya
            st.session_state['Running'] = True
        sb.button('بدء الاختبار', on_click = startTestthree)
        if st.session_state['Running']:
            Testing(oneForJuzz=True)
        
