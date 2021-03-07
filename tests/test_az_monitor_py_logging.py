from azfunctionsmonitor import __version__, get_logger


def test_version():
    l = get_logger("foo")
    assert __version__ == '0.1.112'
