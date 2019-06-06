class segment_tree:
    def __init__(self, data, l, r, cmp):
        self.cmp = cmp
        self.data = data
        if l == r - 1:
            self.l, self.r = l, r
            self.value = l
        else:
            self.lt = segment_tree(data, l, int((l + r) / 2), cmp)
            self.rt = segment_tree(data, int((l + r) / 2), r, cmp)
            self.l, self.r = l, r
            self.value = self.cmp(self.lt.value, self.rt.value, data)

    def query(self, l, r):
        if self.l == l and self.r == r:
            return self.value

        if self.rt.l <= l:
            return self.rt.query(l, r)
        elif r <= self.lt.r:
            return self.lt.query(l, r)
        else:
            lans = self.lt.query(l, self.lt.r)
            rans = self.rt.query(self.rt.l, r)
            return self.cmp(lans, rans, self.data)

"""
data = [5, 4, 8, 7, 5, 8, 0]
st = segment_tree(data, 0, 7, lambda x, y, a: x if a[x] < a[y] else y)
while True:
    l, r = int(input("l")), int(input("r"))
    ans = st.query(l, r)
    print(ans, data[ans])
"""