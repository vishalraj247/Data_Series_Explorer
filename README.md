# Data Series Explorer Web App

## Authors
Group 11: 
- Vishal Raj (14227627)
- Rohit Sharma (24590960)
- Ronik Jayakumar (24680264)
- William Dai (13628019)

## Description
This application serves as a data exploration tool, offering users the ability to upload and analyze CSV datasets through an intuitive web interface. It provides detailed insights into DataFrame statistics, numerical and text series analysis, as well as date-time information extraction.

Challenges faced during development included managing version control with multiple collaborators, ensuring data validation for robust error handling, and implementing interactive visualizations that are both informative and user-friendly.

Future features we hope to implement include predictive analytics capabilities, integration with more data sources, and enhanced customization for data visualizations.

## How to Setup
To set up the development environment, follow these steps:

1. Ensure Python 3.9 is installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the project directory and install required packages using `pip install -r requirements.txt`.

The project uses the following main packages:
- Streamlit for the web application framework.
- Pandas for data manipulation.
- Altair for interactive charting.

## How to Run the Program
To run the web application, use the following steps:

1. Open your command prompt or terminal.
2. Navigate to the directory containing `streamlit_app.py`.
3. Run the command `streamlit run streamlit_app.py`.
4. The web application should now be accessible in your web browser at the local address provided by Streamlit.

## Project Structure
The project is organized as follows:

- `app/` - Contains the Streamlit application file `streamlit_app.py` which is the entry point of the web app.
- `tab_df/` - Houses the `display.py` and `logics.py` for the DataFrame tab functionality.
- `tab_num/` - Contains scripts for displaying and processing numeric series data.
- `tab_text/` - Includes modules for text data analysis and visualization.
- `tab_date/` - Comprises files for datetime series analysis.
- `requirements.txt` - A list of all the packages required to run the application.

## Citations
This project uses open-source code from the following authors and repositories:

- Streamlit Team for the core Streamlit framework (https://streamlit.io)
- Pandas Development Team for pandas library (https://pandas.pydata.org)
- Altair Visualization authors for the Altair charting library (https://altair-viz.github.io)

We have also taken inspiration and code snippets from Stack Overflow where applicable, adhering to license agreements.