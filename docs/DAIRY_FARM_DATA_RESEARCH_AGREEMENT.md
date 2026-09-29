# Dairy Farm Data Student Research Agreement

> **Template and legal-review notice:** This agreement is a practical starting point for a student research project and is not legal advice. Complete every bracketed field before signing. The student must consult the faculty supervisor and any required institutional office before collecting or using data. If the project involves information about people, animal interventions, confidential business information, or publication beyond the course, additional review may be required.

This Dairy Farm Data Student Research Agreement (the **“Agreement”**) is effective **[date]** between:

- **Data Provider/Farm:** [legal name and address] (**“Farm”**);
- **Student Researcher:** [student name, institution, course, email] (**“Student”**); and
- **Faculty Supervisor:** [name, title, department, email] (**“Supervisor”**).

The Farm and Student are the **“Parties.”** The Supervisor acknowledges the project but is not a party, and the Student cannot bind the institution, unless an authorized institutional representative signs a separate written agreement.

## 1. Project purpose and scope

The Farm permits the Student to use the data listed in Schedule A solely for the following noncommercial academic project:

**Project title:** Dairy Cow Missing-Data Prediction  
**Course/program:** [course number and title]  
**Purpose:** Evaluate reproducible methods for cleaning dairy-cow milking records and estimating missing milk-yield or milk-flow values. Missing animal identifiers may be investigated as a separate record-linkage problem, but an identifier will not be guessed when the evidence is ambiguous.  
**Expected outputs:** [course notebook, report, presentation, poster, or other]  
**Project end date:** [date]

The Student may clean, transform, summarize, visualize, and analyze the Farm Data and may train project-specific statistical or machine-learning models for this purpose. A new research question, public dataset release, commercial activity, or other materially different use requires the Farm’s prior written permission and any required institutional approval.

## 2. Data covered

**“Farm Data”** means only the files and fields described in Schedule A, including any copies or derived row-level datasets. It may include animal identifiers, event dates, lactation information, reproduction status, milk yield, milk flow, milking duration, and related metadata.

Farm Data does not include employee, customer, financial-account, veterinary-client, or other personal information unless Schedule A expressly identifies it and the Student documents the authority and approvals required to use it. The Farm should remove unnecessary direct identifiers before transfer when practical.

## 3. Voluntary participation and authority

The Farm represents that it owns the Farm Data or has authority to provide it for the stated project and will disclose known third-party restrictions. Participation is voluntary. The Farm may decline to provide any requested field without penalty.

The Student will collect the minimum data reasonably needed for the project and will not represent that Cornell University or another institution has approved the project unless that approval has been obtained.

## 4. Ownership and limited research permission

The Farm retains its rights in the original Farm Data. No ownership of the Farm, animals, records, trade secrets, or other Farm property is transferred.

The Farm grants the Student a nonexclusive, nontransferable, royalty-free right, during the Agreement term, to receive, copy, clean, analyze, and create research outputs from the Farm Data solely for the project described in Section 1.

Subject to applicable course and institutional policies, the Student retains rights in original code, documentation, and written analysis. Those rights do not permit disclosure or redistribution of identifiable or row-level Farm Data. Models or outputs that could reasonably reveal confidential records remain subject to this Agreement.

## 5. Permitted users and systems

Access is limited to:

1. the Student;
2. the Supervisor and course instructor; and
3. project teammates or service providers specifically named in Schedule A and bound by equivalent confidentiality duties.

Approved storage and analysis systems are listed in Schedule A. The Student may keep code and nonconfidential documentation in a public GitHub repository, but must not commit or upload Farm Data, row-level derived data, credentials, private reports, or outputs containing identifiable records. The repository must use `.gitignore` or equivalent controls for private data, but technical controls do not replace the Student’s obligation to review every commit before pushing.

## 6. Confidentiality and de-identification

The Student will treat animal identifiers, precise locations, business records, operational details, and any information marked or reasonably understood as confidential (**“Confidential Farm Data”**) as confidential.

Before sharing results outside the approved users, the Student will:

- remove direct farm and animal identifiers;
- generalize or suppress precise dates, locations, rare characteristics, and small groups when needed to reduce re-identification risk;
- report aggregated results using a minimum group size of **[five farms/animals/other threshold]**, unless the Farm approves another threshold in writing; and
- check figures, notebook outputs, logs, screenshots, and model artifacts for accidental disclosure.

