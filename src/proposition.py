import spacy

from dep_vars import dep_vars

def ecw_trf_doc(text):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(text)
    return doc

def str_i_lemma():
    for var in dep_vars:
        var_counter[var] = 0
    text = input("Enter your text: ")
    doc = ecw_trf_doc(text)
    full_span = doc[0:]
    fs_root = full_span.root
    data["root node"]["name"] = f"{fs_root.text}_{fs_root.pos_}"
    stack = [("root node", fs_root)]
    for node in stack:
        token = node[1]
        node_key = node[0]
        for dep in dep_vars:
            key = f"{dep}_{var_counter[dep]}"
            for child in token.children:
                if dep == child.dep_ and not (child.dep_ == "punct" and child.text in [".", ",", ":", "!", ";"]):
                    pred_name = f"{child.text}_{child.pos_}"
                    data[key] = {
                        "name": pred_name.lower()
                    }
                    if child.n_rights + child.n_lefts > 0:
                        stack.append((key, child))
            if key not in data:
                data[key] = {
                    "name": "None"
                }
            data[key]["dep"] = dep
            data[key]["children"] = []
            var_counter[dep] = var_counter[dep] + 1  
            data[node_key]["children"].append(key)

    data_to_lf(data["root node"])
    # thy_end = '"\n  by auto\n\n\nend'
    i_and = " \<and> "
    append_i_file(i_and)

def data_to_lf(node):
    append_i_file(node["name"])
    if len(node["children"]) > 0:
        append_i_file("(")
        for idx, child in enumerate(node["children"]):
            data_to_lf(data[child])
            if idx + 1 < len(node["children"]):
                append_i_file(", ")
        append_i_file(")")

def append_i_file(thy_part):
    i_file = open("../theories/Size_Test2.thy", "a")  
    i_file.write(thy_part)

data = {
        "root node": {
            "dep": "ROOT",
            "children": [],
        }
    }
var_counter = {}

str_i_lemma()