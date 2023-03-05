# Data models (work in progress)

**Route**

| column name | description | example |
|-------------|-------------|----------
| `id` | primary key | `1` |
| `name` | Route name | '376', 'M1'

**Stop**

| column name | description | example |
|-------------|-------------|----------
| `id` | primary key | `1` |
| `name` | Stop full name | Obolonsky ave. |

### ERM

``` mermaid
	erDiagram

		Route ||--|{ Schedule : "goes on"
		Schedule }o--|| Stop : contains
```
