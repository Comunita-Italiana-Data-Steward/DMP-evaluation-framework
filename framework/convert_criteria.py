import json
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess as sb

PDF_PRELUDE = """
#let example_table(ful, not_ful, part_ful: none) = {
  figure(
    if (part_ful == none) {
      table(
        columns: (50%, 50%),
        align: (left),
        table.header(align(center)[*Fulfilled Examples*], align(center)[*Not fulfilled examples*]),
        ful, not_ful
      )
    } else {
      table(
        columns: (33.3%, 33.3%, 33.4%),
        align: (left),
        table.header(align(center)[*Fulfilled Examples*], align(center)[*Partially Fulfilled Examples*], align(center)[*Not fulfilled examples*]),
        ful, part_ful, not_ful
      )
    },
    kind: table
  )
}

"""


def to_pdf(obj, output_path: Path):
    base_str = "\n== \[{id}\] {title}\n{scoring}\n{description}\n"
    formatted_pdf = PDF_PRELUDE

    for criteria in obj:
        this_str = base_str.format(
            id=criteria["id"],
            title=criteria["title"],
            scoring=criteria["scoring"],
            description=criteria["description"],
        )

        if criteria["rationale"] is not None:
            this_str += f"*Rationale*: {criteria['rationale']}\n"

        if criteria["examples"] is not None:
            table_strs = []
            for example in criteria["examples"]:
                blob = [f"- {x}" for x in example["examples"]]
                table_strs.append(f"[{'\n'.join(blob)}]")
            assert len(table_strs) <= 3
            this_str += f"#example_table({', '.join(table_strs)})\n"

        formatted_pdf += this_str

    print(formatted_pdf)

    with NamedTemporaryFile("w") as conn:
        conn.write(formatted_pdf)
        conn.flush()
        print(f"Compiling PDF {conn.name} to {output_path}")
        out = sb.run(["typst", "compile", conn.name, output_path], capture_output=True)

    print(out.stdout.decode("UTF-8"))

    if out.returncode != 0:
        print(out.stderr.decode("UTF-8"))
        out.check_returncode()


def main(args):
    with args.criteria_json.open("r") as obj:
        raw_json = json.load(obj)["criteria"]

    match args.output_type:
        case "pdf":
            to_pdf(raw_json, args.output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("criteria_json", type=Path)
    parser.add_argument("output_type", choices=["pdf"])
    parser.add_argument("output_file", type=Path)

    args = parser.parse_args()

    main(args)
