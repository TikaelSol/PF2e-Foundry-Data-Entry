import regex as re

# rtf reference
# https://www.biblioscape.com/rtf15_spec.htm

ignored_tags = list(map(lambda x: re.compile(x), [
    r"q(l|r|j|c)",  # text alignment
    "ulnone",  # underline none
    "strike0",  # strike none
    "pard",  # remove style of prev paragraph
    "plain",  # reset font
    r"s\d+",  # paragraph style
    r"fi\d+",  # first line indent
    r"li\d+",  # left indent
    r"sl\d+",  # space between lines
    r"slmult\d+",  # spacing multiple
    r"f\d+",  # font id
    r"fs\d+",  # font size
    r"cf\d+",  # foreground color
    r"^marg.*",  # margin-related tags
    r"^pg.*",  # page-related tags
    r"^paper.*",  # paper-related tags
    r"'\d+",  # unicode char supplementary tag
]))

replace_tags = list(map(lambda x: (re.compile(x[0]), x[1]), [
    ["i", "<em>"],
    ["i0", "</em>"],
    ["b", "<strong>"],
    ["b0", "</strong>"],
    ["rquote", "'"],
    ["emdash", "—"],
    ["endash", "–"],
    ["par", "\n"],
    [r"^u(\d+)", lambda m: chr(int(m.group(1)))],  # unicode char
    [r"^_(.*)", lambda m: "-" + m.group(1)],  # non-breaking hyphen
]))


def preformat_rtf(s: str) -> str:
    s = s.replace("\r\n", "")
    s = s.replace("\n", "")

    s = remove_rtf_header(s)
    s = re.sub(r"(?:(?<!\\)\\(?!\\))([^\s]+)\s", process_rtf_tag_group, s)

    s = resort_tags(s)

    # remove opening/closing brackets
    s = re.sub(r"(^\{\s+)|(\s+\}$)", "", s)
    return s


def remove_rtf_header(s: str) -> str:
    """Removes style/font definitions"""
    brackets = re.compile(r"\{(?!\\rtf)[^{}]+\}")
    m = brackets.search(s)
    while m:
        s = s[:m.start(0)] + s[m.end(0):]
        m = brackets.search(s)
    return s


def process_rtf_tag_group(match: re.Match) -> str:
    tags = match.group(1).split("\\")
    if tags[0].startswith("rtf"):
        return ""
    res = ""

    def process_tag(t):
        for r in ignored_tags:
            if r.fullmatch(t):
                return ""
        for e in replace_tags:
            if e[0].fullmatch(t):
                return e[0].sub(e[1], t)
        return "\\" + t

    for t in tags:
        res += process_tag(t)

    # print(match.group(1))
    # print(res)
    return res


def resort_tags(s: str):
    s = re.sub(r"<(\w+)> ", lambda m: " <" + m.group(1) + ">", s)
    s = re.sub(r" </(\w+)>", lambda m: "</" + m.group(1) + "> ", s)

    # stitch over line breaks
    s = re.sub(r"</(\w+)>(\s)<\1>", lambda m: m.group(2), s)

    return s
