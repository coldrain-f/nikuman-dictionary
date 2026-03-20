import subprocess

cmd = [
    r"C:\Users\User\AppData\Local\Programs\Python\Python313\Scripts\pyglossary.exe",
    r"resources\stardict\Ja-Ko_DIC_2018.ifo",
    r"resources\yomitan\Ja-Ko_DIC_2018.zip",
    "--write-format=Yomichan",
    "--write-options", r"rule_v5_defi_pattern=\[.*?5단.*?\]",
    "--write-options", r"rule_v1_defi_pattern=\[.*?[상하]1단.*?\]",
    "--write-options", r"rule_vs_defi_pattern=\[.*?サ(?:변격| 行).*?\]",
    "--write-options", r"rule_vk_defi_pattern=\[.*?カ(?:변격| 行).*?\]",
    "--write-options", r"rule_adji_defi_pattern=\[형용사\]|\[형용사ク활용\]"
]

print("Running PyGlossary with custom Yomichan formatting rules...")
result = subprocess.run(cmd)
print(f"Exit code: {result.returncode}")
