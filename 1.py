class Porple:
    age = 18

    @staticmethod
    def pl3(nb):
        print("这是类和对象都可使用的静态方法，age=", nb)

    def pl1(self):
        print("这是绑定给对象的动态方法，age=", self.age)

    @classmethod
    def pl2(self):
        print("这是绑定给类的动态方法，age=", self.age)


man = Porple()
man.pl3(man.age)
man.pl3(Porple.age)
man.age = 20
man.pl3(man.age)
man.pl3(Porple.age)

man.pl2()
print(Porple.age)
print(man.age)
man.age = 22
man.pl2()


print(Porple.age)
print(man.age)
man.pl1()
man.age = 20
man.pl1()

