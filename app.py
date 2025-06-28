import streamlit as st
import preprocessor #importing fncn for calling
import helperr
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chats Analyzer")
import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()
        except:
            st.error("Invalid JSON")
    return None

lottie_url = "https://assets9.lottiefiles.com/packages/lf20_j1adxtyb.json"  # Loading animation
loading_animation = load_lottie_url(lottie_url)

from streamlit_lottie import st_lottie
import requests


def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.title("🚀 Welcome to Watcha - WhatsApp Chat Analyzer")

lottie_url = "https://assets9.lottiefiles.com/packages/lf20_w51pcehl.json"  # Replace with your desired animation
lottie_json = load_lottie_url(lottie_url)

st_lottie(lottie_json, height=300, key="watcha_intro")

st.set_page_config(layout="wide")
import streamlit as st

uploaded_file = st.sidebar.file_uploader("Choose a file") #this option should be in sidebar
if uploaded_file is not None:
    placeholder = st.empty()

    # Show temporary message
    placeholder.info("✅ Select to analyse..")

    # Wait for 5 seconds


    # Clear the message
    placeholder.empty()

    # st.write("✅ Select to analyse..")


    bytes_data = uploaded_file.getvalue() #upload txt option
    data = bytes_data.decode("utf-8") #convert stream into string uding decode
    # st.text(data) #return to streamlit
    df= preprocessor.preprocess(data) #calling fncn to give preprocessed data
    # st.dataframe(df)  #this is fncn in streamlit to display datframe format

   #nhow analysis time
   #for individual level anlaysis or overall
   #fetch unique users, extracting participants of chat, group
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification') #agar ho to remove,wrna error, ijndividual wale me to nhii hoga group notificn

    user_list.sort()
    user_list.insert(0,"Group-Level/Mutual") #add for overall analysis , this will be at top of dropdown
#proper indentation must be there
    selected_user = st.sidebar.selectbox("Show analysis wrt ", user_list)#put the selected in a var
    #if there is group notification, remove it arrange user in ascending order of words

    #ADD BUTTON for showing analysis, number of emojis,nmessage,length of words typed, timing
    if st.sidebar.button("Analyze :"):

        num_messages,num_words, num_media_messages,num_links= helperr.fetch_stats(selected_user,df) #call helperr fro dift fncns
        # words = helperr.fetch_stats(selected_user,df)
        #creating beta columns
        # To read file as bytes:
        placeholder = st.empty()

        # Show temporary message
        placeholder.info("🔍 Analyzing chat...")

        # Wait for 5 seconds
        time.sleep(5)

        # Clear the message
        placeholder.empty()

        with st.spinner("Please wait while we analyze the chat..."):
            st_lottie(loading_animation, height=200)
            time.sleep(3)  # Simulate analysis delay

        st.success("Chat Analysis completed!")

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)


#pattern smjho
        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(num_words)

        with col3:
            st.header("Total media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Total links")
            st.title(num_links)

        #TIMELINE
        st.title("Monthly Timeline")

        timeline= helperr.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helperr.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map se most busy month,day
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helperr.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helperr.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helperr.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == "Group-Level/Mutual":
            st.title("Busiest users")
            x,new_df=helperr.most_busy(df)
            fig, ax =plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                #prints the dataframe of percentage contri

    #WORDCLOUD
        df_wc= helperr.create_wordcloud(selected_user,df)
        fig, ax =plt.subplots()
        plt.imshow(df_wc)
        st.title("WordCloud")
        st.pyplot(fig) #wodcloud is according to most used word and size in image

    #most common words
        most_common_df=helperr.most_common_words(selected_user,df)
        st.title("Most common words")
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

    #emoji analysis
        emoji_df=helperr.emoji_analysis(selected_user,df)
        st.title("Emoji analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")#only top 5 to avoid cluttering
            st.pyplot(fig)

        # st.title("Emoji analysis")
        # fig, ax = plt.subplots()
        # ax.barh(emoji_df[0], emoji_df[1]) #0&1 are columns
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
