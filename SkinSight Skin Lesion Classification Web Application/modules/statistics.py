import streamlit as st
import pandas as pd
import altair as alt
from utils import history_utils

def run():
    st.title("📊 Real-time Statistics by Lesion Type")

    # Load classification history
    history = history_utils.load_history()

    if not history:
        st.write("No classification history available.")
        return

    # Count uploads by lesion type
    lesion_counts = {}
    for record in history:
        lesion_type = record["prediction"]
        lesion_counts[lesion_type] = lesion_counts.get(lesion_type, 0) + 1

    # Convert to a DataFrame for visualization
    df = pd.DataFrame(list(lesion_counts.items()), columns=["Lesion Type", "Number of Uploads"])

    # Sort the DataFrame by "Number of Uploads" in descending order
    df = df.sort_values(by="Number of Uploads", ascending=False)

    # Create a bar chart using Altair
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "Number of Uploads:Q",
            title="Number of Uploads",
            scale=alt.Scale(domain=(0, df["Number of Uploads"].max() + 1)),  # Ensure domain covers max value
            axis=alt.Axis(tickCount=df["Number of Uploads"].max(), tickMinStep=1)  # Force increments of 1
        ),
        y=alt.Y(
            "Lesion Type:N",
            sort="-x",
            title="Lesion Type",
            axis=alt.Axis(labelLimit=200)  # Allow longer labels
        ),
        tooltip=["Lesion Type", "Number of Uploads"]
    ).properties(
        title="Number of Uploads by Lesion Type",
        height=500,  # Increase height for better readability
        width=700    # Adjust width for better spacing
    )

    # Display the bar chart
    st.altair_chart(bar_chart, use_container_width=True)

    # Reset the index for the data table and start numbering from 1
    df.index += 1

    # Display the data table
    st.write("### Detailed Upload Data")
    st.dataframe(df)
