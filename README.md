# DMP Evaluation Framework

This is an attempt of creating a framework to evaluate Data Management Plans.

To evaluate qualitatively Data Management Plans (DMPs) but at the same time allow comparing them with each other, a framework is needed. 

A framework is a list of characteristics that are seen as *a priori* desirable in the DMP, so that we can check if the DMP fulfills them or not.
Without a framework, the evaluation would be completely arbitrary and up to the reviewer’s internal standards and expectations. 

Each characteristic, or “criterium”, must be as punctiform as possible as to be just “fulfilled” or “not fulfilled”, reducing the need for interpretation or personal opinion to a minimum.

A criterium looks like this:

---
## [Criterium ID] Criterium short, expressive title
Applicable only if... Scored as ...

A longer description of the criterium, claryfing what parts of the DMP it is trying to check, and how.
Also describes exceptions and additional requirements if the criterium title is too short to contain them.

**Rationale**: The reason why this criterium was created in the first place.

Examples of phrases in the DMP that would fulfill this criterium, and phrases that would not satisfy it.

---

Each criterium is scored in two ways: fully boolean (1 or 0) or partial (1, 0.5 or 0).
The criterium description tells you what they mean, especially for partial compliance.

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

### A note about software
Software is executable data.
Treat it like a normal data type but consider if it can be used on its own (e.g. executable files) or requires specific runtime environments (e.g. python scripts, R scripts, some executable files require external libraries, etc...).

### A note about examples
All examples are completely fabricated, and might mention non-existing repositories, improbable situation or otherwise absurd suggestions.
They are only there to give a sense of which statements might fulfill each criterium.

## Criteria weights
Optionally, weights can be applied to each criteria that describes what happens if the criterium is not fulfilled. Suggested weight interpretations are as follows: 
1. Marginally important.
   The quality of the (projected) RDM is marginally affected. 
2. Low importance.
   The quality of the (projected) RDM is impacted slightly, and there might be a small loss of reusability. 
3. Medium importance.
   The ability to work with the data is affected, and the quality of the (projected) RDM in general is diminished.
   There might be repercussions in the quality of the shared data and its ability to be reused. 
4. High importance.
   The quality of the shared data is greatly diminished or impeded, and there might be problems related to data management during the project. 
5. Extreme importance.
   It is impossible or extremely hard to properly manage the project’s data, or key information regarding it is missing.
   Effective data sharing is impossible, and it is impossible to know if problems regarding data may arise during the project.

## Sources
Most of the criteria presented here are inspired by the 
