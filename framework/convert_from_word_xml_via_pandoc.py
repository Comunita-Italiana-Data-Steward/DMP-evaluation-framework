import xml.etree.ElementTree as ET
import json
from pathlib import Path

"""Converts the Word XML obtained via Pandoc to the Json file

This requires that <Bold>, <Link> and <Emph> tags are removed manually from the
input XML. Plus, it relies on the word document following a very specific format
(the one of the initial draft of it.)

it doesn't do a perfect job, so the output needs to be checked manually.
It does most of the job, however.
"""

tree = ET.parse("criteria.xml")
root = tree.getroot()
blocks = root[1]


def split_first_whitespace(line):
    pieces = line.split()
    return [pieces[0], " ".join(pieces[1:])]


assert split_first_whitespace("hello how are you") == ["hello", "how are you"]


class LineProcessor:
    def __init__(self):
        self.criteria = []
        self.has_open_criteria = False
        self.current_id = None
        self.current_title = None
        self.current_scoring = None
        self.current_scoring_type = None
        self.current_description = []
        self.current_examples = None
        self.current_para_id = 0

    def gobble_line(self, line):
        if line.tag == "Header" and line.attrib["level"] == "3":
            print("Found new criterium header")
            if self.has_open_criteria:
                print("Flushing open criterium")
                self.flush()
            self.has_open_criteria = True
            pieces = split_first_whitespace(line.text)
            self.current_id = pieces[0].strip("[]").strip()
            self.current_title = pieces[1].strip()
            return

        if not self.has_open_criteria:
            return

        if line.tag == "Para":
            self.current_para_id += 1
            if self.current_para_id == 1:
                # This is a scoring string
                self.current_scoring = line.text
                return
            if line.text is None:
                return
            self.current_description.append(line.text)
        if line.tag == "Table":
            self.process_table(line)

    def process_table(self, element):
        print("Processing a table...")
        headers = element.find("TableHead").find("Row")  # enters the first and only row
        examples = []
        for cell in headers:
            examples.append({"title": cell.find("Plain").text, "examples": []})
        body = (
            element.find("TableBody").find("body").find("Row")
        )  # enters the first and only row

        for i, cell in enumerate(body):
            bullets = cell.find("BulletList")
            content = [x.find("Para").text for x in bullets]
            examples[i]["examples"] = content

        if len(examples) == 2:
            self.current_scoring_type = "boolean"
        elif len(examples) == 3:
            self.current_scoring_type = "partial"
        else:
            raise ValueError("Unknown Scoring type")

        self.current_examples = examples

    def flush(self):
        if len(self.current_description) > 1 and self.current_description[
            -1
        ].startswith("Rationale"):
            rationale = self.current_description[-1][
                11:
            ]  # Strips 'rationale: ', in any order
            description = "\n".join(self.current_description[:-1])
        else:
            rationale = None
            description = "\n".join(self.current_description)

        data = {
            "id": self.current_id,
            "title": self.current_title,
            "scoring": self.current_scoring,
            "description": description,
            "rationale": rationale,
            "examples": self.current_examples,
        }
        self.criteria.append(data)
        self.reset()

    def reset(self):
        self.current_examples = None
        self.current_scoring = None
        self.current_id = None
        self.current_title = None
        self.current_description = []
        self.current_scoring_type = None
        self.current_para_id = 0


gobbler = LineProcessor()
for child in blocks:
    gobbler.gobble_line(child)

gobbler.flush()

with Path("/home/hedmad/Desktop/criteria.json").open("w+") as obj:
    json.dump({"criteria": gobbler.criteria}, obj, indent=4)
