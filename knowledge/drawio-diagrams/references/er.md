# ER diagram (crow's foot)

Answers "what is stored and how the pieces relate".

## Parts

| Part | How |
| --- | --- |
| Entity | A square-cornered frame named with the thing in plain words ("นักศึกษา (Student)"); attributes listed inside, one per line |
| Key | Mark the primary key with `PK` and a foreign key with `FK` before the attribute |
| Relationship | A solid line between entities with crow's foot ends: `startArrow=ERmandOne;endArrow=ERmany;` (draw.io names: `ERone`, `ERmandOne`, `ERmany`, `ERzeroToMany`, `ERoneToMany`) |
| Relationship label | A verb on the line: "ลงทะเบียน" |

## Rules

| Rule | Why |
| --- | --- |
| 4 to 7 entities per page | Beyond that, split by area (people, courses, grades) |
| Show only attributes a reader needs: keys plus up to 5 others | Full column lists belong in the schema, not the picture |
| Read each line aloud both ways: "นักศึกษา ลงทะเบียน หลายวิชา" | If a direction sounds wrong, the symbol is wrong |
| Cardinality ends are never omitted | An unmarked line says nothing about one or many |
| Focus colour marks the entity the discussion is about | Gives a non-expert an entry point |

An attribute list is text inside a frame, so it stays inside the 16px minimum; if the list does not fit, cut attributes rather than the font.
