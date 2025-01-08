import streamlit as st
from textblob import TextBlob
import pandas as pd
import cleantext

def main():
    st.title("Customer review analysis")

    st.header("Sentiment Analysis")

    with st.expander("Analyze Text"):
        text = st.text_input("Text here:")
        if text:
            blob = TextBlob(text)
            st.write("Polarity", round(blob.sentiment.polarity, 2))
            st.write("Subjectivity", round(blob.sentiment.subjectivity, 2))

        pre = st.text_input("Clean Text:")
        if pre:
            st.write(
                cleantext.clean(pre, clean_all=False, extra_spaces=True, stopwords=True, lowercase=True, numbers=True,
                                punct=True))


    def score(x):
        blob = TextBlob(x)
        return blob.sentiment.polarity


    def analyze(x):
        if x >= 0.5:
            return "Positive"
        elif x <= -0.5:
            return "Negative"
        else:
            return "Neutral"

    with st.expander("Analyze CSV"):
        upl = st.file_uploader("Upload file")

        if upl:
            try:
                st.write("File uploaded successfully!")
                # Check file format and read content
                if upl.name.endswith('.csv'):
                    df = pd.read_csv(upl)
                elif upl.name.endswith('.xlsx') or upl.name.endswith('.xls'):
                    df = pd.read_excel(upl, engine='openpyxl')
                else:
                    st.error("Unsupported file format. Please upload a CSV or Excel file.")
                    return

                st.write("File read successfully!")
                st.write(df.head())  # Display the first few rows of the DataFrame

                if "tweets" in df.columns:
                    df["score"] = df["tweets"].apply(score)
                    df["analysis"] = df["score"].apply(analyze)

                    # Calculate overall sentiment
                    avg_score = df["score"].mean()

                    if avg_score > 0.5:
                        overall_sentiment = "Overall Sentiment: Positive"
                    elif avg_score < -0.5:
                        overall_sentiment = "Overall Sentiment: Negative"
                    else:
                        overall_sentiment = "Overall Sentiment: Neutral"

                    st.write(df.head())  # Display the processed DataFrame
                    st.subheader(overall_sentiment)  # Display overall prediction

                    @st.cache_data
                    def convert_df(df):
                        return df.to_csv().encode("utf-8")

                    csv = convert_df(df)
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name="sentiment.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("Column 'tweets' not found in the uploaded file. Please check the column names.")
            except Exception as e:
                st.error(f"Error reading or processing the file: {e}")


if __name__ == "__main__":
    main()
