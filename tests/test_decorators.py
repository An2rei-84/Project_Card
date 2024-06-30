from src.decorators import log


def test_log_correct(capsys):
    @log()
    def my_function(x, y):
        return x + y
    my_function(5, 5)
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n\n"


def test_log_not_correct(capsys):
    @log()
    def my_function(x, y):
        return x / y
    my_function(5, 0)
    captured = capsys.readouterr()
    assert captured.out == 'my_function error: ZeroDivisionError. Inputs: (5, 0), {}\n\n'
