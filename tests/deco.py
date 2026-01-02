
def sumFunc(func):
    def mdf(*args):
        if args[0] == 5:
            return
        print(f"sum-1 {sum(args)}")
        func(*args)
        print(f"sum-2 {sum(args)}")
    return mdf


@sumFunc
def add(a, b):
    print(a, b)

# add(4,6)

a = {
    "2": "a",
    "4": "r"
}
for c,v in a.items():
    print(c, v)