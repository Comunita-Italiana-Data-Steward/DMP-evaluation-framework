# DMP Evaluation Framework
[![All Contributors](https://img.shields.io/github/all-contributors/Comunita-Italiana-Data-Steward/DMP-evaluation-framework?color=ee8449&style=flat-square)](#contributors)

This is an attempt of creating a framework to evaluate Data Management Plans (DMPs) throughout their lifetime.

With "DMP Framework" we mean a list of characteristics that are seen as *a priori* desirable in the DMP, so that we can check if the DMP fulfills them or not.

Without a framework, the evaluation would be completely arbitrary and up to the reviewer’s internal standards and expectations.

This is the sister repository to the [Guide on Writing Data Management Plans](https://github.com/Comunita-Italiana-Data-Steward/DMP-guide).

## Evaluation criteria
Each characteristic, or “criterium”, must be as punctiform as possible as to be just “fulfilled” or “not fulfilled”, reducing the need for interpretation or personal opinion to a minimum.

A criterium looks like this:

---
## [Criterium ID] The criterium short, expressive title
Applicable only if... Scored as ...

A longer description of the criterium, claryfing what parts of the DMP it is trying to check, and how.
Also describes exceptions and additional requirements if the criterium title is too short to contain them.

**Rationale**: The reason why this criterium was created in the first place.

Examples of phrases in the DMP that would fulfill this criterium, and phrases that would not satisfy it.

---

To increase machine interoperability, the criteria are stored as a JSON list, in which each item is a dictionary containing information for a single criteria.

The structure of the JSON file adheres to the included [JSON Schema](https://json-schema.org/) file available [here](framework/criteria/criteria.schema.json).
In short, it is a list of criteria (under the key `criteria`), each looking like this:

```json
{
    "id": "X.xxx.1",
    "title": "Title of criterium",
    "scoring": "Scored as ...",
    "description": "The longer description of the criterium",
    "rationale": "The rationale of the criterium, or NULL",
    "examples": [ // This may be NULL if no examples are provided
        {
            "title": "First example title",
            "examples": [
                "First example, line 1",
                "First example, line 2",
                "..."
            ]
        },
        {
          "title": "Second example title",
          "examples": [
              "Second example, line 1",
              "Second example, line 2",
              "..."
          ]
        }
    ]
}
```

### Converting from JSON
Working with JSON while using the framework is unwieldy.
To side-step this, a Python script ([`convert_criteria.py`](framework/convert_criteria.py)) is available to convert the JSON file to either PDF or CSV.

Use it by installing the required packages (see the [`requirements.txt`](requirements.txt) file) and launching (inside the `framework` folder):

To get a CSV file:
```bash
python convert_criteria.py -s criteria/criteria.json csv out.csv
```

To get a PDF file:
```bash
python convert_criteria.py -s criteria/criteria.json pdf out.pdf
```
In any case, you can learn more about how to use the script with `python convert_criteria.py --help`.

## Criteria characteristics

Each criterium has a few characteristics.
Here they are described in detail:

### Scoring
Each criterium is scored in two ways: fully boolean (1 or 0) or partial (1, 0.5 or 0).
The criterium description tells you what they mean, especially for partial compliance.

### Applicability
Criteria starting with “IA” (If Applicable), might not be relevant to every DMP.
The description of the criterium states where it is applicable.
If not relevant, score that point as NA.
To the discretion of reviewers, a required criterium may still be deemed not applicable.
If so, please provide an explanation together with the assessment as to why the point was so.
Some criteria start with “IP” (if previous), and are only applicable if a previous criterium has a specific value.
If this is not the case, they are marked as NA.
The description of the criterium specifies the dependency relation. 

As DMPs might be varied, scoring software should treat missing values (NAs) as possible in every criteria, not just those listed here, in case the expert reviewer decides that a criterium that the framework assumes is mandatory does not apply in the specific case they are reviewing.
However, consider that all mandatory criteria have been considered under a variety of scenarios and are broadly applicable.

Usually, criteria starting with “Indicates...” require mandatory information.
It is not enough to state that this information is not given for X or Y reasons.
On the other hand, criteria starting with “Addresses...” can be fulfilled by a rejection statement (“Information is not give due to...”), if the omission is properly defended.

### Criteria weights
Optionally, weights can be applied to each criteria that describes what happens if the criterium is not fulfilled. Suggested weight interpretations are as follows: 
1. **Marginally important.**
   The quality of the (projected) RDM is marginally affected. 
2. **Low importance.**
   The quality of the (projected) RDM is impacted slightly, and there might be a small loss of reusability. 
3. **Medium importance.**
   The ability to work with the data is affected, and the quality of the (projected) RDM in general is diminished.
   There might be repercussions in the quality of the shared data and its ability to be reused. 
4. **High importance.**
   The quality of the shared data is greatly diminished or impeded, and there might be problems related to data management during the project. 
5. **Extreme importance.**
   It is impossible or extremely hard to properly manage the project’s data, or key information regarding it is missing.
   Effective data sharing is impossible, and it is impossible to know if problems regarding data may arise during the project.

> [!IMPORTANT]
> Currently, the JSON file does not contain any weights.
> They will be potentially added later on.

## Important concepts to keep in mind
The criteria have been developed with the following non-intuitive opinions in mind.
Do consider them if you plan to use the framework to evaluate your own DMPs.

### A note about software
Software is executable data.
Treat it like a normal data type but consider if it can be used on its own (e.g. executable files) or requires specific runtime environments (e.g. python scripts, R scripts, some executable files require external libraries, etc...).

### A note about examples
All examples are completely fabricated, and might mention non-existing repositories, improbable situation or otherwise absurd suggestions.
They are only there to give a sense of which statements might fulfill each criterium.

## Sources
Most of the criteria presented here are inspired by the [ScienceEurope DMP Evaluation Guide](https://scienceeurope.org/our-resources/practical-guide-to-the-international-alignment-of-research-data-management/).
The criteria presented in the document were heavily expanded and iterated upon to create the framework.

## Contributing to the guide
The framework is open for contributions from everyone!
Please refer to the [Contributing Guide](CONTRIBUTING.md) for more information.

Contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md) of this repository.

> [!TIP]
> You don't need any particular experience to contribute!
> We accept and treasure contributions also from non-experts in the field of DMP writing or reviewing, such as fixing typos, providing feedback, and more.
> Refer to the contributing guide to learn more.
> Thank you!

## Citing the framework
If you use the framework and would like to cite it, please use the following:
> "DMP Evaluation Framework", Comunita' Italiana Data Steward, https://github.com/Comunita-Italiana-Data-Steward/DMP-evaluation-framework

> [!NOTE]
> A proper DOI will come soon!

## Useful contacts
This project is part of the Comunita' Italiana Data Steward (CIDS), and in particular in the Gruppo di Lavoro Data Management Plan (GdL DMP).

If you wish to get in touch, you may contact [anyone on the Coordinator Board of the CIDS](https://github.com/Comunita-Italiana-Data-Steward/.github/blob/main/COORDINATORS.md), or, for issues regarding this project in particular, the co-chairs of the GdL DMP:
- Andrea Tarallo (andrea.tarallo@cnr.it)
- Luca Visentin (luca.visentin@polimi.it)

## All contributors

All contributions to this project are tracked by the [All Contributors Bot](https://allcontributors.org/en/).

Thank you to these wonderful people!
<!-- THIS NEXT LINE MUST REMAIN EMPTY! -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://mrhedmad.github.io/blog/"><img src="https://avatars.githubusercontent.com/u/46203625?v=4?s=100" width="100px;" alt="Luca "Hedmad" Visentin"/><br /><sub><b>Luca "Hedmad" Visentin</b></sub></a><br /><a href="#code-MrHedmad" title="Code">💻</a> <a href="#doc-MrHedmad" title="Documentation">📖</a> <a href="#infra-MrHedmad" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#projectManagement-MrHedmad" title="Project Management">📆</a> <a href="#tool-MrHedmad" title="Tools">🔧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
