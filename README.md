# OrgAnalyze

Collect data from org-mode/org-roam pages and do some simple analyzing it

Items parsed:
 - Lines starting with "CLOCK:" or "#+CLK:" as OrgClock
 - Headers starting with "*", "**", etc. as OrgHeader
 - Tables starting with "|", as OrgTable

## export_org_to_markdown from org2md

Converts an org-mode file into a list of Markdown strings. It handles various org elements like headers, tables, source code blocks, and text.

### Conversion Rules
-   **Headers**: `* Header` becomes `# Header`, `** Sub-header` becomes `## Sub-header`, and so on.
-   **Tables**: Org-mode tables are converted to Markdown tables.
-   **Source Blocks**: `#+BEGIN_SRC language ... #+END_SRC` becomes a fenced code block in Markdown (```` ```language ... ``` ````).
-   **Math Blocks**: `\[ ... \]` becomes a fenced math block.
-   **Links**: Org-mode links are converted. `[[id:some-id][My Link]]` becomes `[[My Link]]` and `[[https://example.com][Example]]` becomes `[Example](https://example.com)`.
-   **Text**: Plain text lines are preserved.
-   **Ignored**: `CLOCK`, `PROPERTIES` blocks are currently ignored in the output.

### Example
```python
from org_analyze.org2md import export_org_to_markdown

markdown_lines = export_org_to_markdown('example.org')
for line in markdown_lines:
    print(line)

```

## read_org_clocks_2 from clocks

This function parses all `*.org` files in a given directory. It extracts all clocking information and associates it with its parent header (Feature) and sub-header (Task).

The function returns a tuple containing a list of column names and a list of rows. This structure is ideal for creating a pandas DataFrame.

### Example Usage

Let's say you have an org file `tasks.org` in a directory called `my_orgs` with the following content:

```org
* Feature A
** Task 1
CLOCK: [2025-10-25 Sat 10:00]--[2025-10-25 Sat 11:30] =>  1:30
** Task 2
CLOCK: [2025-10-25 Sat 12:00]--[2025-10-25 Sat 13:00] =>  1:00

* Feature B
** Task 3
CLOCK: [2025-10-25 Sat 14:00]--[2025-10-25 Sat 14:30] =>  0:30
```

You can parse this file and analyze the data with pandas like this:

```python
import pandas as pd
from org_analyze.clocks import read_org_clocks_2

# 1. Parse the org files in the directory
columns, rows = read_org_clocks_2('my_orgs')

# 2. Create a pandas DataFrame
df = pd.DataFrame(rows, columns=columns)

# 3. Analyze the data: Group by feature (head1) and sum the duration
feature_hours = df.groupby('head1')['duration'].sum()

print("Total hours per feature:")
print(feature_hours)

```

Output:

```
Total hours per feature:
head1
Feature A    2.5
Feature B    0.5
Name: duration, dtype: float64
```
