import re


def get_i18n(i18n_response: str):
    reg_script = '{name}\("{id}",({fn}|{quote}{any}{quote})\)'.format(
        quote="[\"']",
        name="([a-z])",
        id="([a-z0-9]{8})",
        any="([\s\S]*?)",
        fn="\(function\([aent]\){return([\s\S]*?)}\)",
    )

    return {
        script[1]: script[4]
        if script[3] == ""
        else i18n_format(script[3].strip().lstrip().strip('"').lstrip('"'))
        for script in re.findall(reg_script, i18n_response)
    }


def i18n_format(script):
    output = re.sub(
        "{join_first}{name}\([aent]\.{placeholder},{any}\)(?={join_last})".format(
            join_first="((\"|')?\+|^)",
            join_last="(\+(\"|')?|\Z)",
            name="([a-z])",
            any="([\s\S]*?)",
            placeholder="([A-Za-z0-9_]*)",
        ),
        r"\1({\4},\5)",
        script,
    )
    output = re.sub(
        "{join_first}[aent]\.{placeholder}(?={join_last})".format(
            join_first="((\"|')?\+|^|,)",
            join_last="(\+(\"|')?|\Z|\))",
            placeholder="([A-Za-z0-9_]*)",
        ),
        r"\1{\3}",
        output,
    )

    return output.replace('"', "").replace("+", "")
