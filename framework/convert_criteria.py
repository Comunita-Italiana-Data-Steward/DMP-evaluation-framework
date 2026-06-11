import csv
import json
import subprocess as sb
from pathlib import Path
from tempfile import NamedTemporaryFile

from jsonschema.validators import validate

"""
This script converts the criteria file into some other file format.

It fist validates the data against the schema, to check for any problems before
proceeding.

TODO: This template doesn't really handle more than three examples.
"""

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

#set page(paper:"a4")

= DMP Evaluation Criteria

"""


def to_pdf(obj, output_path: Path):
    base_str = "\n== \\[{id}\\] {title}\n{scoring}\n\n{description}\n"
    formatted_pdf = PDF_PRELUDE

    for criteria in obj:
        this_str = base_str.format(
            id=criteria["id"],
            title=criteria["title"],
            scoring=criteria["scoring"],
            description=criteria["description"],
        )

        if criteria["rationale"] is not None:
            this_str += f"\n*Rationale*: {criteria['rationale']}\n"

        if criteria["examples"] is not None:
            table_strs = []
            for example in criteria["examples"]:
                blob = [f"- {x.strip()}" for x in example["examples"]]
                table_strs.append(f"[{'\n'.join(blob)}]")
            assert len(table_strs) <= 3
            if len(table_strs) < 3:
                this_str += f"#example_table({', '.join(table_strs)})\n"
            else:
                this_str += f"#example_table({table_strs[0]}, {table_strs[2]}, part_ful:{table_strs[1]})"

        formatted_pdf += this_str

    # Sanitize possible escape codes
    formatted_pdf = formatted_pdf.replace("@", r"\@")

    with NamedTemporaryFile("w") as conn:
        conn.write(formatted_pdf)
        conn.flush()
        print(f"Compiling PDF {conn.name} to {output_path}...")
        out = sb.run(["typst", "compile", conn.name, output_path], capture_output=True)

    print(out.stdout.decode("UTF-8"))

    if out.returncode != 0:
        print(out.stderr.decode("UTF-8"))
        out.check_returncode()


def take_section(id):
    pieces = id.split(r".")
    return ".".join(pieces[0:2])


assert take_section("A.one.1") == "A.one"


def to_csv(obj, output_path: Path):
    obj.sort(key=lambda x: x["id"])
    res = [
        ["section", "criteria_id", "criteria"],
    ]
    for criteria in obj:
        res.append([take_section(criteria["id"]), criteria["id"], criteria["title"]])

    print(f"Writing {len(res) - 1} criteria to {output_path}...")
    with output_path.open("w+") as sink:
        writer = csv.writer(sink, delimiter=",")
        writer.writerows(res)


def main(args):
    with args.criteria_json.open("r") as obj:
        raw_json = json.load(obj)

    if not args.skip_validation:
        if args.schema is None:
            raise ValueError(
                "No schema provided, and validation is requested (pass --skip-validation to skip)"
            )
        with args.schema.open("r") as obj:
            schema = json.load(obj)

        print("Validating data using provided schema...")
        validate(schema=schema, instance=raw_json)
        print("Data adheres to the JSON schema!")

    match args.output_type:
        case "pdf":
            to_pdf(raw_json["criteria"], args.output_file)
        case "csv":
            to_csv(raw_json["criteria"], args.output_file)

    print("Done!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "criteria_json", type=Path, help="(Full) path to the criteria in JSON format"
    )
    parser.add_argument(
        "output_type",
        choices=["pdf", "csv"],
        help="Desired output format. Currently supports only PDF",
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Path to the output file. Extension is NOT set automatically",
    )
    parser.add_argument(
        "schema",
        type=Path,
        nargs="?",
        default=None,
        help="Path to the schema file for preliminary validation",
    )

    parser.add_argument(
        "-s",
        "--skip-validation",
        action="store_true",
        help="Skip validation before conversion",
    )

    args = parser.parse_args()

    main(args)
