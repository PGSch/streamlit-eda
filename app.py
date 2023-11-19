from datetime import datetime

import streamlit as st
import numpy as np
import pandas as pd
import ta
from PIL import Image

# Settings
width_px = 1000
ta_col_prefix = 'ta_'

# 1. Streamlit Theme Configuration
st.set_page_config(layout="wide", page_title="Financial Data Analysis", page_icon="📊")

# 2. Improved Layout and Spacing
col1, col2, col3 = st.columns(3)
# Sidebar settings header
with col1:
    st.sidebar.header("S&S Consulting 2024")

# Sidebar
# Load the logo image (replace 'path/to/logo.png' with the actual path or URL to your logo)
logo = Image.open('./.streamlit/docs/logo.png')

# Display the logo in the sidebar
st.sidebar.image(logo, use_column_width=True)

# Sidebar settings header
with col2:
    st.sidebar.header("Settings")

# Dropdown values col2
rv_periods = st.sidebar.selectbox(
    'How many periods to calculate the return price?',
     [1, 2, 3, 5, 7, 14, 31])

# Dropdown values col3
rv_noise = st.sidebar.selectbox(
    'Simulate noise (0 is no noise)',
     [0, 1, 2, 3, 4, 5])






# Data preparation
@st.cache_data
def load_data():

    # Load financial dataset
    df = pd.read_csv('https://raw.githubusercontent.com/bukosabino/streamlit-demo-financial-eda/master/data/data.csv', sep=',')

    # Clean NaN values
    df = ta.utils.dropna(df)

    # Apply feature engineering (technical analysis)
    # df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume_BTC", fillna=True)
    df = ta.add_volatility_ta(df, "High", "Low", "Close", fillna=False, colprefix=ta_col_prefix)
    df = ta.add_momentum_ta(df, "High", "Low", "Close", "Volume_Currency", fillna=False, colprefix=ta_col_prefix)

    return df

df = load_data()

# Prepare target: X Periods Return
df['y'] = (df['Close'] / df['Close'].shift(rv_periods) - 1) * 100

if rv_noise>0:
    # Define the standard deviation of the noise
    # This determines how much noise you want to add
    noise_level = rv_noise/100

    # Add noise to the 'High' and 'Low' columns
    df['High'] += np.random.normal(0, df['High'] * noise_level, df['High'].shape)
    df['Low'] += np.random.normal(0, df['Low'] * noise_level, df['Low'].shape)
    df['Close_Noise'] = df['Close']+np.random.normal(0, df['Low'] * noise_level, df['Low'].shape)


# Clean NaN values
df = df.dropna()

# Body
st.title('EDA for financial datasets (OHLCV)')

a = datetime.utcfromtimestamp(df['Timestamp'].head(1)).strftime('%Y-%m-%d %H:%M:%S')
b = datetime.utcfromtimestamp(df['Timestamp'].tail(1)).strftime('%Y-%m-%d %H:%M:%S')
st.write(f'We try to explore a small financial time series dataset (2000 rows) with BTC/USD prices from {a} to {b}')
st.write('We start with an OHLCV financial dataset, and we get some technical analysis features from the original '
         'dataset using [ta package](https://github.com/bukosabino/ta). Then, we define the target value as the X '
         'period return value (the user can set it). Finally, we explore these features and the target column '
         'graphically.')

st.subheader('Dataframe')
st.write(df.head())

st.subheader('Describe dataframe')
st.write(df.describe())

st.write('Number of rows: {}, Number of columns: {}'.format(*df.shape))

st.subheader('Close Price')
if rv_noise>0:
    # Combine both 'Close' and 'Close_Noise' into a single DataFrame for plotting
    plot_data = df[['Close_Noise', 'Close']]
    st.line_chart(plot_data, width=width_px, color=["#FF0000","#0000FF"])
else:
    st.line_chart(df['Close'], width=width_px, color="#0000FF")
    
st.subheader('Open + Close Price')
plot_data = df[['Open', 'Close']]
st.line_chart(plot_data, width=width_px, color=["#8532a8","#0000FF"])

st.subheader(f'Return {rv_periods} periods')
st.area_chart(df['y'], width=width_px)

st.subheader('Target Histogram')
bins = list(np.arange(-10, 10, 0.5))
hist_values, hist_indexes = np.histogram(df['y'], bins=bins)
st.bar_chart(pd.DataFrame(data=hist_values, index=hist_indexes[0:-1]), width=width_px)
st.write('Target value min: {0:.2f}%; max: {1:.2f}%; mean: {2:.2f}%; std: {3:.2f}'.format(
    np.min(df['y']), np.max(df['y']), np.mean(df['y']), np.std(df['y'])))

# Univariate Analysis
st.subheader('Correlation coefficient ta features and target column')

x_cols = [col for col in df.columns if col not in ['Timestamp', 'y'] and col.startswith(ta_col_prefix)]
labels = [col for col in x_cols]
values = [np.corrcoef(df[col], df['y'])[0, 1] for col in x_cols]

st.bar_chart(data=pd.DataFrame(data=values, index=labels), width=width_px)
