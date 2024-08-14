# Backtesting Crypto

## Requirments
- Python 3.11.9
- install the latest backtesting.py version `pip install git+https://github.com/kernc/backtesting.py.git`
- TA Lib
    - `brew install ta-lib` - need ta-lib c library to work with ta-lib python
    - `pip install numpy==1.26.4` - need to ensure that we are using a numpy version lower then 2.0
- install additional deps `pip install yfinance pandas`
- Jupyter Noteboks deps
    - `uv pip install ipykernel` for jupyter notebooks
- CCXT for candle stick data
    - `pip install ccxt`

In this repo i will be learning how to backtest different strategies in crypto with Bitcoin and Ethereum using differnt backtesting libraries like

The goal is to document the journey of learning how to become a quant and deploying stratgies in production

## Watch me build in public

- I endevour to stream weekly Mon-Wed-Friday

https://www.youtube.com/watch?v=-TytHI38sU8&list=PLwbt1uBf9iqAsuCpIwOxrHJlSVCH7SsDY&pp=gAQBiAQB


### Documentation
- https://kernc.github.io/backtesting.py/
- https://numpy.org/
- https://pandas.pydata.org/docs/index.html
- https://ta-lib.org/

#### Todo's

- [ ] add requirments for differnt operating systems like windows and linux (top 5 distros, arch, ubuntu, fedora...etc)
 