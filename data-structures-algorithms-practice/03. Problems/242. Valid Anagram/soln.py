def isAnagram(s: str, t: str) -> bool:
        count = {}

        for c in s:
            count[c] = count.get(c, 0) + 1

        for c in t:
            count[c] = count.get(c, 0) - 1

        for value in count.values():
            if value != 0:
                return False

        return True