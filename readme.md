# Backtesting Crypto

## Requirments
- Python 3.11.9 (i'm using pyenv with fishshell)
- uv (rust based - python package manger)
    - _On macOS and Linux_
        - curl -LsSf https://astral.sh/uv/install.sh | sh
    - _windows_
        - coming soon
- install the latest backtesting.py version `pip install git+https://github.com/kernc/backtesting.py.git`
- TA Lib
    - `brew install ta-lib` - need ta-lib c library to work with ta-lib python
    - `pip install numpy==1.26.4` - need to ensure that we are using a numpy version lower then 2.0
- install additional deps `pip install pandas`
- Jupyter Noteboks deps
    - `pip install ipykernel` for jupyter notebooks
- CCXT for candle stick data
    - `pip install ccxt`

### Purpose
In this repo i will be learning how to backtest different strategies in crypto using backtesting.py

### Why?
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
 