import streamlit as st 
import newspaper

from textblob import TextBlob 
import nltk 
nltk.download('punkt_tab')

st.title('Article for ADHD') 
url = st.text_input('Enter Url: ',placeholder='URL and then enter') 


if 'saved_articles' not in st.session_state:
    st.session_state.saved_articles = []

try:
    if url:
        article = newspaper.Article(url) 
        article.download() 
        article.parse()



        if st.button('Save Article'):
            st.session_state.saved_articles.append(url) 
            st.success("Article saved!")


        if st.button('Clear'):
             st.session_state.saved_articles = []
             st.success("Cleared!")

      
        if st.session_state.saved_articles:
            st.subheader("Saved Articles:")
            for saved_url in st.session_state.saved_articles:
                st.text(saved_url)  
        
        authors = article.authors

        st.text('Author/s')
        st.text(''.join(authors))
        article.nlp() 


        st.download_button(
            label="Download Summary as Text",
            data=article.summary, 
            file_name="article.txt",  
            mime="text/plain" 
        )

        tab1, tab2,tab3 = st.tabs(['Full Text', 'Summary','Etc']) #created tabs
        with tab1:
                article.text

        with tab2:
                
                st.text('Keywords')
                st.text(', '.join(article.keywords))
                st.text(article.summary)

        with tab3:
                if article.publish_date:
                    st.text('Published Date')
                    st.text(article.publish_date)
                    analysis = TextBlob(article.text)
                    st.text(f'Sentiment Polarity: {analysis.sentiment.polarity}')
                    
                    sentiment_score = analysis.sentiment.polarity
                    if sentiment_score > 0:
                        st.text('Sentiment: Positive')
                    elif sentiment_score < 0:
                        st.text('Sentiment: Negative')
                    else:
                        st.text('Sentiment: Neutral')

except:
        st.text('Error looks like soemthing is wrong')
        