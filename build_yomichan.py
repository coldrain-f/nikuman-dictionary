import pyglossary
import os

pyglossary.Glossary.init()
glos = pyglossary.Glossary()

input_file = r"resources\stardict\Ja-Ko_DIC_2018.ifo"
output_file = r"resources\yomitan\Ja-Ko_DIC_2018.zip"

print("Reading StarDict...")
glos.read(input_file, format="StarDict")

options = {
    "rule_v5_defi_pattern": r"\[.*?5단.*?\]",
    "rule_v1_defi_pattern": r"\[.*?[상하]1단.*?\]",
    "rule_vs_defi_pattern": r"\[.*?サ(?:변격| 행| 行).*?\]",
    "rule_vk_defi_pattern": r"\[.*?カ(?:변격| 행| 行).*?\]",
    "rule_adji_defi_pattern": r"\[형용사\]|\[형용사ク활용\]"
}

print(f"Writing Yomichan with options: {options}")
glos.write(output_file, format="Yomichan", **options)
print("Done!")