The Student will not attempt to re-identify de-identified records and will not identify the Farm publicly without specific written consent.

These duties do not apply to information the Student can document was lawfully public, already lawfully known without restriction, independently developed without Farm Data, or lawfully received from another source without a confidentiality duty.

## 7. Data cleaning, imputation, and model integrity

The Student will preserve the original data unchanged and perform cleaning on documented copies. The Student will distinguish existing missing values from zero values and will convert zeros to missing only when the data documentation or the Farm confirms that zero is a missing-value code. Cleaning decisions, exclusions, transformations, and assumptions will be recorded.

Observed and predicted values will be stored in separate fields. Predictions will include a method or imputation flag and, when practical, an uncertainty or confidence measure. The Student will not present predicted values as observations supplied by the Farm.

The Student will use leakage-resistant train, validation, and test procedures appropriate for repeated animal records, evaluate performance on held-out observed values, report limitations, and avoid claims beyond the evidence. Research outputs are not veterinary, financial, legal, regulatory, or farm-management advice.

## 8. Artificial intelligence and automated-model restrictions

The Farm authorizes use of Farm Data only for project-specific analysis and models run by the approved users on approved systems. Unless separately authorized in writing, Farm Data may not be:

- used to train or improve a general-purpose or foundation AI model;
- entered into a public consumer AI service or any service that retains inputs for unrelated model training;
- sold, licensed, or used to develop a commercial product; or
- used for automated decisions about credit, insurance, pricing, employment, eligibility, land value, regulatory status, or legal liability.

If the Student proposes a new cloud or AI service, the Student must first document its data retention, training, access, and deletion terms and obtain written approval from the Farm and Supervisor.

## 9. FAIR data stewardship

The Parties intend to apply the FAIR principles—Findable, Accessible, Interoperable, and Reusable—subject to confidentiality and the access limits in this Agreement. **FAIR does not mean that confidential Farm Data must be public.**

- **Findable:** Maintain a project identifier, version history, data dictionary, provenance, and descriptive metadata that do not reveal protected details.
- **Accessible:** Keep Farm Data closed or controlled as selected in Schedule B. Document how an authorized person may request access.
- **Interoperable:** Use documented field names, units, date formats, controlled categories, and widely used formats such as CSV when practical.
- **Reusable:** Record collection context, cleaning rules, missing-value codes, quality limits, software versions, and permitted uses. Any secondary use requires the approval stated in Schedule B.

Metadata may remain after the Farm Data is deleted only if it does not reveal confidential or identifiable information.

## 10. Security and incident response

The Student will use safeguards proportionate to the sensitivity of the Farm Data, including:

- institution-managed or encrypted storage where available;
- strong unique passwords and multifactor authentication;
- least-privilege access and no shared credentials;
- encrypted transfer rather than public links or unencrypted email attachments;
- current software and secure backups; and
- secure deletion from active storage and trash when retention ends.

The Student will notify the Farm and Supervisor without unreasonable delay, and when feasible within **[48 hours]** after confirming loss, unauthorized access, or disclosure. The notice will summarize what happened, what data may be affected, and the containment and correction steps, subject to legal or institutional restrictions.

## 11. Publication, attribution, and review

The Student may submit de-identified or aggregated results to the approved course audience listed in Schedule A. Public posting, a conference presentation, publication, or sharing beyond that audience requires **[Farm approval / notice only / no additional approval]** as selected in Schedule A.

At least **[15] days** before a public release, the Student will provide the Farm any material that identifies or could reasonably identify the Farm. The Farm may request correction of factual errors, removal of identifiers, or protection of confidential information. The Farm may not suppress good-faith findings solely because they are unfavorable.

Attribution will be **[anonymous / named acknowledgment with written consent / authorship under stated criteria]**. The Student will not use the Farm’s name, logo, or trademarks without written permission.

## 12. Results, compensation, and costs

- Compensation to Farm: **[none / amount or in-kind benefit]**
- Costs paid by Farm: **[none / describe]**
- Results returned to Farm: **[plain-language summary, figures, or other]**
- Expected delivery date: **[date]**

