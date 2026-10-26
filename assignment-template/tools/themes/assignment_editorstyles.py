"""Map standard Pygments token classes to documented editor palettes.

This is lexical highlighting: no project index, type checker, or IDE service
is invoked. See tools/SOURCES.md for upstream palette references.
"""
from pygments.style import Style
from pygments.token import Token, Text, Comment, Keyword, Name, String, Number, Operator, Punctuation, Error, Generic


class DarculaStyle(Style):
    name = "Assignment Darcula"
    background_color = "#2B2B2B"
    highlight_color = "#323232"
    styles = {
        Token: "#A9B7C6", Text: "#A9B7C6",
        Comment: "#808080", Comment.Special: "#629755",
        Comment.Preproc: "#CC7832",
        Keyword: "#CC7832", Operator.Word: "#CC7832",
        Name: "#A9B7C6", Name.Function: "#FFC66D",
        Name.Decorator: "#BBB529", Name.Builtin: "#8888C6",
        Name.Builtin.Pseudo: "#CC7832", Name.Variable.Instance: "#9876AA",
        Name.Constant: "#9876AA", Name.Tag: "#E8BF6A",
        Name.Attribute: "#BABABA", Name.Exception: "#A9B7C6",
        String: "#6A8759", String.Doc: "#629755",
        String.Escape: "#CC7832", String.Interpol: "#CC7832",
        Number: "#6897BB", Operator: "#A9B7C6", Punctuation: "#A9B7C6",
        Error: "#FF6B68", Generic.Deleted: "#FF6B68", Generic.Inserted: "#6A8759",
    }


class IntelliJLightStyle(Style):
    name = "Assignment IntelliJ Light"
    background_color = "#FFFFFF"
    highlight_color = "#F2F2F2"
    styles = {
        Token: "#000000", Comment: "italic #808080",
        Comment.Preproc: "#808000", Keyword: "bold #000080",
        Operator.Word: "bold #000080", Name: "#000000",
        Name.Decorator: "#808000", Name.Builtin: "#8888C6",
        Name.Builtin.Pseudo: "bold #000080", Name.Variable.Instance: "#660E7A",
        Name.Constant: "#660E7A", String: "bold #008000",
        String.Doc: "#808080", String.Escape: "bold #000080",
        Number: "#0000FF", Operator: "#000000", Punctuation: "#000000",
        Error: "#D00000",
    }


class VSCodeDarkStyle(Style):
    name = "Assignment VS Code Dark+"
    background_color = "#1E1E1E"
    highlight_color = "#264F78"
    styles = {
        Token: "#D4D4D4", Comment: "#6A9955", Comment.Preproc: "#569CD6",
        Keyword: "#C586C0", Keyword.Declaration: "#569CD6",
        Keyword.Type: "#569CD6", Keyword.Constant: "#569CD6",
        Keyword.Namespace: "#C586C0", Operator.Word: "#569CD6",
        Name: "#9CDCFE", Name.Function: "#DCDCAA", Name.Builtin: "#DCDCAA",
        Name.Builtin.Pseudo: "#569CD6", Name.Class: "#4EC9B0",
        Name.Exception: "#4EC9B0", Name.Namespace: "#4EC9B0",
        Name.Decorator: "#DCDCAA", Name.Constant: "#4FC1FF",
        Name.Tag: "#569CD6", Name.Attribute: "#9CDCFE",
        String: "#CE9178", String.Escape: "#D7BA7D", String.Interpol: "#569CD6",
        Number: "#B5CEA8", Operator: "#D4D4D4", Punctuation: "#D4D4D4",
        Error: "#F44747",
    }


class MatlabLightStyle(Style):
    name = "Assignment MATLAB Light"
    background_color = "#FFFFFF"
    highlight_color = "#F3F3F3"
    styles = {
        Token: "#000000", Comment: "#028009", Keyword: "#0E00FF",
        Name: "#000000", Name.Builtin: "#000000", String: "#AA04F9",
        Number: "#000000", Operator: "#000000", Punctuation: "#000000",
        Generic.Prompt: "#B28C00", Error: "#C40000",
    }
