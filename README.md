# Automated EDA on financial dataset

Just a simple way to get automated Exploration Data Analysis from financial dataset (OHLCV) using [Streamlit](https://github.com/streamlit/streamlit) and [ta](https://github.com/bukosabino/ta).

To use this library you need a financial time series dataset including `Timestamp`, `Open`, `High`, `Low`, `Close` and `Volume` columns.


# Requirements

* python3.8 version

* streamlit==1.28.2
* ta==0.11.0
* protobuf==4.25.1
* lxml==4.9.3
* yfinance==0.2.32


# Run

```sh
conda create -n streamlit-eda python=3.8
pip install -r requirements.txt
streamlit run https://raw.githubusercontent.com/bukosabino/streamlit-demo-financial-eda/master/app.py
```


# TODO

* Heatmap: Visualize the correlation coefficient in between ta features.
* Web application user can load a .csv file


# Extra

Are you interested in more Streamlit demos related to financial data? 

* [Yahoo Finance data web app](https://github.com/paduel/streamlit_finance_chart)


# Contact

* Updated and configured by: Patrick Schneider

* Template by: Darío López Padial (Bukosabino).

Please, let me know about any comment or feedback.

## Setup

```bash
mkdir /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/activate.d/
touch /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/activate.d/env_vars.sh
echo "export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python" >> /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/activate.d/env_vars.sh



mkdir /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/deactivate.d/
touch /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/deactivate.d/env_vars.sh
echo "unset PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION" >> /Users/Patrick/anaconda3/envs/streamlit-eda/etc/conda/deactivate.d/env_vars.sh
```
