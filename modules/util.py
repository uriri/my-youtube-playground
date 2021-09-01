def delete_unused_char_for_dir_name(origin_str: str) -> str:
    """Windowsディレクトリ名で使用できない文字を_に変換する

    Args:
        origin_str (str): 変換元文字列

    Returns:
        str: 変換後文字列
    """
    return origin_str.translate(
        str.maketrans(
            {
                "\\": "_",
                "/": "_",
                ":": "_",
                "：": "_",
                "*": "_",
                "?": "_",
                "？": "_",
                '"': "_",
                ">": "_",
                "<": "_",
                "|": "_",
            }
        )
    )