Unless stated above, this is an unpaid student research project and no particular result or benefit is guaranteed.

## 13. Term, withdrawal, retention, and deletion

This Agreement begins on the effective date and ends on **[date or event]**. The Farm may withdraw permission for future use by written notice to **[contact]**.

Within **[30] days** after withdrawal or the end of the retention period, the Student will stop new use and securely delete or return identifiable Farm Data, except for:

- data already incorporated into a completed submitted assignment or published aggregate result;
- records that have been irreversibly de-identified so they can no longer reasonably be linked to the Farm; and
- temporary backups that cannot reasonably be isolated, provided they remain protected and are deleted through the normal backup cycle.

The Student will document deletion or return upon request. The planned retention period and disposition are specified in Schedule A.

## 14. Required disclosure and compliance

If law, court order, institutional policy, or another binding obligation requires disclosure, the Student will, when legally permitted, promptly notify the Farm and disclose only what is required.

Before collection begins, the Student and Supervisor will determine whether institutional review, informed consent, animal-care review, data-protection review, or other approval is required. The determination and any protocol number must be recorded in Schedule A. This Agreement does not replace an institutional consent form or approval.

## 15. Disclaimers and responsibility

The Farm will provide data in the form reasonably available and does not guarantee that it is complete or error-free. The Student will not knowingly misstate results or attribute a suspected data error to the Farm without reasonable verification and context.

Except for the express commitments in this Agreement, the Farm Data and research outputs are provided “as is.” Any indemnity, limitation of liability, insurance, or waiver must be reviewed and added by authorized counsel; none is created by this template.

## 16. General terms

- **Changes:** Any material change to purpose, data categories, users, public release, AI use, or retention must be written and approved by both Parties.
- **No assignment:** Neither Party may transfer this Agreement without the other Party’s written consent.
- **No partnership:** This Agreement does not create an employment, partnership, agency, or fiduciary relationship.
- **Entire agreement:** This Agreement and its schedules are the complete agreement concerning the Farm Data for this project.
- **Severability:** If one term is unenforceable, the remaining terms continue to the extent permitted by law.
- **Governing law and disputes:** The Parties will first try to resolve concerns through the contacts below. Any additional governing-law or dispute terms must be inserted after appropriate review: **[terms or “not specified”].**
- **Electronic signatures:** Signatures may be electronic and in counterparts.

## 17. Contacts and signatures

| Role | Name | Organization | Email | Phone |
|---|---|---|---|---|
| Farm contact | [Name] | [Farm] | [Email] | [Phone] |
| Student | [Name] | [Institution/course] | [Email] | [Phone] |
| Supervisor | [Name] | [Department] | [Email] | [Phone] |
| Institutional/privacy contact, if applicable | [Name] | [Office] | [Email] | [Phone] |

By signing, the Parties confirm that they have read and agreed to this Agreement and its schedules.

### Farm/Data Provider

Name: ______________________________  
Title: ______________________________  
Signature: ______________________________  
Date: ______________________________

### Student Researcher

Name: ______________________________  
Signature: ______________________________  
Date: ______________________________

### Faculty Supervisor acknowledgment

The Supervisor acknowledges supervision of the described student project. This acknowledgment does not make the Supervisor or institution a Party or create institutional obligations.

Name/Title: ______________________________  
Signature: ______________________________  
Date: ______________________________

---

# Schedule A — Project, Data, and Access Plan

## A1. Project administration

- Farm/Data Provider: **[name]**
- Student: **[name]**
- Course and instructor: **[course; instructor]**
- Supervisor: **[name]**
- Project dates: **[start] to [end]**
- Institutional review determination: **[not required / pending / approved; decision-maker and protocol number]**
- Approved course audience: **[instructor, class, named team]**
- Public release rule: **[Farm approval / advance notice / no public release]**

## A2. Data inventory

