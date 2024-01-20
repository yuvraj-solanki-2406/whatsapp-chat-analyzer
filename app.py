import streamlit as st
import preprocessor as pp
import helper
# import matplotlib as mpl
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Select a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = pp.preprocessData(data=data)

    # st.dataframe(df)
    user_list = df["user"].unique().tolist()
    user_list.remove("Encryption notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyse with User", user_list)

    if st.sidebar.button("Show Analysis"):
        num_msgs, num_words, num_media, num_links = helper.showStats(selected_user, df)
        st.title("Top Stats of the Chat")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.subheader(num_msgs)

        with col2:
            st.subheader("Total Words")
            st.subheader(num_words)

        with col3:
            st.subheader("Total Media Items")
            st.subheader(num_media)

        with col4:
            st.subheader("Total Links")
            st.subheader(num_links)

        # Group monthly timeline
        monthly_timeline = helper.monthlyTimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'], monthly_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Week activity day
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy week day")
            week_activity_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(week_activity_day.index, week_activity_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            month_activity = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_activity.index, month_activity.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':
            st.subheader("Most Active User")
            col1, col2 = st.columns(2)

            data, new_df = helper.mostActiveUser(df)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(data.index, data.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.header("Word Cloud")
        df_wc = helper.createWordCloud(selected_user, df=df)
        fig, axes = plt.subplots()
        axes.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        common_words = helper.mostCommonWords(selected_user, df)
        fig, axes = plt.subplots()
        axes.barh(common_words[0], common_words[1])
        plt.xticks(rotation='vertical')

        st.header("Most Common Words")
        st.pyplot(fig)

        # Emojis Analysis
        st.header("Emojis Analysis")
        col1, col2 = st.columns(2)
        emojis_df = helper.emojiCount(selected_user, df)
        with col1:
            st.dataframe(emojis_df)
        with col2:
            # mpl.rc('font', family='serif', serif='cmr10')
            plt.rcParams['font.family'] = 'DejaVu Sans'
            fig, axes = plt.subplots()
            axes.pie(emojis_df[1].head(6), labels=emojis_df[0].head(6), autopct="%0.2f")
            st.pyplot(fig)
