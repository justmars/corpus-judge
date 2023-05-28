---
hide:
- navigation
---

# Justice

A Justice, as defined in this reference document, is one of many justices sitting in the Supreme Court:

::: corpus_judge.justice_model.Justice

## Cleaning Raw Justice Names

::: corpus_judge.justice_name.OpinionWriterName

## Candidate Justice

::: corpus_judge.justice_select.CandidateJustice

## View chief justice dates

```sql
WITH end_chief_date(d) AS (
    -- For each chief justice, get a second date: the date that the next chief justice is appointed; Can get this by getting the first chief date greater than the present chief date and using an ascending order. */
    SELECT
        DATE(
            tbl2.chief_date,
            '-1 day'
        )
    FROM
        {{ justice_table }}
        tbl2
    WHERE
        tbl2.chief_date IS NOT NULL
        AND tbl2.chief_date > tbl1.chief_date
    ORDER BY
        tbl2.chief_date ASC
    LIMIT
        1
), time_as_chief(period) AS (
    -- Difference between the two chief dates: that will be the time served as chief in years format */
    SELECT
        (
            SELECT
                DATE(d)
            FROM
                end_chief_date
        ) - DATE(
            tbl1.chief_date
        )
)
SELECT
    tbl1.id,
    tbl1.last_name,
    tbl1.chief_date,
    (
        SELECT
            d
        FROM
            end_chief_date
    ) max_end_chief_date,
    MIN(
        tbl1.inactive_date,
        (
            SELECT
                d
            FROM
                end_chief_date
        )
    ) actual_inactive_as_chief,
    (
        SELECT
            period
        FROM
            time_as_chief
    ) years_as_chief
FROM
    {{ justice_table }}
    tbl1
WHERE
    tbl1.chief_date IS NOT NULL
ORDER BY
    tbl1.chief_date DESC
```

```py
[
    {
        'id': 178,
        'last_name': 'Gesmundo',
        'chief_date': '2021-04-05',
        'max_end_chief_date': None,
        'actual_inactive_as_chief': None,
        'years_as_chief': None
    },
    {
        'id': 162,
        'last_name': 'Peralta',
        'chief_date': '2019-10-23',
        'max_end_chief_date': '2021-04-04',
        'actual_inactive_as_chief': '2021-03-27',
        'years_as_chief': 2
    },
    {
        'id': 163,
        'last_name': 'Bersamin',
        'chief_date': '2018-11-26',
        'max_end_chief_date': '2019-10-22',
        'actual_inactive_as_chief': '2019-10-18',
        'years_as_chief': 1
    },
    {
        'id': 160,
        'last_name': 'Leonardo-De Castro',
        'chief_date': '2018-08-28',
        'max_end_chief_date': '2018-11-25',
        'actual_inactive_as_chief': '2018-10-08',
        'years_as_chief': 0
    }...
]
```
