from hstest import FlaskTest, dynamic_test

from .base import (
    test_correct_request,
    test_bad_request
)


class ServerTest(FlaskTest):
    source = 'app'

    funcs = [
        test_correct_request,
        test_bad_request
    ]

    @dynamic_test(data=funcs)
    def test_correct_request(self, func):
        return func(self)


if __name__ == '__main__':
    ServerTest().run_tests()
