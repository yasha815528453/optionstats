from tdamodule import tdamethods
import datetime
import sys
import pymysql
import pymysql.cursors
import json
from database import methods



connection = methods.acquire_connection()
methods.sector_perf_aggre(connection)

methods.release_connection(connection)
