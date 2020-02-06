import argparse
import logging
import sys
from logging import getLogger

import pandas as pd

LOG_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}

# ライブラリのLOG設定
logger = getLogger(__name__)


def set_verbose(verbose: str):
    """
    ライブラリを使用する側のlog設定
    """
    # ルートはデフォルトでDEBUG
    root_logger = logging.getLogger('')  # どんなモジュール、パッケージでも
    root_logger.setLevel(logging.DEBUG)

    # コンソールへの出力設定
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL[verbose])
    handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(handler)


# メインとなる処理を書く
def main(arg1: str, arg2: str):
    logger.debug('arg1: ' + arg1)
    logger.debug('arg2: ' + arg2)

    df = pd.read_csv('./pokemon.csv', sep=',')
    logger.debug(df.head(3))


if __name__ == '__main__':
    set_verbose('DEBUG')
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('arg1', type=str)
    parser.add_argument('arg2', type=str)
    args = parser.parse_args()
    main(args.arg1, args.arg2)

    logger.debug('Python script finished!')
