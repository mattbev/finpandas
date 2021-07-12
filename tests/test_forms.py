import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from finpandas import dispose, fundamentals
from finpandas.dataframes import Form10K, Form10Q, HistoricalStockPrices

###########################################################################
######################### Basic Operational Tests #########################
###########################################################################



###########################################################################
############################## Validity Tests #############################
###########################################################################

dispose()
