from Twitter_Utils.EternalProcess import EternalProcess  # pragma: no cover
from urllib3.contrib import pyopenssl # pragma: no cover

pyopenssl.inject_into_urllib3() # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    process = EternalProcess()
    process.start_process()
