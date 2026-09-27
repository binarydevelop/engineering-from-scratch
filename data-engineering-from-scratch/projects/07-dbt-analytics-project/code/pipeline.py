import re

def compile_model(sql_content, manifest):
    # Replaces ref('model_name') with target table name
    def replace_ref(match):
        ref_name = match.group(1)
        return manifest.get(ref_name, ref_name)
    return re.sub(r"ref\('([^']+)'\)", replace_ref, sql_content)
