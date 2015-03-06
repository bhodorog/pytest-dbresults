pytest_plugins = ("pytester",)


def test_properly_initialized(testdir):
    result = testdir.runpytest("--help")
    assert result.ret == 0
    result.fnmatch_lines("--dbresults")