| Data category | Expected fields | Date range/frequency | Sensitivity | Required? | Retention/disposition |
|---|---|---|---|---|---|
| Animal record | Coded animal ID | [range] | Potentially identifying within farm | [Yes/No] | [period; delete/return] |
| Milking event | Event date/time, session | [range] | Operational | [Yes/No] | [period; delete/return] |
| Production | Milk yield, average flow, 30–60 second flow, first-two-minute yield, duration | [range] | Confidential production data | [Yes/No] | [period; delete/return] |
| Lactation | Days in milk, lactation number | [range] | Operational | [Yes/No] | [period; delete/return] |
| Reproduction | Reproduction status or coded category | [range] | Animal-management data | [Yes/No] | [period; delete/return] |
| Other | [fields] | [range] | [level] | [Yes/No] | [period; action] |

## A3. Transfer, access, and systems

- Source and format: **[farm system; CSV/other]**
- Secure transfer method: **[approved method]**
- Approved users: **[names or roles]**
- Approved local/institutional storage: **[system/path description]**
- Approved cloud or analysis services: **[none or list]**
- Public code repository: **[URL]**; Farm Data and identifiable outputs are prohibited
- Encryption and backup approach: **[describe]**
- Farmer’s third-party/platform restrictions: **[describe]**
- Known missing-value codes, including meaning of zero: **[describe]**
- Units and data dictionary location: **[describe]**

## A4. Permission selections

Mark each selection clearly.

- Project-specific statistical/ML modeling: **[Allowed / Not allowed]**
- General-purpose AI or foundation-model training: **Not allowed unless separately agreed in writing**
- Public row-level data release: **Not allowed unless separately agreed in writing**
- Commercial use: **Not allowed unless separately agreed in writing**
- Named public acknowledgment: **[Allowed / Not allowed]**
- Farm-specific results returned: **[describe]**

---

# Schedule B — FAIR Implementation Plan

| FAIR area | Project implementation | Confidentiality limit | Responsible person | Review date |
|---|---|---|---|---|
| Findable | Versioned data dictionary, provenance notes, project ID, and non-sensitive metadata | No farm name, exact location, animal ID, or sensitive field-level statistics in public metadata | [Name] | [Date] |
| Accessible | Raw and processed row-level data kept closed; access limited to approved users | Authentication and written approval required for any new user | [Name] | [Date] |
| Interoperable | CSV where practical; ISO-style dates; documented units, categories, and missing-value codes | Proprietary source formats remain restricted | [Name] | [Date] |
| Reusable | Reproducible code, cleaning log, model documentation, limitations, and explicit reuse terms | Secondary use and redistribution require written approval | [Name] | [Date] |

- Repository or archive for approved materials: **[name/URL]**
- Data and code versioning method: **[describe]**
- Metadata retained after deletion: **[describe or none]**
- Secondary-use request decision-maker: **[Farm/contact]**
- Citation or acknowledgment text: **[text or anonymous]**

---

# Schedule C — Plain-Language Summary for the Farm

- **What data are requested?** Coded dairy-cow and milking-session records listed in Schedule A.
- **Why are they needed?** To study data cleaning and methods for predicting missing milk-yield or milk-flow values in a student project.
- **Who will see row-level data?** Only the approved users listed in Schedule A.
- **Will the data go on GitHub?** No. Only code, nonconfidential documentation, and approved aggregate outputs may be public.
- **Will AI be used?** Only project-specific statistical or machine-learning methods approved in Schedule A. The data will not be used to train a general-purpose AI model without separate written permission.
- **Will the Farm be identifiable?** Not in public or classroom outputs unless the Farm gives written permission.
- **What will the Farm receive?** [Plain-language summary or other deliverable].
- **How long will data be kept?** [Retention period], followed by [secure deletion/return/controlled archive].
- **How can the Farm withdraw or report a concern?** Contact [name/email/phone].
- **What happens after a security incident?** The Student will notify the Farm and Supervisor, contain the issue, and document corrective steps as described in Section 10.

## Reference points

This template incorporates:

- the [FAIR Guiding Principles](https://www.go-fair.org/fair-principles/), including the distinction between controlled accessibility and automatic public release;
- the [Ag Data Transparent Core Principles](https://www.agdatatransparent.com/principles), including clear terms for ownership, collection, use, access, portability, security, and disclosure; and
- [Cornell Research Services’ IRB guidance](https://researchservices.cornell.edu/resources/irb-faqs), which the Student and Supervisor should consult if the project could involve human participants or identifiable information about people.

Project-specific legal and institutional requirements control if they differ from this template.
