from azfunctionsmonitor import __version__, get_logger


def test_version():
    logger = get_logger("foo")
    logger.debug("heelo")
    assert __version__ == "0.1.112"


if __name__ == "__main__":
    print("test run directly")
    test_version()
else:
    print("run under pytest..")
