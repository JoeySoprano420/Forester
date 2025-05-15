import os

# Create a sample .fstr file with Hasm block
hasm_sample_code = """\
Start Main

:hasm
    [0000] B0 4F              ; MOV AL, 0x4F
    [0002] E8 05 00 00 00     ; CALL 0x0007
    [0007] C3                 ; RET
:endhasm

Stop
"""

# Create a basic .tmLanguage syntax highlighter for Hasm mode
tm_language_json = {
    "name": "Forester + Hasm",
    "scopeName": "source.forester",
    "patterns": [
        {
            "name": "keyword.control.forester",
            "match": "\\b(Start|Stop)\\b"
        },
        {
            "name": "keyword.control.hasm",
            "match": "(:hasm|:endhasm)"
        },
        {
            "name": "constant.numeric.hex.forester",
            "match": "\\b[0-9A-Fa-f]{2}\\b"
        },
        {
            "name": "comment.line.semicolon.forester",
            "match": ";.*$"
        }
    ],
    "fileTypes": ["fstr"],
    "uuid": "c2038c4c-5c79-4b25-baad-hex-embed"
}

# Save sample files to /mnt/data
sample_path = "/mnt/data/forester_hasm_sample.fstr"
tm_language_path = "/mnt/data/forester_hasm.tmLanguage.json"

with open(sample_path, "w") as fstr_file:
    fstr_file.write(hasm_sample_code)

import json
with open(tm_language_path, "w") as tm_file:
    json.dump(tm_language_json, tm_file, indent=4)

(sample_path, tm_language_path)
