import json
from pathlib import Path
from sys import exit, stdin

from jsonschema import exceptions as schema_exceptions
from jsonschema import validate

"""
This is a thin wrapper around the validate function of python-jsonschema
to validate whatever is inside the file fed to it.
"""

USAGE = """
Usage:
    validate_schema.py <schema>
"""


def main(args):
    with args.schema.open("r") as stream:
        schema = json.load(stream)

    if args.data is None:
        data = json.load(stdin)
    else:
        with args.data.open("r") as stream:
            data = json.load(stream)

    try:
        validate(schema=schema, instance=data)
    except schema_exceptions.SchemaError as e:
        res = ["SCHEMA ERROR", "", "The provided schema is invalid:", str(e)]
        print("\n".join(res))
        exit(1)
    except schema_exceptions.ValidationError as e:
        res = [
            "VALIDATION ERROR",
            "",
            "Provided data does not adhere to the schema.",
            "",
            f"Error: {e.message}",
            f"Location: {'/'.join([str(x) for x in e.absolute_path])}",
            f"Does not adhere to rule: {'/'.join([str(x) for x in e.absolute_schema_path])}",
        ]

        print("\n".join(res))
        exit(1)
    except Exception as e:
        print(e)
        exit(1)

    print("Data is valid!")
    exit(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="validate_schema.py", usage="%(prog)s [arguments]"
    )

    parser.add_argument(
        "schema", type=Path, help="path to the schema used to validate with."
    )

    parser.add_argument(
        "data",
        type=Path,
        help="path to the data to validate. If missing, reads from STDIN.",
        nargs="?",
        default=None,
    )

    args = parser.parse_args()

    main(args)
