def soln(strs):
    m = {}

    for s in strs:
        key = ''.join(sorted(s))
        m[key].append(s)

    return list(m.values())