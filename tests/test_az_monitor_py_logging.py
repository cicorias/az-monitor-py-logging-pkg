from azfunctionmon import __version__, LoggingHelper, get_logger


def test_version():
    l = LoggingHelper("foo")
    assert __version__ == '0.1.0'
