class A(object):
    def test(self):
        print('In A')


class B(A):
    def test(self):
        super(B, self).test()
        print('In B')


class C(B):
    def test(self):
        super(C, self).test()
        print('In C')


class D(A):
    def test(self):
        super(D, self).test()
        print('in D')


class E(C, D):
    def test(self):
        super(E, self).test()
        print('in E')


print(E.__mro__)
E().test()
