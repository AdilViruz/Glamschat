import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns
import matplotlib.font_manager as fm
from textblob import TextBlob


st.set_page_config(page_title='Chats Glam',layout='wide', initial_sidebar_state='expanded')


st.title('WhatsApp Chat Analyzer')

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://i.pinimg.com/564x/d2/a7/76/d2a77609f5d97b9081b117c8f699bd37.jpg")
    }
  
    </style>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader('Upload a WhatsApp Chat File:')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    for user in user_list:
        if user == 'whatsapp notification':
            user_list.remove('whatsapp notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.selectbox("Analysis based on user", user_list)



    # Stats
    if st.button("Show Analysis"):
        num_messages, words, num_media_msgs, links = helper.fetch_stats(selected_user, df)

        st.divider()

        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(len(words))

        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Links Shared")
            st.title(len(links))

            # Adding some styling and additional info
            st.markdown("""
                   <style>
                     [data-testid="column"]{
                     background-color: #dcf8c6;
                     border-radius:25px;
                     padding:10px
                    }
                   </style>
                      """, unsafe_allow_html=True)



        st.divider()

        st.title('Timelines')
        col1, col2,  = st.columns(2)


        with col1:

            st.header('Monthly Timeline')
            timeline = helper.monthly_timeline(selected_user, df)
            sns.set_style("whitegrid")
            fig, ax = plt.subplots()
            sns.lineplot(data=timeline, x='time', y='message', ax=ax, color='red', marker='o')
            ax.set_xlabel('Time', fontsize=12)
            ax.set_ylabel('Messages', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Display the plot in the Streamlit app
            st.pyplot(fig)

            # Adding some styling and additional info
            st.markdown("""
                <style>
                .reportview-container {
                    background: #f0f2f6;
                }
                .sidebar .sidebar-content {
                    background: #f9f9f9;
                }
                .css-1d391kg p {
                    font-size: 18px;
                }
                </style>
            """, unsafe_allow_html=True)
        with col2:
            # daily timeline
            st.header('Daily Timeline')
            daily_timeline = helper.daily_timeline(selected_user, df)

            # Display a line plot with improved styling
            sns.set_style("whitegrid")
            fig, ax = plt.subplots()
            sns.lineplot(data=daily_timeline, x='only_date', y='message', ax=ax, color='green', marker='o')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Messages', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Display the plot in the Streamlit app
            st.pyplot(fig)

            # Adding some styling and additional info
            st.markdown("""
                <style>
                .reportview-container {
                    background: #00ff00;
                }
                .sidebar .sidebar-content {
                    background: #f9f9f9;
                }
                .css-1d391kg p {
                    font-size: 18px;
                }
                </style>
            """, unsafe_allow_html=True)

        st.divider()

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
        # activity heatmap
            st.title('Weekly Activity Map')
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            # sns.heatmap(user_heatmap, cmap='coolwarm', ax=ax, annot=True, fmt='.1f')
            # sns.heatmap(user_heatmap, cmap='viridis', ax=ax, annot=True, fmt='.1f')
            # sns.heatmap(user_heatmap, cmap='plasma', ax=ax, annot=True, fmt='.1f')
            sns.heatmap(user_heatmap, cmap='inferno', ax=ax, annot=True, fmt='.1f')
            # sns.heatmap(user_heatmap, cmap='magma', ax=ax, annot=True, fmt='.1f')
            # sns.heatmap(user_heatmap, cmap='YlGnBu', ax=ax, annot=True, fmt='.1f')

            ax.set_title('Weekly Activity Heatmap', fontsize=16)
            ax.set_xlabel('Day of Week', fontsize=12)
            ax.set_ylabel('Hour of Day', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            # Finding the most active users in a group
            if selected_user == 'Overall':
                st.title("Most Active Users")
                x, new_df = helper.most_active_users(df)

                fig, ax = plt.subplots(figsize=(8, 6))
                ax.bar(x.index, x.values, color='red')
                ax.set_xlabel('Users', fontsize=12)
                ax.set_ylabel('Message Count', fontsize=12)
                ax.set_title('Most Active Users', fontsize=14)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)

            # Adding some styling and additional info
            st.markdown("""
                <style>
                .reportview-container {
                    background: #f0f2f6;
                }
                .sidebar .sidebar-content {
                    background: #f9f9f9;
                }
                .css-1d391kg p {
                    font-size: 18px;
                }
                </style>
            """, unsafe_allow_html=True)

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            # WordCloud
            st.title('Wordcloud')
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

        with col2:
            # most common words
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color='red')
            plt.xticks(rotation='vertical')
            st.title('Most Common Words')
            st.pyplot(fig)


        # most common emojis
        # emoji_df = helper.emoji_helper(selected_user, df)
        # st.title("Emoji Analysis")
        #
        # if emoji_df.empty is True:
        #     st.header("No Emojis Used")
        #
        # else:
        #     col1, col2 = st.columns(2)
        #
        #     with col1:
        #         st.dataframe(emoji_df)
        #
        #     with col2:
        #         fig, ax = plt.subplots()
        #         ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        #         st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        if emoji_df.empty:
            st.header("No Emojis Used")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Emoji Data")
                st.table(emoji_df.style.set_table_styles(
                    [{'selector': 'thead th',
                      'props': [('background-color', '#f0f2f6'), ('color', '#333'), ('font-size', '16px')]},
                     {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f9f9f9')]},
                     {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', 'white')]}]
                ))

            with col2:
                st.subheader("Emoji Usage Distribution")
                fig, ax = plt.subplots()
                colors = sns.color_palette('pastel')[0:len(emoji_df)]
                wedges, texts, autotexts = ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f",
                                                  colors=colors, startangle=140)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # Adding custom style to the chart
                for text in texts:
                    text.set_color('black')
                    text.set_fontsize(12)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(10)

                st.pyplot(fig)

        # Adding some styling and additional info
        st.markdown("""
            <style>
            .reportview-container {
                background: #f0f2f6;
            }
            .sidebar .sidebar-content {
                background: #f9f9f9;
            }
            .css-1d391kg p {
                font-size: 18px;
            }
            </style>
        """, unsafe_allow_html=True)




        def analyze_sentiment(df):
            sentiments = df['message'].apply(lambda msg: TextBlob(msg).sentiment.polarity)
            df['sentiment'] = sentiments.apply(lambda polarity: 'Positive' if polarity > 0
            else ('Negative' if polarity < 0 else 'Neutral'))
            sentiment_counts = df['sentiment'].value_counts()
            return sentiment_counts, df

        sentiment_counts, df = analyze_sentiment(df)


        st.divider()

        st.title("Sentiment Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots()
            ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'gray'])
            ax.set_ylabel('Number of Messages')
            ax.set_xlabel('Sentiment')
            ax.set_title('Sentiment Distribution')
            st.pyplot(fig)

        with col2:
            st.subheader("Sentiment Breakdown")
            st.subheader("")
            st.table(sentiment_counts.reset_index().rename(columns={'index': 'Sentiment', 'sentiment': 'Count'}))

